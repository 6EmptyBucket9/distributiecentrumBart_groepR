import random
import string

# Function to generate a random track and trace code
def generate_track_and_trace_code(length=12):
    """Generate a random track and trace code."""
    characters = string.ascii_letters + string.digits  # Includes both letters and digits
    track_code = ''.join(random.choice(characters) for i in range(length))
    return track_code