#!/usr/bin/env python3

import zipfile

import sys


# You are provided with a ZIP file that is encrypted with a password. 
# The goal is to crack the password by trying each one from a list of possible passwords provided in a file called 'passwords.txt'.

# The ZIP file is protected with a password, and you do not know which one is correct.
# You will attempt to open the ZIP file by trying each password in the 'passwords.txt' file, which contains a list of potential passwords.
# The script will iterate over the passwords, trying each one until the correct password is found, at which point the contents of the ZIP file will be extracted.
# If the correct password is found, it will be printed to the console.

zip_file_path = 'crack_me.zip'
passwords_file_path = 'passwords.txt'

def crack_zip(zip_file, passwords_file):
    with zipfile.ZipFile(zip_file) as zf:
        with open(passwords_file, 'r') as pf:
            for line in pf:
                password = line.strip()  # Get rid of any newline characters
                try:
                    # TODO 1: Extract the ZIP file with the current password - don't forget the encoding :)
                    zf.extractall(pwd=bytes(password, 'utf-8'))

                    # TODO 2: If the extraction is successful, print the password found
                    print(f"Yuppi! Password found: {password}")
                    # The password should be "sunshine"
                
                    # TODO 3: Exit the function if the password is correct
                    return 0


                except:
                    continue
            # TODO 4: Print a message if the password was not found
            print("[ERROR] The 'passwords.txt' does NOT contain a valid password!", file=sys.stderr)
            return 1 
    return None


if __name__ == '__main__':
    # TODO 5: Call the crack_zip function
    crack_zip(zip_file_path, passwords_file_path)
