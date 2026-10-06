import math

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

def diffie_hellman():
    # Saisie et test de p
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

key_secret = pow(B,a,p) 


