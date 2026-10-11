def chiffrer_aes(message):
    return "AES(" + message + ")"  

def chiffrer_rsa(message):
    return "RSA(" + message + ")"  

ALGOS = {
    "1": ("AES", chiffrer_aes),
    "2": ("RSA", chiffrer_rsa),
}

print("=== Choix de l'algorithme ===")
for cle, (nom, _) in ALGOS.items():
    print(f"{cle} - {nom}")

choix = input("Ton choix : ")

if choix in ALGOS:
    nom, fonction = ALGOS[choix]
    message = input("Message à chiffrer : ")
    print(f"Résultat avec {nom} :", fonction(message))
else:
    print("Choix invalide")
