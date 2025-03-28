from hashlib import sha256

def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256
    """
    return sha256(password.encode()).hexdigest()

def check_password(password: str, hashed_password: str) -> bool:
    """
    Check if a password matches a hashed password
    """
    return hash_password(password) == hashed_password