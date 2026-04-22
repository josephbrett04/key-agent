import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class encryptor:
    def __init__(self):
        # 1. Define where the master key should be saved
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.key_file = os.path.join(root_dir, "secret.key")
        
        # 2. If the key file already exists, load it!
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        
        # 3. If it doesn't exist, generate a new one and SAVE it!
        else:
            self.key = AESGCM.generate_key(bit_length=256)
            with open(self.key_file, "wb") as f:
                f.write(self.key)
                
        # 4. Spin up the AES engine using the persistent key
        self.worker = AESGCM(self.key)

    # ... keep your existing encrypt, decrypt, and decrypt_log_file functions below ...
    
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

    def decrypt_log_file(self, enc_filepath, output_filepath):
        try:
            with open(enc_filepath, "rb") as f:
                decrypted_data = b""
                
                while True:
                    # 1. Read the 1-byte nonce length
                    nonce_len_bytes = f.read(1)
                    if not nonce_len_bytes:
                        break  # End of file reached
                    nonce_len = int.from_bytes(nonce_len_bytes, "big")
                    
                    # 2. Read the actual nonce
                    nonce = f.read(nonce_len)
                    
                    # 3. Read the 4-byte ciphertext length
                    cipher_len_bytes = f.read(4)
                    cipher_len = int.from_bytes(cipher_len_bytes, "big")
                    
                    # 4. Read the actual ciphertext
                    ciphertext = f.read(cipher_len)
                    
                    # 5. Pass it to Johnny's existing decrypt logic
                    decrypted_chunk = self.decrypt(nonce, ciphertext)
                    decrypted_data += decrypted_chunk
                    
            # 6. Write the final decoded string to a new file
            with open(output_filepath, "w", encoding="utf-8") as out_f:
                out_f.write(decrypted_data.decode("utf-8"))
                
            return True
            
        except Exception as e:
            print(f"Decryption failed: {e}")
            return False
