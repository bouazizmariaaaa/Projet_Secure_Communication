import random
from math import gcd

def est_premier(nombre: int, essais: int = 20) -> bool:
    if nombre < 2: return False
    if nombre in (2, 3): return True
    if nombre % 2 == 0: return False
    d, r = nombre - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(essais):
        a = random.randrange(2, nombre - 1)
        x = pow(a, d, nombre)
        if x == 1 or x == nombre - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, nombre)
            if x == nombre - 1: break
        else: return False
    return True

def inverse_modulaire(e: int, phi: int) -> int:
    ancien_reste, reste = e, phi
    ancien_x, x = 1, 0
    while reste != 0:
        quotient = ancien_reste // reste
        ancien_reste, reste = reste, ancien_reste - quotient * reste
        ancien_x, x = x, ancien_x - quotient * x
    return ancien_x % phi

def generer_cles_auto(bits: int = 512):
    taille_p_q = bits // 2
    def gen_prime():
        while True:
            n = random.getrandbits(taille_p_q)
            n |= (1 << (taille_p_q - 1)) | 1
            if est_premier(n): return n
    p, q = gen_prime(), gen_prime()
    while p == q: q = gen_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = inverse_modulaire(e, phi)
    return (e, n), (d, n)

def generer_cles():
    return generer_cles_auto(512)

def chiffrer(message_int: int, cle_publique: tuple) -> int:
    e, n = cle_publique
    return pow(message_int, e, n)

def dechiffrer(chiffre_int: int, cle_privee: tuple) -> int:
    d, n = cle_privee
    return pow(chiffre_int, d, n)
