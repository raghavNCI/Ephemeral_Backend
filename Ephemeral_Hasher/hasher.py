import hmac
import hashlib

def hash_string(input_string, key):
    """
    Hashes an input_string using HMAC and SHA-256 with a provided key.

    Args:
    input_string (str): The string to hash.
    key (str): The secret key for hashing.

    Returns:
    str: The resulting HMAC-SHA-256 hash, encoded in hexadecimal.
    """
    # Ensure the key and string are bytes
    byte_key = key.encode()
    byte_string = input_string.encode()

    # Create a new HMAC object using the provided key and SHA-256 as the hash function
    hasher = hmac.new(byte_key, byte_string, hashlib.sha256)
    
    # Return the hex digest of the hash
    return hasher.hexdigest()
