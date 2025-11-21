# Import necessary modules from Python and PyQt5
import sys
import re  # <-- used by normalize_mode
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QComboBox,
    QTextEdit, QMessageBox, QTextBrowser, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5 import uic

# Import your backend file that contains all the conversion functions 
import backend as backend


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
        uic.loadUi("BIN UI.ui", self)
        self.setWindowTitle("BINLATOR")          # Set window title
        self.setWindowIcon(QIcon("Logo.jpg"))    # Set window icon 

        #  Connect Python to widgets made in Qt Designer 
        self.combo: QComboBox = self.findChild(QComboBox, "comboBox")        # Dropdown menu
        self.text_1: QTextEdit = self.findChild(QTextEdit, "textEdit")       # Input text box
        self.text_2: QTextBrowser = self.findChild(QTextBrowser, "textBrowser")  # Output box
        self.trans_button: QPushButton = self.findChild(QPushButton, "pushButton")     # Translate button
        self.clear_button: QPushButton = self.findChild(QPushButton, "pushButton_2")  # Clear button
        self.copy_button: QPushButton = self.findChild(QPushButton, "pushButton_3")   # Copy Output button

        # --- Sample Input label under the input box ---
        self.sample_label: QLabel = QLabel(self)
        self.sample_label.setObjectName("sampleLabel")
        self.sample_label.setStyleSheet("color: rgb(255, 105, 180); font: 13pt 'Times New Roman';")
        self.sample_label.setText("")
        if self.text_1:
            g = self.text_1.geometry()
            self.sample_label.setGeometry(g.x(), g.y() + g.height() + 5, g.width(), 24)
        self.sample_label.hide()

        #  Connect buttons to their corresponding functions 
        self.trans_button.clicked.connect(self.translate)  # Runs translate() when clicked
        self.clear_button.clicked.connect(self.clear)      # Runs clear() when clicked
        if self.copy_button:
            self.copy_button.clicked.connect(self.copy_output)

        # When mode changes, update the sample hint
        if self.combo:
            self.combo.currentTextChanged.connect(self.update_sample_hint)

        #  Dictionary linking dropdown modes to backend functions 
        self.fn_map = {
            # Text Based Translations
            "Text - Unicode/ASCII": backend.text_to_unicode,
            "Text - Binary": backend.text_to_binary,
            "Text - Octal": backend.text_to_octal,
            "Text - Hexadecimal": backend.text_to_hex,

            # Binary Based translations
            "Binary (ASCII Bytes) - Text": backend.binary_to_text,
            "Binary (ASCII Bytes) - Unicode/ASCII": backend.binary_to_unicode,
            "Binary (ASCII Bytes) - Octal": backend.binary_to_octal,
            "Binary (ASCII Bytes) - Hexadecimal": backend.binary_to_hex,

            # Unicode/ASCII Based Translations
            "Unicode/ASCII - Text": backend.unicode_to_text,
            "Unicode/ASCII - Binary": backend.unicode_to_binary,
            "Unicode/ASCII - Octal": backend.unicode_to_octal,
            "Unicode/ASCII - Hexadecimal": backend.decimal_to_hex,

            # Octal Based Translations
            "Octal - Text": backend.octal_to_text,
            "Octal - Binary": backend.octal_to_binary,
            "Octal - Unicode/ASCII": backend.octal_to_unicode,
            "Octal - Hexadecimal": backend.octal_to_hex,

            #Hexadecimal Based Translations
            "Hexadecimal - Text": backend.hex_to_text,
            "Hexadecimal - Unicode/ASCII": backend.hex_to_decimal,
            "Hexadecimal - Octal": backend.hex_to_octal,
            "Hexadecimal - Binary": backend.hex_to_binary,
        }

        # Build a normalized lookup so small spacing/dash differences don’t break things
        self.fn_map_norm = {normalize_mode(k): v for k, v in self.fn_map.items()}

        # Initialize sample hint text based on current combo value
        self.update_sample_hint()

    # -----------------------------
    # Sample hint updater
    # -----------------------------
    def update_sample_hint(self, _=None):
        """Show a 'Sample Input:' hint under the Input box based on the selected mode."""
        if not (self.combo and self.sample_label):
            return

        mode = normalize_mode(self.combo.currentText())

        examples = {
            "Text - Unicode/ASCII": "Sample Input: Hi!  →  72 105 33",
            "Text - Binary": "Sample Input: Hi  →  01001000 01101001",
            "Text - Octal": "Sample Input: Hi  →  110 151",
            "Text - Hexadecimal": "Sample Input: Hi  →  48 69",

            "Binary (ASCII Bytes) - Text": "Sample Input: 01001000 01101001  →  Hi",
            "Binary (ASCII Bytes) - Unicode/ASCII": "Sample Input: 01001000 01101001  →  72 105",
            "Binary (ASCII Bytes) - Octal": "Sample Input: 01001000 01101001  →  110 151",
            "Binary (ASCII Bytes) - Hexadecimal": "Sample Input: 01001000 01101001  →  48 69",

            "Unicode/ASCII - Text": "Sample Input: 72 105  →  Hi",
            "Unicode/ASCII - Binary": "Sample Input: 72 105  →  01001000 01101001",
            "Unicode/ASCII - Octal": "Sample Input: 72 105  →  110 151",
            "Unicode/ASCII - Hexadecimal": "Sample Input: 72 105  →  48 69",

            "Octal - Text": "Sample Input: 110 151  →  Hi",
            "Octal - Binary": "Sample Input: 110 151  →  01001000 01101001",
            "Octal - Unicode/ASCII": "Sample Input: 110 151  →  72 105",
            "Octal - Hexadecimal": "Sample Input: 110 151  →  48 69",

            "Hexadecimal - Text": "Sample Input: 48 69 21  →  Hi!",
            "Hexadecimal - Unicode/ASCII": "Sample Input: 48 69  →  72 105",
            "Hexadecimal - Octal": "Sample Input: 48 69  →  110 151",
            "Hexadecimal - Binary": "Sample Input: 48 69  →  01001000 01101001",
        }

        text = examples.get(mode, "")

        if text:
            self.sample_label.setText(text)
            if self.text_1:
                g = self.text_1.geometry()
                self.sample_label.setGeometry(g.x(), g.y() + g.height() + 5, g.width(), 24)
            self.sample_label.show()
        else:
            self.sample_label.hide()

    # -----------------------------
    # UI helper: group binary input
    # -----------------------------
    def _group_binary_8(self, raw: str):
        """
        Binary helper:
          1) keep only 0 and 1,
          2) require length % 8 == 0,
          3) return 'xxxxxxxx xxxxxxxx ...' (8-bit groups) or None.
        """
        if raw is None:
            return None

        cleaned = ""
        for ch in raw:
            if ch == "0" or ch == "1":
                cleaned += ch

        if len(cleaned) == 0 or (len(cleaned) % 8) != 0:
            return None

        groups = []
        current = ""
        for bit in cleaned:
            current += bit
            if len(current) == 8:
                groups.append(current)
                current = ""

        if current:
            return None

        grouped = ""
        i = 0
        while i < len(groups):
            grouped += groups[i]
            if i != len(groups) - 1:
                grouped += " "
            i += 1

        return grouped

    # -----------------------------
    # UI helper: group octal input
    # -----------------------------
    def _group_octal_3(self, raw: str):
        """
        Octal helper:
          1) keep only digits 0–7,
          2) require length % 3 == 0,
          3) return 'xxx xxx ...' (3-digit octal groups) or None.
        Example: '110151' -> '110 151'
        """
        if raw is None:
            return None

        cleaned = ""
        for ch in raw:
            if ch in "01234567":
                cleaned += ch

        if len(cleaned) == 0 or (len(cleaned) % 3) != 0:
            return None

        groups = []
        current = ""
        for ch in cleaned:
            current += ch
            if len(current) == 3:
                groups.append(current)
                current = ""

        if current:
            return None

        grouped = ""
        i = 0
        while i < len(groups):
            grouped += groups[i]
            if i != len(groups) - 1:
                grouped += " "
            i += 1

        return grouped

    # -----------------------------
    # UI helper: normalize decimal codes (Unicode/ASCII input)
    # -----------------------------
    def _normalize_decimal_codes(self, raw: str):
        """
        Unicode/ASCII helper:

        - Keep only digits, spaces, commas, semicolons.
        - Turn commas/semicolons into spaces.
        - Collapse multiple spaces.
        Example:
            '72,105;  33'  -> '72 105 33'
        We do NOT try to guess splits like '72105' -> backend will show error.
        """
        if raw is None:
            return ""

        # Replace commas/semicolons with spaces
        temp = ""
        for ch in raw:
            if ch.isdigit():
                temp += ch
            elif ch in [",", ";"]:
                temp += " "
            elif ch.isspace():
                temp += " "
            # ignore any weird characters

        # Collapse multiple spaces
        temp = temp.strip()
        temp = re.sub(r"\s+", " ", temp)
        return temp

    #  Function: Clear the interface 
    def clear(self):
        if self.text_1:
            self.text_1.setPlainText("")
        if self.text_2:
            self.text_2.setPlainText("")
        if self.combo:
            self.combo.setCurrentIndex(0)
        self.update_sample_hint()

    #  Function: Copy output to clipboard 
    def copy_output(self):
        if not self.text_2:
            QMessageBox.warning(self, "Copy Failed", "Output box not found.")
            return

        text = self.text_2.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Nothing to Copy", "There’s no translated output yet.")
            return

        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Copied!", "Translated output copied to clipboard!")

    #  Function: Handle the translation process 
    def translate(self):
        if not (self.combo and self.text_1 and self.text_2):
            QMessageBox.critical(self, "Error", "UI elements not found (check objectNames in the .ui).")
            return

        mode_raw = self.combo.currentText()
        mode = normalize_mode(mode_raw)
        if mode.lower() == "select" or not mode:
            QMessageBox.information(self, "Pick a mode", "Please pick a mode of translation.")
            return

        user_input = self.text_1.toPlainText()

        # AUTO-SPACING / AUTO-CLEAN STEP (UI-side convenience)
        if mode.startswith("Binary"):
            grouped = self._group_binary_8(user_input)
            if grouped is not None:
                self.text_1.setPlainText(grouped)
                user_input = grouped

        elif mode.startswith("Octal"):
            grouped = self._group_octal_3(user_input)
            if grouped is not None:
                self.text_1.setPlainText(grouped)
                user_input = grouped

        elif mode.startswith("Unicode/ASCII"):
            normalized = self._normalize_decimal_codes(user_input)
            if normalized:
                self.text_1.setPlainText(normalized)
                user_input = normalized

        # Look up the correct backend function based on dropdown choice (normalized)
        func = self.fn_map_norm.get(mode)
        if func is None:
            QMessageBox.warning(
                self,
                "Pick a mode",
                f"Please pick a valid mode of translation.\n\nSelected: {mode_raw}"
            )
            return

        # Try running the backend function safely
        try:
            result = func(user_input)
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred:\n{e}")
            return

        # If backend returns an "Error: ..." message
        if isinstance(result, str) and result.startswith("Error:"):
            QMessageBox.warning(self, "Input Error", result)
            self.text_2.setPlainText("")
            return

        # Display the result in the output box 
        if isinstance(result, list):
            pretty = " ".join(str(x) for x in result)
            self.text_2.setPlainText(pretty)
        elif isinstance(result, str):
            self.text_2.setPlainText(result)
        else:
            self.text_2.setPlainText(str(result))


#  Main entry point of the program 
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


#  Only runs this if file is executed directly 
if __name__ == "__main__":
    main()
