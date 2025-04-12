from datetime import datetime
import hashlib
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

def generate_otp() -> str:
    """
    Generate a random OTP
    """
    import random
    return str(random.randint(100000, 999999))

def generate_session_id(user_id: str) -> str:
    """
    Generate a random session ID using user ID and current timestamp
    """    
    # Combine user_id with current timestamp for uniqueness
    timestamp = datetime.now().isoformat()
    combined = f"{user_id}{timestamp}"
    
    # Generate a hash of the combined string
    session_id = hashlib.sha256(combined.encode()).hexdigest()
    return session_id
