'''
This script uses symmetric encryption built on the AES algorithm to encrypt or decrypt files, byte objects or string objects.


'''

'''
very basic encryption example, using a string:

write_key()
key = load_key()
message = "Dwight, you ignorant slut!".encode()
f = Fernet(key)
encrypted_message = f.encrypt(message)
print(encrypted_message)

decrypted_message = f.decrypt(encrypted_message)
print(decrypted_message)

'''

# Fernet uses symmetric authenticated cryptography
from cryptography.fernet import Fernet


# generate a key and save it to a file
def write_key():
    key = Fernet.generate_key()                 # generates a fresh fernet key
    with open("key.key", "wb") as key_file:     # don't lose the key, or you can't decrypt the files
        key_file.write(key)


# don't generate the key every time you encrypt something with the same key
def load_key():
    return open("key.key", "rb").read()     # loads the key from the directory 'key.key'


# given a filename (str) and key (bytes), this encrypts the file and writes it
def encrypt(filename, key):
    f = Fernet(key)

    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)


# given a filename (str) and key (bytes), this decrypts the file and writes it
def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    with open(filename, "wb") as file:
        file.write(decrypted_data)


write_key()

key = load_key()

file = "data.csv"

encrypt(file, key)

decrypt(file, key)