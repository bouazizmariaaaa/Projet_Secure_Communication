import hashlib

def hash_sha256(message: str) -> str:
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

def verify_sha256(message: str, hash_valeur: str) -> bool:
    return hash_sha256(message) == hash_valeur
