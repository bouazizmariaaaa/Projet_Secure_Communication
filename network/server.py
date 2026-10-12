import argparse
import json
import os
import socket
import sys
import threading
 
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RACINE not in sys.path:
    sys.path.insert(0, RACINE)
 
from Crypto.PublicKey import RSA as CryptoRSA
 
from network.protocol import SecureProtocol
from algorithms.classical.caesar import caesar_decrypt
from algorithms.classical.vigenere import vigenere_decrypt
from algorithms.classical.playfair import playfair_decrypt
from algorithms.symmetric.modes import aes_decrypt_cbc, aes_decrypt_ecb, aes_decrypt_ctr
from algorithms.asymmetric import rsa
from algorithms.asymmetric import diffie_hellman as dh
from algorithms.hash.sha256 import verify_sha256
from algorithms.hash import signature
 
P_MAX_DEMO = 100_000
 
 
def dechiffrer_aes(mode, cle, iv, chiffre):
    if mode == "ECB":
        return aes_decrypt_ecb(chiffre, cle)
    if mode == "CBC":
        return aes_decrypt_cbc(chiffre, cle, iv)
    if mode == "CTR":
        return aes_decrypt_ctr(chiffre, cle, iv)
    raise ValueError(f"Mode AES inconnu : {mode}")
 
 
def erreur(texte):
    return {"status": "ERROR", "message": texte}
 
 
def traiter_message(msg, etat):
    algo = str(msg.get("algorithm", "")).lower()
    mode = str(msg.get("mode", "None")).upper()
    cle = msg.get("key", "")
    chiffre = msg.get("ciphertext", "")
 
    if algo == "caesar":
        clair = caesar_decrypt(chiffre, int(cle))
 
    elif algo == "vigenere":
        clair = vigenere_decrypt(chiffre, str(cle))
 
    elif algo == "playfair":
        clair = playfair_decrypt(chiffre, str(cle))
 
    elif algo == "aes":
        clair = dechiffrer_aes(
            mode,
            bytes.fromhex(cle),
            bytes.fromhex(msg.get("iv", "")),
            bytes.fromhex(chiffre),
        )
 
    elif algo == "rsa_pubkey":
        e, n = etat["rsa_pub"]
        return {"status": "SUCCESS", "message": "Clé publique RSA du serveur",
                "e": str(e), "n": str(n)}
 
    elif algo == "rsa":
        morceaux = []
        for bloc in chiffre.split(","):
            if bloc:
                m = rsa.dechiffrer(int(bloc, 16), etat["rsa_priv"])
                morceaux.append(m.to_bytes((m.bit_length() + 7) // 8, "big"))
        clair = b"".join(morceaux).decode("utf-8")
 
    elif algo == "sha256":
        message = msg.get("message", "")
        if verify_sha256(message, chiffre):
            print(f"    Hash valide, message intact : {message}")
            return {"status": "SUCCESS", "message": "Hash valide : le message est intact",
                    "decrypted": message}
        print("    Hash INVALIDE : le message a été modifié")
        return erreur("Hash invalide : le message a été modifié")
 
    elif algo == "signature":
        message = msg.get("message", "")
        cle_pub = CryptoRSA.import_key(cle)
        if signature.verifier_signature(message, bytes.fromhex(chiffre), cle_pub):
            print(f"    Signature valide, message authentique : {message}")
            return {"status": "SUCCESS", "message": "Signature valide : message authentique",
                    "decrypted": message}
        print("    Signature INVALIDE")
        return erreur("Signature invalide : message altéré ou fausse signature")
 
    elif algo == "dh_init":
        p, g = int(msg["p"]), int(msg["g"])
        if p < 5 or p > P_MAX_DEMO or not dh.est_premier(p):
            return erreur(f"p doit être un nombre premier entre 5 et {P_MAX_DEMO}")
        if not dh.est_racine_primitive(g, p):
            return erreur("g n'est pas un générateur valide pour ce p")
        b = dh.generer_secret(p)
        etat["dh"] = (p, g, b)
        print(f"    Diffie-Hellman : p={p}, g={g} acceptés (le secret b reste sur le serveur)")
        return {"status": "SUCCESS", "message": "Paramètres Diffie-Hellman acceptés",
                "B": str(dh.cle_publique(g, b, p))}
 
    elif algo == "diffiehellman":
        if "dh" not in etat:
            return erreur("Envoie d'abord les paramètres (DH_INIT)")
        p, g, b = etat["dh"]
        A = int(msg["A"])
        if not 1 < A < p:
            return erreur("Clé publique A invalide")
        cle_aes = dh.deriver_cle_aes(dh.cle_partagee(A, b, p))
        clair = aes_decrypt_cbc(bytes.fromhex(chiffre), cle_aes, bytes.fromhex(msg["iv"]))
 
    else:
        return erreur(f"Algorithme inconnu : {msg.get('algorithm')}")
 
    print(f"    Message déchiffré : {clair}")
    return {"status": "SUCCESS", "message": "Message reçu et déchiffré", "decrypted": clair}
 
 
def lire_messages(sock):
    decodeur = json.JSONDecoder()
    tampon = ""
    while True:
        donnees = sock.recv(4096)
        if not donnees:
            return
        tampon += donnees.decode("utf-8", errors="replace")
        while True:
            tampon = tampon.lstrip()
            if not tampon:
                break
            try:
                objet, fin = decodeur.raw_decode(tampon)
            except json.JSONDecodeError:
                if "\n" in tampon:
                    tampon = tampon.split("\n", 1)[1]
                    yield None
                    continue
                break
            tampon = tampon[fin:]
            yield objet if isinstance(objet, dict) else None
 
 
def gerer_client(client_socket, addr, cles_rsa):
    print(f"[+] Connexion reçue de {addr}")
    etat = {"rsa_pub": cles_rsa[0], "rsa_priv": cles_rsa[1]}
    try:
        for msg in lire_messages(client_socket):
            if msg is None:
                reponse = erreur("JSON invalide")
            else:
                print(f"[>] Message reçu ({msg.get('algorithm')}) :")
                print(json.dumps(msg, indent=4, ensure_ascii=False))
                try:
                    reponse = traiter_message(msg, etat)
                except Exception as e:
                    reponse = erreur(f"Erreur de traitement : {e}")
                    print(f"    {reponse['message']}")
            client_socket.sendall((json.dumps(reponse) + "\n").encode("utf-8"))
    except (ConnectionError, OSError):
        pass
    finally:
        client_socket.close()
        print(f"[-] Connexion fermée ({addr})")
 
 
def start_server(host, port):
    print("[*] Génération des clés RSA du serveur...")
    cles_rsa = rsa.generer_cles()
 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[+] Serveur en écoute sur {host}:{port}... (Ctrl+C pour arrêter)")
 
    try:
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=gerer_client, args=(client_socket, addr, cles_rsa),
                             daemon=True).start()
    except KeyboardInterrupt:
        print("\n[*] Arrêt du serveur.")
    finally:
        server_socket.close()
 
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
 
    start_server(args.host, args.port)
 
Claude a terminé sa réponse.
