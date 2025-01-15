import secrets
import string

def generate_track_and_trace_code(length=10):
    """Generate a random track and trace code."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
