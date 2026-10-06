from Crypto.Hash import SHA256

def hash_sha256(message: str) -> str:
    hasher = SHA256.new()
    hasher.update(message.encode('utf-8'))
    return hasher.hexdigest()

def verify_sha256(message: str, expected_hash: str) -> bool:
    computed_hash = hash_sha256(message)
    return computed_hash.lower() == expected_hash.lower()
