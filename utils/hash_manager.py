"""##########################HASH MANAGER.PY###############################""" 

from utils.path_utils import user_key_path
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


# Creation d'un objet PasswordHasher (Perf)
hasher = PasswordHasher()


# Function to convert password to hash
def generate_hash(password: str) -> str:
    return hasher.hash(password)


# Function to store crypted key in file
def store_key(username: str, key: str) -> str:
    try:
        with open(user_key_path(username), 'w', encoding="utf-8") as master_pwd:
            master_pwd.write(key)
        print(f'You are registered! Key for {username} was created successfully.')
        print('Restart the program to continue.')
    except OSError as e:
        print(f"Failed to store key for '{username}': {e}")


def read_key(username: str) -> str:
    try:
        with open(user_key_path(username), 'r', encoding="utf-8") as master_pwd:
            return master_pwd.read()
    except FileNotFoundError:
        print(f"No key found for '{username}'.")
        return ""


# Function to verify if password matches the stored hash
def valid_password(hash_stored: str, password: str) -> bool:
    try:
        PasswordHasher().verify(hash_stored, password)
        return True
    except VerifyMismatchError:
        return False
    except Exception as e:
        print(f"Verification failed: {e}")
        return False
