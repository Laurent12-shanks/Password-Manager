# Password Manager

Simple local password manager (Python).  
Uses Argon2 for password hashing and Fernet (cryptography) for symmetric encryption.

## Quick start (local)
1. Clone:
   ```bash
   git clone https://github.com/<yourname>/password-manager.git
   cd password-manager

2. Initialize:
 python init_structure.py
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# optional: generate a test master key (do NOT commit)
python init_keys.py


4. Run:
source venv/bin/activate
python password_manager.py