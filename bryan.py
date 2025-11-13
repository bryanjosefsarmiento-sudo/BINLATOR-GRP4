# ==========================================================
# BINLATOR Translation Functions
# ==========================================================
# TEST CHANGE 123


# ===========================
# TEXT-BASED MODES
# ===========================

# Text → Unicode/ASCII
def text_to_unicode(user):
    try:
        if not isinstance(user, str): 
            # Checks if the input is a string using isinstance()
            return "Error: Input must be a string."
        if not user or user.isspace(): 
            # Checks if the user entered something (not empty or just spaces)
            return "Error: Please enter something, not just spaces."

        unicode_list = []  # list to store Unicode/ASCII numbers/output
        for char in user:
            unicode_list.append(ord(char)) 
            # 'ord()' converts each character to its Unicode/ASCII value
        return unicode_list
    except Exception:
        # Catches any unexpected error
        return "Error: Something went wrong while converting text to Unicode."


# Text → Binary
def text_to_binary(user):
    try:
        if not isinstance(user, str): 
            # Ensures the input is text
            return "Error: Input must be a string."
        if not user or user.isspace(): 
            # Prevents empty or whitespace-only inputs
            return "Error: Please enter something, not just spaces."

        binary_result = ''  # empty string to store binary output
        for char in user:
            binary_result += format(ord(char), '08b') + ' ' 
            # Converts each letter to binary (8 bits per character)
        return binary_result.strip()  # Removes the last extra space
    except Exception:
        return "Error: Something went wrong while converting text to binary."


# Text → Hexadecimal
def text_to_hex(user):
    try:
        if not isinstance(user, str): 
            return "Error: Input must be a string."
        if not user or user.isspace(): 
            return "Error: Please enter something, not just spaces."

        hex_list = []  # list to store hexadecimal results
        for char in user:
            hex_list.append(format(ord(char), 'X')) 
            # Converts each character to its hex code
        return hex_list
    except Exception:
        return "Error: Something went wrong while converting text to hexadecimal."


# ===========================
# BINARY-BASED MODES
# ===========================

# Binary → Text
def binary_to_text(user):
    try:
        if not isinstance(user, str): 
            # Checks that the input is a string of 0s and 1s
            return "Error: Input must be a string of binary values."
        if not user or user.isspace(): 
            # Checks for blank or whitespace input
            return "Error: Please enter something, not just spaces."

        cleaned = user.replace(" ", "")  
        # Removes spaces for counting the total bits
        if len(cleaned) % 8 == 0 and " " not in user.strip():  
            # Detects missing spaces between binary groups
            return "Error: Missing spaces between binary codes (e.g. '01001000 01101001')."

        text = ""  # stores result variable for converted text
        binary_values = user.split()  # splits binary input by spaces
        for binary in binary_values:
            decimal_value = int(binary, 2)  # converts binary to decimal
            text += chr(decimal_value)  # converts decimal to character
        return text
    except ValueError:
        # Handles invalid binary inputs
        return "Error: Make sure you only enter valid binary numbers (0s and 1s)."
    except Exception:
        return "Error: Something went wrong while converting binary to text."


# Binary → Unicode/ASCII
def binary_to_unicode(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string of binary values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."

        cleaned = user.replace(" ", "")
        if len(cleaned) % 8 == 0 and " " not in user.strip():
            # Same check for missing spaces
            return "Error: Missing spaces between binary codes (e.g. '01001000 01101001')."

        number_list = []  # stores decimal numbers
        for b in user.split():
            number_list.append(int(b, 2))  # converts binary to decimal
        return number_list
    except ValueError:
        return "Error: Make sure you only enter valid binary numbers (0s and 1s)"
    except Exception:
        return "Error: Something went wrong while converting binary to Unicode."


# Binary → Hexadecimal
def binary_to_hex(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string of binary values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."

        cleaned = user.replace(" ", "")
        if len(cleaned) % 8 == 0 and " " not in user.strip():
            return "Error: Missing spaces between binary codes (e.g. '01001000 01101001')."

        hex_list = []
        for b in user.split():
            decimal_value = int(b, 2)  # binary → decimal
            hex_list.append(format(decimal_value, 'X'))  # decimal → hex
        return hex_list
    except ValueError:
        return "Error: Make sure you only enter valid binary numbers (0s and 1s)"
    except Exception:
        return "Error: Something went wrong while converting binary to hexadecimal."


# ===========================
# UNICODE/ASCII-BASED MODES
# ===========================

# Unicode/ASCII → Text
def unicode_to_text(user):
    try:
        if not isinstance(user, str): 
            return "Error: Input must be a string of numbers."
        if not user or user.isspace(): 
            return "Error: Please enter something, not just spaces."

        number_list = []  # stores Unicode numbers
        for b in user.split():
            number_list.append(int(b))  # converts string to integer
        result_text = ''
        for code in number_list:
            result_text += chr(code)  # converts number to character
        return result_text
    except ValueError:
        return "Error: Please enter valid decimal numbers (e.g. 65 66 67)."
    except Exception:
        return "Error: Something went wrong while converting Unicode to text."


# Unicode/ASCII → Binary
def unicode_to_binary(user):
    try:
        if not isinstance(user, str): 
            return "Error: Input must be a string of numbers."
        if not user or user.isspace(): 
            return "Error: Please enter something, not just spaces."

        binary_list = []
        for code in user.split():
            number = int(code)  # converts text to number
            binary_list.append(format(number, '08b'))  # converts to binary
        return binary_list
    except ValueError:
        return "Error: Please enter valid decimal numbers."
    except Exception:
        return "Error: Something went wrong while converting Unicode to binary."


# Decimal (Unicode/ASCII) → Hexadecimal
def decimal_to_hex(user):
    try:
        if not isinstance(user, str): 
            return "Error: Input must be a string of numbers."
        if not user or user.isspace(): 
            return "Error: Please enter something, not just spaces."

        hex_list = []
        for num in user.split():
            number = int(num)
            hex_list.append(format(number, 'X'))  # converts decimal to hex
        return hex_list
    except ValueError:
        return "Error: Please enter valid decimal numbers."
    except Exception:
        return "Error: Something went wrong while converting decimal to hex."


# ===========================
# HEXADECIMAL-BASED MODES
# ===========================

# Hexadecimal → Text
def hex_to_text(user):
    try:
        if not isinstance(user, str): 
            return "Error: Input must be a string of hexadecimal values."
        if not user or user.isspace(): 
            return "Error: Please enter something, not just spaces."

        text_result = ""
        for num in user.split():
            text_result += chr(int(num, 16))  # hex → decimal → character
        return text_result
    except ValueError:
        return "Error: Please enter valid hexadecimal values (0–9, A–F)."
    except Exception:
        return "Error: Something went wrong while converting hex to text."


# Hexadecimal → Decimal (Unicode/ASCII)
def hex_to_decimal(user):
    try:
        if not isinstance(user, str): 
            return "Error: Input must be a string of hexadecimal values."
        if not user or user.isspace(): 
            return "Error: Please enter something, not just spaces."

        dec_list = []
        for num in user.split():
            dec_list.append(int(num, 16))  # hex → decimal
        return dec_list
    except ValueError:
        return "Error: Please enter valid hexadecimal values (0–9, A–F)."
    except Exception:
        return "Error: Something went wrong while converting hex to decimal."


# Hexadecimal → Binary
def hex_to_binary(user):
    try:
        if not isinstance(user, str): 
            return "Error: Input must be a string of hexadecimal values."
        if not user or user.isspace(): 
            return "Error: Please enter something, not just spaces."

        binary_list = []
        for h in user.split():
            decimal_value = int(h, 16)  # hex → decimal
            binary_list.append(format(decimal_value, '08b'))  # decimal → binary
        return binary_list
    except ValueError:
        return "Error: Please enter valid hexadecimal values (0–9, A–F)."
    except Exception:
        return "Error: Something went wrong while converting hex to binary."
