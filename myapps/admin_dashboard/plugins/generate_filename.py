import uuid
import os

def generate_filename(instance, filename):
    # Generate a unique filename using a UUID
    filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    # Return the path where the file should be uploaded
    return os.path.join('photo', filename)