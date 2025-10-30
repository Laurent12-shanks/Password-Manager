"""##########################DEECRYPTOR.PY############################### """

from typing import Optional
from cryptography.fernet import Fernet
import pyperclip as pc
from utils.hash_manager import read_key, valid_password
from utils.crypto_utils import derive_key_from_password
from utils.path_utils import user_credentials_path
from os import path


"""
Lire le fichier username.credentials et retourner la chaîne chiffrée
(str) correspondant au service_name, ou None si non trouvée.
"""
def get_cipher(username: str, service_name: str) -> Optional[str]:
    filename = user_credentials_path(username)
    if not path.exists(filename):
        return None

    try:
        with open(filename, 'r', encoding="utf-8") as credentials:
            for line in credentials:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("\t")
                if len(parts) >= 3 and parts[0] == service_name:
                    return parts[2]
    except OSError as e:
        print(f"Error during reading credentials: {e}")
    return None


"""
Déchiffre le mot de passe du service demandé et le copie dans le presse-papier.
Retourne le mot de passe déchiffré (str) en cas de succès, ou None si échec.
"""
def decrypt_cipher(username: str, password: str) -> Optional[str]:
    stored_hash = read_key(username)
    if not stored_hash:
        print("Aucun hash stocké pour cet utilisateur.")
        return None

    if not valid_password(stored_hash, password):
        print("Mot de passe maître incorrect.")
        return None

    service_name = input("Service name: ").strip()
    cipher_text = get_cipher(username, service_name)

    if not cipher_text:
        print(f"Aucune entrée pour le service '{service_name}'.")
        return None

    # Dériver la clé Fernet (la même méthode que pour le chiffrement)
    salt = username.encode()
    key = derive_key_from_password(password, salt)  # renvoie bytes base64-urlsafe
    fernet = Fernet(key)

    try:
        # cipher_text est une string encodée (stockée via cipher.decode())
        decrypted_bytes = fernet.decrypt(cipher_text.encode())
        decrypted = decrypted_bytes.decode("utf-8")
        pc.copy(decrypted)  # copier dans le presse-papier
        print("Mot de passe déchiffré et copié dans le presse-papier.")
        return decrypted
    except Exception as e:
        print(f"Échec du déchiffrement : {e}")
        return None
