"""##########################ENCRYPTOR.PY###############################"""

from os import path
from utils.crypto_utils import derive_key_from_password
from getpass import getpass
from cryptography.fernet import Fernet
from utils.hash_manager import read_key, valid_password
from utils.file_manager import decrypt_file
from utils.path_utils import user_credentials_path


#derive_from_function

def encrypt_data(username: str, password: str) -> None:
    """Encrypt a service password and store it securely for the user."""
    stored_hash = read_key(username)

    if not valid_password(stored_hash, password):
        print("Wrong master password. Cannot encrypt data.")
        return

    service_name = input("Your service name: ").strip()
    username_service = input(f"Your username for {service_name}: ").strip()
    pwd_service = getpass(prompt=f"Your password for {service_name}: ").strip()

    # Derive encryption key from master password
    salt = username.encode()  # Using username as salt
    key = derive_key_from_password(password, salt)
    fernet = Fernet(key)

    cipher = fernet.encrypt(pwd_service.encode())
    store_credentials(username, password, service_name, username_service, cipher)


def store_credentials(
    username: str,
    password: str,
    service_name: str,
    username_service: str,
    cipher: bytes
) -> None:

    """Store encrypted credentials in a user's file."""
    filename= user_credentials_path(username)
    if path.exists(filename):
        decrypt_file(username, password)
    try:
        with open(filename, 'a', encoding="utf-8") as credentials:
            credentials.write(service_name + '\t' + username_service + '\t' + cipher.decode() + '\n')
        print("Your data has been stored successfully.")
    except OSError as e:
        print(f"Failed to store credentials: {e}")
