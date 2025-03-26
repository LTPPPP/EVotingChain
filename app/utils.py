import hashlib
import re

def hash_data(data: str) -> str:
    """
    Create a secure hash of any input data
    """
    return hashlib.sha256(data.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """
    Basic email validation
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def generate_unique_id() -> str:
    """
    Generate a unique identifier
    """
    import uuid
    return str(uuid.uuid4())