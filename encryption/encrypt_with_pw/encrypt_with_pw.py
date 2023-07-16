import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import secrets      # use to make the salt
import base64       # use to encode the key
import getpass      # securely handle password


# generate the salt used to derive the key
def generate_salt(size=16):
    return secrets.token_bytes(size)


def derive_key(salt, password):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def load_salt():
    return open("salt.salt", "rb").read()


def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    if load_existing_salt:
        salt = load_salt()

    elif save_salt:
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)

    derived_key = derive_key(salt, password)

    return base64.urlsafe_b64encode(derived_key)