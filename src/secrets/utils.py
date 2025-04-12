from cryptography.fernet import Fernet
from src.config import settings


def load_key():
    return settings.SECRET_ENRYPT

def encrypt_string(input_string: str) -> str:
    key = load_key().encode()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(input_string.encode())
    return encrypted.decode()

def decrypt_string(encrypted_string: str) -> str:
    key = load_key().encode()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_string.encode())
    return decrypted.decode()