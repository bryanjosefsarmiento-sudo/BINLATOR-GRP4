# Import necessary modules from Python and PyQt5
import sys
import re  # <-- used by normalize_mode
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QComboBox,
    QTextEdit, QMessageBox, QTextBrowser
)
from PyQt5.QtGui import QIcon
from PyQt5 import uic

# Import your backend file that contains all the conversion functions 
import bryan as bryan


def normalize_mode(s: str) -> str:
    """
    Make combobox text consistent so it matches fn_map keys even if the UI
    has extra/missing spaces or uses en/em dashes.
    """
    s = (s or "")
    # unify different dashes to a plain hyphen
    s = s.replace("–", "-").replace("—", "-")
    # collapse multiple spaces
    s = re.sub(r"\s+", " ", s)
    # ensure single spaces around the hyphen
    s = re.sub(r"\s*-\s*", " - ", s)
    return s.strip()


class MainWindow(QMainWindow):  # Main window class (inherits from QMainWindow)
    def __init__(self):
        super().__init__()

        # Load the .ui file (created using Qt Designer)
        uic.loadUi("CUNT.ui", self)
        self.setWindowTitle("BINLATOR")          # Set window title
        self.setWindowIcon(QIcon("Logo.jpg"))    # Set window icon 

        #  Connect Python to widgets made in Qt Designer 
        # Find each widget by its "objectName" (set in Qt Designer)
        self.combo: QComboBox = self.findChild(QComboBox, "comboBox")        # Dropdown menu
        self.text_1: QTextEdit = self.findChild(QTextEdit, "textEdit")       # Input text box
        self.text_2: QTextBrowser = self.findChild(QTextBrowser, "textBrowser")  # Output box
        self.trans_button: QPushButton = self.findChild(QPushButton, "pushButton")     # Translate button
        self.clear_button: QPushButton = self.findChild(QPushButton, "pushButton_2")  # Clear button
        self.copy_button: QPushButton = self.findChild(QPushButton, "pushButton_3")   # Copy Output button

        #  Connect buttons to their corresponding functions 
        self.trans_button.clicked.connect(self.translate)  # Runs translate() when clicked
        self.clear_button.clicked.connect(self.clear)      # Runs clear() when clicked
        if self.copy_button:  # Check if copy button exists in the UI
            self.copy_button.clicked.connect(self.copy_output)  # Runs copy_output() when clicked

        #  Dictionary linking dropdown modes to backend functions 
        self.fn_map = {
            "Text - Unicode/ASCII": bryan.text_to_unicode,
            "Text - Binary": bryan.text_to_binary,
            "Text - Hexadecimal": bryan.text_to_hex,

            "Binary (ASCII Bytes) - Text": bryan.binary_to_text,
            "Binary (ASCII Bytes) - Unicode/ASCII": bryan.binary_to_unicode,
            "Binary (ASCII Bytes) - Hexadecimal": bryan.binary_to_hex,

            "Unicode/ASCII - Text": bryan.unicode_to_text,
            "Unicode/ASCII - Binary": bryan.unicode_to_binary,
            "Unicode/ASCII - Hexadecimal": bryan.decimal_to_hex,   

            "Hexadecimal - Text": bryan.hex_to_text,
            "Hexadecimal - Unicode/ASCII": bryan.hex_to_decimal,   
            "Hexadecimal - Binary": bryan.hex_to_binary,
        }

        # Build a normalized lookup so small spacing/dash differences don’t break things
        self.fn_map_norm = {normalize_mode(k): v for k, v in self.fn_map.items()}

    # -----------------------------
    # UI helper: group binary input
    # -----------------------------
    def _group_binary_8(self, raw: str):
        """
        Take whatever is in the input box and:
          1) keep only 0 and 1 (ignore spaces/other chars),
          2) ensure total length is a multiple of 8,
          3) return a string grouped into 8-bit chunks separated by spaces,
             e.g. "0100100001101001" -> "01001000 01101001".
        Returns None if invalid (backend will handle errors later).
        """
        if raw is None:
            return None

        # (1) Keep only '0' and '1' — ignore any spaces the user added.
        cleaned = ""
        for ch in raw:
            if ch == "0" or ch == "1":
                cleaned += ch
            # ignore spaces or any other characters, we don't keep them

        # (2) Must be non-empty and a multiple of 8 (1 byte per character)
        if len(cleaned) == 0 or (len(cleaned) % 8) != 0:
            return None  # let the backend raise a user-friendly error message

        # (3) Build 8-bit groups using a simple counter 
        groups = []
        current = ""
        for bit in cleaned:
            current += bit
            if len(current) == 8:
                groups.append(current)
                current = ""

        if current:  # shouldn't happen if len % 8 == 0, but be safe
            return None

        # Join groups with single spaces
        grouped = ""
        i = 0
        while i < len(groups):
            grouped += groups[i]
            if i != len(groups) - 1:
                grouped += " "
            i += 1

        return grouped

    #  Function: Clear the interface 
    def clear(self):
        # Clears all text fields and resets the dropdown
        if self.text_1:
            self.text_1.setPlainText("")  # Clear the input box
        if self.text_2:
            self.text_2.setPlainText("")  # Clear the output box
        if self.combo:
            self.combo.setCurrentIndex(0)  # Reset dropdown to first option

    #  Function: Copy output to clipboard 
    def copy_output(self):
        # Copies whatever text is currently displayed in the output box
        if not self.text_2:
            QMessageBox.warning(self, "Copy Failed", "Output box not found.")
            return

        text = self.text_2.toPlainText()  # Extract text from output box
        if not text.strip():  # If output is empty or only spaces
            QMessageBox.warning(self, "Nothing to Copy", "There’s no translated output yet.")
            return

        QApplication.clipboard().setText(text)  # Copy text to clipboard
        QMessageBox.information(self, "Copied!", "Translated output copied to clipboard!")

    #  Function: Handle the translation process 
    def translate(self):
        # Make sure all widgets exist
        if not (self.combo and self.text_1 and self.text_2):
            QMessageBox.critical(self, "Error", "UI elements not found (check objectNames in the .ui).")
            return

        # Get the selected translation mode from the dropdown, normalized
        mode_raw = self.combo.currentText()
        mode = normalize_mode(mode_raw)
        if mode.lower() == "select" or not mode:  # If user didn’t pick anything
            QMessageBox.information(self, "Pick a mode", "Please pick a mode of translation.")
            return

        # Get whatever text the user typed in the input box
        user_input = self.text_1.toPlainText()

        # ✅ AUTO-SPACING STEP (UI-side convenience, backend unchanged)
        # Only do this when the selected mode is one of the Binary modes.
        if mode.startswith("Binary"):
            grouped = self._group_binary_8(user_input)
            if grouped is not None:
                # Update the input box to the neatly spaced 8-bit form so the user sees it.
                self.text_1.setPlainText(grouped)
                user_input = grouped
            # If grouped is None, we leave the input as-is; backend will return a clear error.

        # Look up the correct backend function based on dropdown choice (normalized)
        func = self.fn_map_norm.get(mode)
        if func is None:  # If mode isn’t found in the dictionary
            QMessageBox.warning(
                self,
                "Pick a mode",
                f"Please pick a valid mode of translation.\n\nSelected: {mode_raw}"
            )
            return

        # Try running the backend function safely
        try:
            result = func(user_input)  # Pass user input to backend function
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred:\n{e}")
            return

        # If backend returns an "Error:" message
        if isinstance(result, str) and result.startswith("Error:"):
            QMessageBox.warning(self, "Input Error", result)
            self.text_2.setPlainText("")  # Clear the output box
            return

        #  Display the result in the output box 
        if isinstance(result, list):
            # If backend returns a list (like [65, 66, 67])
            pretty = " ".join(str(x) for x in result)  # Convert to string "65 66 67"
            self.text_2.setPlainText(pretty)
        elif isinstance(result, str):
            # If backend returns a normal string
            self.text_2.setPlainText(result)
        else:
            # For anything else (just convert to string)
            self.text_2.setPlainText(str(result))


#  Main entry point of the program 
def main():
    app = QApplication(sys.argv)  # Start the Qt application
    window = MainWindow()         # Create the main window
    window.show()                 # Show the main window on screen
    sys.exit(app.exec_())         # Run the app until closed


#  Only runs this if file is executed directly 
if __name__ == "__main__":
    main()


# bryan