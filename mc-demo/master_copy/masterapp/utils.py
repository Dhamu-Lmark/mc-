# utils.py

import random
import string

def generate_token(length=32):
    """Generate a random token."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
