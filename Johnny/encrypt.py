import os
import stat
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class encryptor:
    def __init__(self, key_path="secret.key"):
        self.key_path = os.path.abspath(key_path)
        if os.path.exists(self.key_path):
            self.key = self._load_key()
        else:
            self.key = AESGCM.generate_key(bit_length=256)
            self._save_key()
        self.worker = AESGCM(self.key)

    def _save_key(self):
        with open(self.key_path, "wb") as f:
            f.write(self.key)
        os.chmod(self.key_path, stat.S_IRUSR | stat.S_IWUSR)

    def _load_key(self):
        with open(self.key_path, "rb") as f:
            return f.read()
    
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

    def decrypt_from_file(self, filename):
        # read length-prefixed encrypted entries from a file and decrypt them
        results = []
        with open(filename, "rb") as f:
            while True:
                nonce_len_byte = f.read(1)
                if not nonce_len_byte:
                    break
                nonce_len = int.from_bytes(nonce_len_byte, "big")
                nonce = f.read(nonce_len)
                ct_len = int.from_bytes(f.read(4), "big")
                ciphertext = f.read(ct_len)
                results.append(self.worker.decrypt(nonce, ciphertext, None).decode("utf-8"))
        return results
