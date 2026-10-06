
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter

def generate_key(key_size: int = 16) -> bytes:
    return get_random_bytes(key_size)

def aes_encrypt_cbc(plaintext: str, key: bytes) -> tuple:
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext, iv

def aes_decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def aes_encrypt_ecb(plaintext: str, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext

def aes_decrypt_ecb(ciphertext: bytes, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def aes_encrypt_ctr(plaintext: str, key: bytes) -> tuple:
    cipher = AES.new(key, AES.MODE_CTR)
    ciphertext = cipher.encrypt(plaintext.encode())
    return ciphertext, cipher.nonce

def aes_decrypt_ctr(ciphertext: bytes, key: bytes, nonce: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()
