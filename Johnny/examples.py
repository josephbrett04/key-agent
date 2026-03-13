import encrypt

encryptor = encrypt.encryptor()
returns = encryptor.encrypt_from_string(b"secret secret secret")
nonce = returns[0]
ciphertext = returns[1]

print(encryptor.decrypt(nonce, ciphertext).decode('utf-8'))
encryptor.encrypt_to_file(b"secret secret secret", "hi.enc")