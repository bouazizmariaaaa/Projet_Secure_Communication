from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

def generer_cles():
    cle = RSA.generate(2048)
    cle_privee = cle
    cle_publique = cle.publickey()
    return cle_privee, cle_publique

def signer_message(message: str, cle_privee) -> bytes:
    hasher = SHA256.new(message.encode("utf-8"))
    signature = pkcs1_15.new(cle_privee).sign(hasher)
    return signature

def verifier_signature(message: str, signature: bytes, cle_publique) -> bool:
    hasher = SHA256.new(message.encode("utf-8"))
    try:
        pkcs1_15.new(cle_publique).verify(hasher, signature)
        return True  # La signature est valide et le message est intact
    except (ValueError, TypeError):
        return False  # Signature invalide ou message altéré
