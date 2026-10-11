from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def generate_key(key_size: int = 16) -> bytes:
    if key_size in (16, 24, 32):
        return get_random_bytes(key_size)

def aes_encrypt_block(key: bytes, plaintext_block: bytes) -> bytes:
    if len(plaintext_block) != 16:
        raise ValueError(
            f"AES sans mode ne peut traiter qu'un bloc de 16 octets"
        )
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext_block = cipher.encrypt(plaintext_block)
    return ciphertext_block


def aes_decrypt_block(key: bytes, ciphertext_block: bytes) -> bytes:
    if len(ciphertext_block) != 16:
        raise ValueError(
            f"AES sans mode ne peut déchiffrer qu'un bloc de 16 octets. "
        )
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext_block = cipher.decrypt(ciphertext_block)
    return plaintext_block
