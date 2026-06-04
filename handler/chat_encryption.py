import os
import pickle
import json
from cryptography.fernet import Fernet
import hashlib

def get_encryption_key(session_id):
    """Derive encryption key from session ID"""
    key_material = hashlib.sha256(f"{session_id}".encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key_material))

def encrypt_chat_history(messages, session_id):
    """Encrypt chat history before saving"""
    cipher = get_encryption_key(session_id)
    plaintext = json.dumps(messages)
    encrypted = cipher.encrypt(plaintext.encode())
    return encrypted

def decrypt_chat_history(encrypted_data, session_id):
    """Decrypt saved chat history"""
    try:
        cipher = get_encryption_key(session_id)
        plaintext = cipher.decrypt(encrypted_data)
        return json.loads(plaintext.decode())
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")

def save_encrypted_chat(filepath, messages, session_id):
    """Save encrypted chat history to file"""
    encrypted = encrypt_chat_history(messages, session_id)
    with open(filepath, 'wb') as f:
        f.write(encrypted)

def load_encrypted_chat(filepath, session_id):
    """Load and decrypt chat history from file"""
    with open(filepath, 'rb') as f:
        encrypted = f.read()
    return decrypt_chat_history(encrypted, session_id)
