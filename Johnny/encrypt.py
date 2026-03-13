import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class encryptor:
    def __init__(self):
        self.key = AESGCM.generate_key(bit_length=256)
        self.worker = AESGCM(self.key)
    
    def encrypt_from_string(self, data):
        nonce = os.urandom(12)
        ciphertext = self.worker.encrypt(nonce, data, None)
        return [nonce, ciphertext]
    
    def decrypt(self, nonce, cipher):
        return self.worker.decrypt(nonce, cipher, None)
    
    def encrypt_to_file(self, data, filename):
        nonce, ciphertext = self.encrypt_from_string(data)

        with open(filename, "wb") as f:
            f.write(nonce + ciphertext)
