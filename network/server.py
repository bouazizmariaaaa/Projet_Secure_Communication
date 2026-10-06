import socket
import json
import argparse
from protocol import SecureProtocol

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[+] Serveur en écoute sur {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Connexion reçue de {addr}")
        
        data = client_socket.recv(4096).decode('utf-8')
        if data:
            msg = SecureProtocol.parse_message(data)
            if msg:
                print(json.dumps(msg, indent=4))
                response = {"status": "SUCCESS", "message": "Message reçu"}
            else:
                response = {"status": "ERROR", "message": "JSON invalide"}
            
            client_socket.sendall(json.dumps(response).encode('utf-8'))
        
        client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    start_server(args.host, args.port)
