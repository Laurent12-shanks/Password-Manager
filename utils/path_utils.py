"""########################## PATH UTILS.PY ###############################"""

def user_key_path(username: str) -> str:
    """Return the full path for the user's .key file."""
    return f"utils/keys/{username}.key"


def user_credentials_path(username: str) -> str:
    """Return the full path for the user's .credentials file."""
    return f"utils/credentials/{username}.credentials"
