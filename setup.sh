#!/usr/bin/env bash
set -e

# 1) create venv
python3 -m venv venv

# 2) activate venv (note: source manually on Windows)
source venv/bin/activate

# 3) upgrade pip and install deps
pip install --upgrade pip
pip install -r requirements.txt

# 4) initialize folders
python3 init_structure.py

# 5) copy env example if .env not exists
if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env created from .env.example — edit .env to set paths if needed."
fi

echo "Setup complete. Activate venv with: source venv/bin/activate"
