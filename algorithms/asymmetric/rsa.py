from math import gcd
import random

def est_premier(nombre, essais=20):
  
    if nombre < 2:
        return False
    if nombre in (2, 3):
        return True
    if nombre % 2 == 0:
        return False

    d = nombre - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(essais):
        a = random.randrange(2, nombre - 1)
        x = pow(a, d, nombre)

        if x == 1 or x == nombre - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, nombre)
            if x == nombre - 1:
                break
        else:
            return False  
    return True

def inverse_modulaire(e, phi):
    ancien_reste, reste = e, phi
    ancien_x, x = 1, 0

    while reste != 0:
        quotient = ancien_reste // reste
        ancien_reste = reste 
        reste = ancien_reste - quotient * reste
        ancien_x, x = x, ancien_x - quotient * x

    return ancien_x % phi

def demander_nombre_premier():
    while True:
        try:
            valeur = int(input(f"Entrez un nombre premier de 512 bits: "))
        except ValueError:
            print("Ce n'est pas un entier valide, réessayez.")
            continue

        if valeur.bit_length() != 512:
            print(f"doit faire exactement 512 bits ")
            continue

        if not est_premier(valeur):
            print(f"Ce nombre n'est pas premier, réessayez.")
            continue

        return valeur

def generer_cles():
    P = demander_nombre_premier("P")
    while True:
        Q = demander_nombre_premier("Q")
        if Q != P:
            break
        print("Q doit être différent de P, réessayez.")

    N = P * Q
    PHI = (P - 1) * (Q - 1)
    E = 65537
    D = inverse_modulaire(E, PHI)
    cle_publique = (E, N)
    cle_privee = (D, N)

    return cle_publique, cle_privee

def chiffrer(message, cle_publique):
    e, n = cle_publique
    return pow(message, e, n)


def dechiffrer(chiffre, cle_privee):
    d, n = cle_privee
    return pow(chiffre, d, n)

def generer_cles_auto(bits=512):
    return generer_cles()

