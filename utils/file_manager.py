"""##########################FILE MANAGER.PY############################### """

from os import path
from cryptography.fernet import Fernet
from utils import hash_manager
from utils.hash_manager import read_key, valid_password
from utils.crypto_utils import derive_key_from_password
from utils.path_utils import user_credentials_path



"""Lire le contenu binaire du fichier credentials."""
def read_file(username: str) -> bytes:
    filename = user_credentials_path(username)

    try:
        with open(filename, 'rb') as file:
            return file.read()

    except FileNotFoundError:
        print(f"Aucun fichier de credentials trouvé pour {username}.")
        return b""
    except OSError as e:
        print(f"Erreur en lisant le fichier : {e}")
        return b""


"""Écrire des données binaires dans le fichier credentials."""
def write_file(username: str, data: bytes) -> None:
    filename = user_credentials_path(username)
    try:
        with open(filename, 'wb') as file:
            file.write(data)
    except OSError as e:
        print(f"Erreur en écrivant le fichier : {e}")


"""
Chiffrer le fichier de credentials complet avec la clé dérivée du mot de passe.
"""
def encrypt_file(username: str, password: str) -> None:
    stored_hash = read_key(username)

    if not valid_password(stored_hash, password):
        print("Mot de passe maître incorrect.")
        return

    salt = username.encode()
    key = derive_key_from_password(password, salt)
    fernet = Fernet(key)

    plaintext = read_file(username)
    if not plaintext:
        print("Aucun contenu à chiffrer.")
        return

    try:
        ciphertext = fernet.encrypt(plaintext)
        write_file(username, ciphertext)
        print(f"Fichier '{username}.credentials' chiffré avec succès.")
    except Exception as e:
        print(f"Erreur lors du chiffrement : {e}")


"""
Déchiffrer le fichier credentials et le réécrire en clair temporairement.
Retourne True si succès.
"""
def decrypt_file(username: str, password: str) -> bool:
    filename = user_credentials_path(username)

    if not path.exists(filename):
        print("Aucun fichier de credentials à déchiffrer.")
        return False

    stored_hash = read_key(username)
    if not valid_password(stored_hash, password):
        print("Mot de passe maître incorrect.")
        return False

    salt = username.encode()
    key = derive_key_from_password(password, salt)
    fernet = Fernet(key)

    ciphertext = read_file(username)
    if not ciphertext:
        print("Fichier vide ou illisible.")
        return False

    try:
        plaintext = fernet.decrypt(ciphertext)
        write_file(username, plaintext)
        print(f"Fichier '{filename}' déchiffré temporairement.")
        return True
    except Exception as e:
        print(f"Erreur lors du déchiffrement : {e}")
        return False


"""
Afficher le contenu texte du fichier credentials (en clair).
"""
def show_data_file(username: str) -> None:
    filename = user_credentials_path(username)
    if not path.exists(filename):
        print("Aucun fichier de données à afficher.")
        return

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            print("Données enregistrées :\n")
            for line in file:
                print(line.strip())
    except Exception as e:
        print(f"Impossible d'afficher le contenu : {e}")
