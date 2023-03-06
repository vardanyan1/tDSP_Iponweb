import hashlib
import os


def hash_file_name(filename):
    hash_object = hashlib.sha256(filename.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


def handle_uploaded_file(instance, filename):
    sub_folder = instance.__class__.__name__.lower()
    extension = os.path.splitext(filename)[1]
    hashed_filename = hash_file_name(filename) + extension
    return os.path.join(sub_folder, hashed_filename)
