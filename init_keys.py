#!/usr/bin/env python3
from pathlib import Path
from cryptography.fernet import Fernet
import os

#génère une clé maîtresse pour tests locaux

def generate_master_key(path: Path):
    if path.exists():
        print(f"{path} already exists — skipping key generation.")
        return
    key = Fernet.generate_key()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(key)
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass
    print(f"Master key generated at {path}")

if __name__ == "__main__":
    generate_master_key(Path("utils/keys/master.key"))

