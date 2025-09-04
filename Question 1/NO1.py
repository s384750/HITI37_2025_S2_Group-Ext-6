# Function to read the contents of a file
def read_func(filename):
    with open(filename, "r") as file:  # Open file in read mode
        content = file.read()          # Read entire file content
    return content                     # Return file data


# Function to write data into a file
def write_func(filename, data):
    with open(filename, "w") as file:  # Open file in write mode
        file.write(data)               # Write data to file


# Main function that drives the program
def Main():
    # Get shift values from user
    shift1 = int(input("input the shift 1 value\t"))
    shift2 = int(input("input the shift 2 value\t"))

    # Read original text from file
    raw_file_data = read_func('raw_text.txt')

    # Encrypt the raw text
    e_data = encrpted_func(raw_file_data, shift1, shift2)

    # Write the encrypted text to new file
    write_func("encrpted_file.txt", e_data)

    # Read encrypted text back from file
    e_file_data = read_func("encrpted_file.txt")

    # Decrypt the encrypted text
    d_data = decrpted_func(e_file_data, shift1, shift2)

    # Write the decrypted text to new file
    write_func("decrpted_file.txt", d_data)

    # Read decrypted text back from file
    d_file_data = read_func("decrpted_file.txt")

    # Verify that original and decrypted data match
    verification(raw_file_data, d_file_data)


# Encryption function
def encrpted_func(name, shift1, shift2):
    content = ""  # Store encrypted text
    for char in name:
        # Handle lowercase letters
        if char.islower():
            if 'a' <= char <= 'm':  # First half of lowercase alphabet
                shift = shift1 * shift2
                new_char = chr(((ord(char) - ord('a') + shift) % 13) + ord('a'))
                content = content + new_char
            elif 'n' <= char <= 'z':  # Second half of lowercase alphabet
                shift = -(shift1 + shift2)
                new_char = chr(((ord(char) - ord('n') + shift) % 13) + ord('n'))
                content = content + new_char
            else:
                content = content + char

        # Handle uppercase letters
        elif char.isupper():
            if 'A' <= char <= 'M':  # First half of uppercase alphabet
                shift = -(shift1)
                new_char = chr(((ord(char) - ord('A') + shift) % 13) + ord('A'))
                content = content + new_char
            elif 'N' <= char <= 'Z':  # Second half of uppercase alphabet
                shift = shift2 ** 2
                new_char = chr(((ord(char) - ord('N') + shift) % 13) + ord('N'))
                content = content + new_char
            else:
                content = content + char
        else:
            content = content + char  # Leave non-alphabet characters unchanged

    print("encrpting text................")
    return content


# Decryption function (reverse of encryption)
def decrpted_func(name, shift1, shift2):
    content = ""  # Store decrypted text
    for char in name:
        # Handle lowercase letters
        if char.islower():
            if 'a' <= char <= 'm':  # Reverse shift for first half
                shift = -(shift1 * shift2)
                new_char = chr(((ord(char) - ord('a') + shift) % 13) + ord('a'))
                content = content + new_char
            elif 'n' <= char <= 'z':  # Reverse shift for second half
                shift = (shift1 + shift2)
                new_char = chr(((ord(char) - ord('n') + shift) % 13) + ord('n'))
                content = content + new_char
            else:
                content += char

        # Handle uppercase letters
        elif char.isupper():
            if 'A' <= char <= 'M':  # Reverse shift for first half
                shift = shift1
                new_char = chr(((ord(char) - ord('A') + shift) % 13) + ord('A'))
                content = content + new_char
            elif 'N' <= char <= 'Z':  # Reverse shift for second half
                shift = -(shift2 ** 2)
                new_char = chr(((ord(char) - ord('N') + shift) % 13) + ord('N'))
                content = content + new_char
            else:
                content = content + char
        else:
            content += char  # Leave non-alphabet characters unchanged

    print("decrpting text................")
    return content


# Verification function to check if encryption/decryption worked correctly
def verification(raw_file, d_file):
    if raw_file != d_file:
        print("encrption and decrption unsuccessful")
    elif raw_file == d_file:
        print("encrption and decrption successful")


# Call the main function to run the program
Main()
