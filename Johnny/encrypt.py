import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class encryptor:
    def __init__(self):
        self.key = AESGCM.generate_key(bit_length=256)
        self.worker = AESGCM(self.key)
    
    def encrypt_from_string(self, data):
        nonce = os.urandom(12)
        ciphertext = self.worker.encrypt(nonce, data, None)
        return nonce, ciphertext