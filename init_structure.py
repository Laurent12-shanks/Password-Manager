#!/usr/bin/env python3
import os

def ensure(path):
    os.makedirs(path, exist_ok=True)
    gitkeep = os.path.join(path, ".gitkeep")
    if not os.path.exists(gitkeep):
        open(gitkeep, "w").close()

if __name__ == "__main__":
    ensure("utils/keys")
    ensure("utils/credentials")
    print("Folders ensured: utils/keys and utils/credentials (with .gitkeep).")
