import pytest
from algorithms.classical.caesar import caesar_encrypt, caesar_decrypt
from algorithms.classical.vigenere import vigenere_encrypt, vigenere_decrypt
from algorithms.classical.playfair import playfair_encrypt, playfair_decrypt
from algorithms.symmetric.modes import aes_encrypt_cbc, aes_decrypt_cbc
from algorithms.asymmetric.rsa import generer_cles_auto, chiffrer, dechiffrer
from algorithms.hash.sha256 import hash_sha256, verify_sha256

def test_caesar():
    msg = "HELLO WORLD"
    encrypted = caesar_encrypt(msg, 5)
    assert caesar_decrypt(encrypted, 5) == msg

def test_vigenere():
    msg = "SECRET MESSAGE"
    key = "KEY"
    encrypted = vigenere_encrypt(msg, key)
    assert vigenere_decrypt(encrypted, key) == msg

def test_playfair():
    msg = "HELLOMESSAGE"
    key = "KEYWORD"
    encrypted = playfair_encrypt(msg, key)
    decrypted = playfair_decrypt(encrypted, key)
    assert "HEL" in decrypted

def test_aes_cbc():
    msg = "Message Secret AES"
    key = b"1234567890123456"
    ciphertext, iv = aes_encrypt_cbc(msg, key)
    decrypted = aes_decrypt_cbc(ciphertext, key, iv)
    assert decrypted == msg

def test_rsa():
    pub, priv = generer_cles_auto(512)
    m = 12345
    c = chiffrer(m, pub)
    d = dechiffrer(c, priv)
    assert d == m

def test_sha256():
    msg = "TestHash"
    h = hash_sha256(msg)
    assert verify_sha256(msg, h) is True
