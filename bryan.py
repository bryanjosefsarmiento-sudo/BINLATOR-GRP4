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
        
        user = user.rstrip() # ignores trailing spaces

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
        
        user = user.rstrip() # ignores trailing spaces

        binary_result = ''  # empty string to store binary output
        for char in user:
            binary_result += format(ord(char), '08b') + ' ' 
            # Converts each letter to binary (8 bits per character)
        return binary_result.strip()  # Removes the last extra space
    except Exception:
        return "Error: Something went wrong while converting text to binary."
    
# Text → Octal (list of octal strings, no 0o prefix)
def text_to_octal(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."
        
        user = user.rstrip() # ignores trailing spaces

        oct_list = []
        for ch in user:
            code = ord(ch)                 # Unicode code point
            oct_list.append(format(code, "o"))  # to octal (no prefix)
        return oct_list
    except Exception:
        return "Error: Something went wrong while converting text to octal."


# Text → Hexadecimal
def text_to_hex(user):
    try:
        if not isinstance(user, str): 
            return "Error: Input must be a string."
        if not user or user.isspace(): 
            return "Error: Please enter something, not just spaces."
        
        user = user.rstrip()  # ignores trailing spaces

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
            return "Error: Input must be a string of binary values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."

        cleaned = user.replace(" ", "")

        #  Must be at least 8 bits
        if len(cleaned) < 8:
            return "Error: Need at least 8 bits."

        # N If total bits > 8, require spaces
        if len(cleaned) > 8 and " " not in user.strip():
            return "Error: Missing spaces between bytes (e.g. '01000001 01000010')."

        # If exactly 8 bits, allow no spaces
        if len(cleaned) == 8:
            user = cleaned   # replace input with the clean single byte

        # Now normal grouped validation
        if len(cleaned) % 8 != 0:
            return "Error: Total bit length must be a multiple of 8."

        text = ""
        for b in user.split():
            if len(b) != 8:
                return "Error: Each group must be 8 bits."
            decimal_value = int(b, 2)
            text += chr(decimal_value)

        return text

    except ValueError:
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

        if len(cleaned) < 8:
            return "Error: Need at least 8 bits."

        #  allow single byte without spaces
        if len(cleaned) > 8 and " " not in user.strip():
            return "Error: Missing spaces between bytes (e.g. '01000001 01000010')."

        if len(cleaned) == 8:
            user = cleaned

        if len(cleaned) % 8 != 0:
            return "Error: Total bit length must be a multiple of 8."

        number_list = []
        for b in user.split():
            if len(b) != 8:
                return "Error: Each group must be 8 bits."
            number_list.append(int(b, 2))

        return number_list

    except ValueError:
        return "Error: Make sure you only enter valid binary numbers (0s and 1s)"
    except Exception:
        return "Error: Something went wrong while converting binary to Unicode."

# Binary to Octal 
def binary_to_octal(user):
    try:
        # If you added _auto_space_binary earlier, keep using it:
        # user = _auto_space_binary(user)

        if not isinstance(user, str):
            return "Error: Input must be a string of binary values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."
        # simple 0/1/space check (same pattern as others)
        for ch in user:
            if ch not in ("0","1"," ", "\t", "\n", "\r"):
                return "Error: Make sure you only enter valid binary numbers (0s and 1s)."

        out = []
        for tok in user.split():
            val = int(tok, 2)        # binary → decimal
            out.append(format(val, "o"))  # decimal → octal
        return out
    except ValueError:
        return "Error: Make sure you only enter valid binary numbers (0s and 1s)."
    except Exception:
        return "Error: Something went wrong while converting binary to octal."


# Binary → Hexadecimal
def binary_to_hex(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string of binary values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."

        cleaned = user.replace(" ", "")

        if len(cleaned) < 8:
            return "Error: Need at least 8 bits."

        if len(cleaned) > 8 and " " not in user.strip():
            return "Error: Missing spaces between bytes (e.g. '01000001 01000010')."

        if len(cleaned) == 8:
            user = cleaned

        if len(cleaned) % 8 != 0:
            return "Error: Total bit length must be a multiple of 8."

        hex_list = []
        for b in user.split():
            if len(b) != 8:
                return "Error: Each group must be 8 bits."
            decimal_value = int(b, 2)
            hex_list.append(format(decimal_value, 'X'))

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
    
# Unicode/ASCII → Octal
def unicode_to_octal(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string of numbers."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."

        out = []
        for tok in user.split():
            val = int(tok)            # string → int
            out.append(format(val, "o"))  # decimal → octal
        return out
    except ValueError:
        return "Error: Please enter valid decimal numbers."
    except Exception:
        return "Error: Something went wrong while converting decimal to octal."


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
    
# Hexadecimal → Octal
def hex_to_octal(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string of hexadecimal values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."

        out = []
        for tok in user.split():
            val = int(tok, 16)        # hex → decimal
            out.append(format(val, "o"))   # decimal → octal
        return out
    except ValueError:
        return "Error: Please enter valid hexadecimal values (0–9, A–F)."
    except Exception:
        return "Error: Something went wrong while converting hexadecimal to octal."

# ===========================
# OCTAL-BASED MODES
# ===========================

# ===========================
# OCTAL HELPERS
# ===========================

def _is_octal_or_space(s: str) -> bool:
    """True only if s contains digits 0–7 and/or whitespace."""
    for ch in s:
        if ch not in ("0","1","2","3","4","5","6","7"," ", "\t", "\n", "\r"):
            return False
    return True

# Octal → Text (space-separated octal code points)
def octal_to_text(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string of octal values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."
        if not _is_octal_or_space(user):
            return "Error: Please add spaces to octal values (0–7)."

        text = ""
        tokens = user.split()  # each token is one code point in base 8
        for tok in tokens:
            val = int(tok, 8)   # octal → decimal (code point)
            text += chr(val)    # decimal → character
        return text
    except ValueError:
        return "Error: Please enter valid octal values (0–7)."
    except Exception:
        return "Error: Something went wrong while converting octal to text."
    
# Octal → Binary (8-bit padded per code point)
def octal_to_binary(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string of octal values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."
        if not _is_octal_or_space(user):
            return "Error: Please enter valid octal values (0–7)."

        out = []
        for bry in user.split():
            val = int(bry, 8)               # octal → decimal
            out.append(format(val, "08b"))  # decimal → 8-bit binary
        return out
    except ValueError:
        return "Error: Please enter valid octal values (0–7)."
    except Exception:
        return "Error: Something went wrong while converting octal to binary."
    

# Octal → Unicode/ASCII
def octal_to_unicode(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string of octal values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."
        if not _is_octal_or_space(user):
            return "Error: Please enter valid octal values (0–7)."

        out = []
        for tok in user.split():
            out.append(int(tok, 8))  # octal → decimal
        return out
    except ValueError:
        return "Error: Please enter valid octal values (0–7)."
    except Exception:
        return "Error: Something went wrong while converting octal to decimal."
    
# Octal → Hexadecimal (uppercase, no 0x)
def octal_to_hex(user):
    try:
        if not isinstance(user, str):
            return "Error: Input must be a string of octal values."
        if not user or user.isspace():
            return "Error: Please enter something, not just spaces."
        if not _is_octal_or_space(user):
            return "Error: Please enter valid octal values (0–7)."

        out = []
        for tok in user.split():
            val = int(tok, 8)           # octal → decimal
            out.append(format(val, "X"))  # decimal → HEX uppercase
        return out
    except ValueError:
        return "Error: Please enter valid octal values (0–7)."
    except Exception:
        return "Error: Something went wrong while converting octal to hexadecimal."
