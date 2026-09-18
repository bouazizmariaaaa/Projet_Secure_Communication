import socket
import json
import argparse

def send_payload(host, port, payload):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
       
        json_data = json.dumps(payload)
        client_socket.sendall(json_data.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
      
    except ConnectionRefusedError:
        print("[-] Impossible de se connecter au serveur. Vérifiez qu'il est bien démarré.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client de communication sécurisée")
    parser.add_argument("--host", default="localhost", help="Adresse IP du serveur")
    parser.add_argument("--port", type=int, default=5000, help="Port du serveur")
    args = parser.parse_args()

    payload = {
        "algorithm": "Caesar",
        "mode": "None",
        "key": "3",
        "iv": "",
        "ciphertext": "KHOOR" 
    }

    send_payload(args.host, args.port, payload)
