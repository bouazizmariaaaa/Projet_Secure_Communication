import socket
import json
import argparse

def process_message(data_json):
  
    algorithm = data_json.get("algorithm")
    ciphertext = data_json.get("ciphertext")
    key = data_json.get("key")
    decrypted_text = ciphertext
    return decrypted_text

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(4096).decode('utf-8')
            
            if data:
                try:
                    payload = json.loads(data)
                    print(f"[<-] Données JSON reçues : {payload}")
                    decrypted_msg = process_message(payload)
                    print(f"[✓] Message déchiffré : {decrypted_msg}")

                    response = {"status": "SUCCESS", "message": "Message reçu et traité."}
                except json.JSONDecodeError:
                    print("[-] Erreur : Format JSON invalide.")
                    response = {"status": "ERROR", "message": "JSON invalide."}

                client_socket.sendall(json.dumps(response).encode('utf-8'))
            client_socket.close()

    except KeyboardInterrupt:
        print("\n[*] Arrêt du serveur.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serveur de communication sécurisée")
    parser.add_argument("--host", default="127.0.0.1", help="Adresse IP d'écoute")
    parser.add_argument("--port", type=int, default=5000, help="Port d'écoute")
    args = parser.parse_args()

    start_server(args.host, args.port)
