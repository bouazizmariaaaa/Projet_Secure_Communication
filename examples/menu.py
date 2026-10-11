import argparse
import json
import os
import socket
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RACINE not in sys.path:
    sys.path.insert(0, RACINE)

from network.protocol import SecureProtocol
from algorithms.classical.caesar import caesar_encrypt
from algorithms.classical.vigenere import vigenere_encrypt
from algorithms.classical.playfair import playfair_encrypt
from algorithms.symmetric.modes import (
    generate_key, aes_encrypt_cbc, aes_encrypt_ecb, aes_encrypt_ctr,
)
from algorithms.asymmetric import rsa
from algorithms.asymmetric import diffie_hellman as dh
from algorithms.hash.sha256 import hash_sha256
from algorithms.hash import signature

class Session:
    def __init__(self, host, port):
        self.sock = socket.create_connection((host, port), timeout=10)
        self.sock.settimeout(60)
        self.lecteur = self.sock.makefile("r", encoding="utf-8")

    def envoyer(self, payload):
        self.sock.sendall((payload + "\n").encode("utf-8"))
        ligne = self.lecteur.readline()
        if not ligne:
            raise ConnectionError("Le serveur a fermé la connexion")
        return json.loads(ligne)

    def fermer(self):
        self.lecteur.close()
        self.sock.close()
def demander(question, valider=lambda s: True, erreur="Entrée invalide, réessaie."):
    while True:
        valeur = input(question)
        if valider(valeur):
            return valeur
        print(erreur)


def est_entier(texte):
    try:
        int(texte)
        return True
    except ValueError:
        return False


def est_cle_lettres(texte):
    return texte.isalpha() and texte.isascii()

def menu_caesar(session, message):
    cle = int(demander("Décalage (nombre entier) : ", est_entier))
    chiffre = caesar_encrypt(message, cle)
    print(f"Message chiffré : {chiffre}")
    return session.envoyer(SecureProtocol.create_message("Caesar", "None", str(cle), "", chiffre))


def menu_vigenere(session, message):
    cle = demander("Clé (lettres uniquement, sans accent) : ", est_cle_lettres,
                   "La clé doit contenir uniquement des lettres A-Z.")
    chiffre = vigenere_encrypt(message, cle)
    print(f"Message chiffré : {chiffre}")
    return session.envoyer(SecureProtocol.create_message("Vigenere", "None", cle, "", chiffre))


def menu_playfair(session, message):
    cle = demander("Clé (lettres uniquement, sans accent) : ", est_cle_lettres,
                   "La clé doit contenir uniquement des lettres A-Z.")
    chiffre = playfair_encrypt(message, cle)
    print(f"Message chiffré : {chiffre}")
    print("(Playfair travaille en majuscules, sans espaces, J devient I, X sert de remplissage.)")
    return session.envoyer(SecureProtocol.create_message("Playfair", "None", cle, "", chiffre))


def menu_aes(session, message):
    mode = demander("Mode (ECB / CBC / CTR) : ",
                    lambda s: s.strip().upper() in ("ECB", "CBC", "CTR")).strip().upper()
    while True:
        saisie = input("Clé AES (16, 24 ou 32 caractères, Entrée = clé aléatoire) : ")
        if saisie == "":
            cle = generate_key(16)
            break
        if len(saisie.encode("utf-8")) in (16, 24, 32):
            cle = saisie.encode("utf-8")
            break
        print("La clé doit faire exactement 16, 24 ou 32 octets.")

    iv = b""
    if mode == "ECB":
        chiffre = aes_encrypt_ecb(message, cle)
    elif mode == "CBC":
        chiffre, iv = aes_encrypt_cbc(message, cle)
    else:
        chiffre, iv = aes_encrypt_ctr(message, cle)

    print(f"Clé (hex)       : {cle.hex()}")
    print(f"Message chiffré : {chiffre.hex()}")
    payload = SecureProtocol.create_message("AES", mode, cle.hex(), iv.hex(), chiffre.hex())
    return session.envoyer(payload)


def menu_rsa(session, message):
    rep = session.envoyer(SecureProtocol.create_message("RSA_PUBKEY", "None", "", "", ""))
    e, n = int(rep["e"]), int(rep["n"])
    print(f"Clé publique du serveur reçue (n de {n.bit_length()} bits)")
    donnees = message.encode("utf-8")
    blocs = [rsa.chiffrer(int.from_bytes(donnees[i:i + 32], "big"), (e, n))
             for i in range(0, len(donnees), 32)]
    chiffre = ",".join(format(b, "x") for b in blocs)
    print(f"Message chiffré : {chiffre[:60]}{'...' if len(chiffre) > 60 else ''}")
    return session.envoyer(SecureProtocol.create_message("RSA", "None", "", "", chiffre))


def menu_sha256(session, message):
    h = hash_sha256(message)
    print(f"Hash SHA-256 : {h}")
    envoye = message
    if input("Simuler une modification du message en route ? (o/N) : ").strip().lower() == "o":
        envoye = message + " (modifié)"
    payload = SecureProtocol.create_message("SHA256", "None", "", "", h, message=envoye)
    return session.envoyer(payload)


def menu_diffie_hellman(session, message):
    print("Paramètres publics (Entrée = valeurs par défaut p=23, g=5)")
    p = int(demander("Nombre premier p : ", lambda s: s == "" or est_entier(s)) or 23)
    g = int(demander("Générateur g : ", lambda s: s == "" or est_entier(s)) or 5)
    if p < 5 or not dh.est_premier(p):
        return {"status": "ERROR", "message": "p doit être un nombre premier >= 5"}
    if not dh.est_racine_primitive(g, p):
        return {"status": "ERROR", "message": "g n'est pas un générateur valide pour ce p"}

    rep = session.envoyer(SecureProtocol.create_message("DH_INIT", "None", "", "", "", p=p, g=g))
    if rep.get("status") != "SUCCESS":
        return rep
    B = int(rep["B"])
    a = dh.generer_secret(p)
    A = dh.cle_publique(g, a, p)
    secret = dh.cle_partagee(B, a, p)
    print(f"Mon secret a = {a}, ma clé publique A = {A}, clé publique du serveur B = {B}")
    print(f"Secret commun calculé : {secret}")

    cle_aes = dh.deriver_cle_aes(secret)
    chiffre, iv = aes_encrypt_cbc(message, cle_aes)
    print(f"Message chiffré : {chiffre.hex()}")
    payload = SecureProtocol.create_message("DiffieHellman", "CBC", "", iv.hex(), chiffre.hex(), A=A)
    return session.envoyer(payload)


def menu_signature(session, message):
    print("Génération d'une paire de clés RSA 2048 bits (quelques secondes)...")
    cle_privee, cle_publique = signature.generer_cles()
    sig = signature.signer_message(message, cle_privee)
    print(f"Signature : {sig.hex()[:60]}...")
    envoye = message
    if input("Simuler une modification du message en route ? (o/N) : ").strip().lower() == "o":
        envoye = message + " (modifié)"
    payload = SecureProtocol.create_message(
        "Signature", "None", cle_publique.export_key().decode(), "", sig.hex(), message=envoye)
    return session.envoyer(payload)


ALGOS = {
    "1": ("Caesar", menu_caesar),
    "2": ("Vigenère", menu_vigenere),
    "3": ("Playfair", menu_playfair),
    "4": ("AES (ECB / CBC / CTR)", menu_aes),
    "5": ("RSA", menu_rsa),
    "6": ("Hash SHA-256", menu_sha256),
    "7": ("Diffie-Hellman (+ AES)", menu_diffie_hellman),
    "8": ("Signature RSA", menu_signature),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    try:
        session = Session(args.host, args.port)
    except OSError:
        print("Impossible de se connecter au serveur.")
        print("Lance d'abord le serveur dans un autre terminal : python network/server.py")
        return

    try:
        print("=== Choix de l'algorithme ===")
        for numero, (nom, _) in ALGOS.items():
            print(f"{numero} - {nom}")
        choix = demander("Ton choix : ", lambda s: s.strip() in ALGOS,
                         "Choix invalide, tape un numéro de la liste.").strip()
        nom, fonction = ALGOS[choix]
        message = input("Message à envoyer : ")

        reponse = fonction(session, message)

        print("\n=== Réponse du serveur ===")
        print(f"Statut  : {reponse.get('status')}")
        print(f"Message : {reponse.get('message')}")
        if "decrypted" in reponse:
            print(f"Déchiffré par le serveur : {reponse['decrypted']}")
    except (ConnectionError, OSError) as e:
        print(f"Erreur de connexion : {e}")
    except KeyboardInterrupt:
        print("\nAnnulé.")
    finally:
        session.fermer()


if __name__ == "__main__":
    main()
