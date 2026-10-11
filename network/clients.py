import os
import socket
import sys
import json
import argparse

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RACINE not in sys.path:
    sys.path.insert(0, RACINE)

from network.protocol import SecureProtocol

def send_encrypted_message(host, port, algo, mode, key, iv, ciphertext):
    payload = SecureProtocol.create_message(algo, mode, key, iv, ciphertext)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        sock.sendall((payload + "\n").encode('utf-8'))

        response = sock.recv(4096).decode('utf-8')
        print(f"Réponse : {response}")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--algo", default="Caesar")
    parser.add_argument("--mode", default="None")
    parser.add_argument("--key", default="3")
    parser.add_argument("--iv", default="")
    parser.add_argument("--ciphertext", default="KHOOR")
    args = parser.parse_args()

    send_encrypted_message(args.host, args.port, args.algo, args.mode, args.key, args.iv, args.ciphertext)
