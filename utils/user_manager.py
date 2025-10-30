"""##########################USER MANAGER.PY############################### """

from os import path
from getpass import getpass
from utils.path_utils import user_key_path
from utils.hash_manager import read_key,valid_password

# files ".key" stored in half-folder "key"

def new_user() -> tuple[str, str]:
    username = input("Your name: ").strip()

    while path.exists(user_key_path(username)):
        print("This username is already taken. Choose another one.")
        username = input("Your username: ").strip()

    password = getpass(prompt="Your master password: ").strip()
    while len(password) < 8:
        print("Password too short. Please use at least 8 characters.")
        password = getpass(prompt="Your master password: ").strip()
    return username, password


def check_user(username: str, password: str) -> bool:
    if not path.exists(user_key_path(username)):
        print("You are not registered yet.")
        return False

    stored_hash = read_key(username)
    if valid_password(stored_hash, password):
        print(f'User: {username}, your password is correct.')
        return True
    else:
        print("Wrong password.")
        return False
