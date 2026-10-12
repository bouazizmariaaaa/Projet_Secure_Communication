import hashlib
import secrets


def est_premier(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def est_racine_primitive(g: int, p: int) -> bool:
    if g <= 1 or g >= p:
        return False
    elements_vus = {pow(g, i, p) for i in range(1, p)}
    return len(elements_vus) == p - 1

def generer_secret(p: int) -> int:
    return 2 + secrets.randbelow(p - 3)

def cle_publique(g: int, secret: int, p: int) -> int:
    return pow(g, secret, p)

def cle_partagee(autre_publique: int, secret: int, p: int) -> int:
    return pow(autre_publique, secret, p)

def deriver_cle_aes(secret_partage: int, taille: int = 16) -> bytes:
    return hashlib.sha256(str(secret_partage).encode()).digest()[:taille]

def diffie_hellman():
    p = int(input("Entrez un nombre premier p : "))
    if not est_premier(p):
        print("Erreur : p n'est pas premier.")
        return

    g = int(input(f"Entrez un générateur g (< {p}) : "))
    if not est_racine_primitive(g, p):
        print("Erreur : g n'est pas un générateur valide pour ce p.")
        return

    a = int(input(f"Entrez le secret 'a' (1 < a < {p}) : "))
    b = int(input(f"Entrez le secret 'b' (1 < b < {p}) : "))

    A = pow(g, a, p)
    B = pow(g, b, p)

    key_secret = pow(B, a, p)
    print(f"A = {A}, B = {B}, clé secrète commune = {key_secret}")
    return key_secret


if __name__ == "__main__":
    diffie_hellman()
