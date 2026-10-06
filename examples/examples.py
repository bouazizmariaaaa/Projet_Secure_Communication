import json
import socket

def caesar_encrypt(plaintext, shift):
    result = ""
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)

def demo_caesar():
    message = "BONJOUR KALI"
    key = 3
    chiffre = caesar_encrypt(message, key)
    dechiffre = caesar_decrypt(chiffre, key)
    
    print(f"Original  : {message}")
    print(f"Chiffré   : {chiffre}")
    print(f"Déchiffré : {dechiffre}")

def demo_protocol():
    payload = {
        "algorithm": "Caesar",
        "mode": "None",
        "key": "3",
        "iv": "",
        "ciphertext": "ERQMRXU NDOL"
    }
    json_str = json.dumps(payload, indent=4)
    print("Structure JSON :")
    print(json_str)

def demo_replay_attack(host="localhost", port=5000):
    captured_json = '{"algorithm": "Caesar", "mode": "None", "key": "3", "iv": "", "ciphertext": "ERQMRXU NDOL"}'
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.sendall(captured_json.encode('utf-8'))
        
        response = sock.recv(4096).decode('utf-8')
        print(f"Réponse : {response}")
        sock.close()
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    demo_caesar()
    demo_protocol()
    demo_replay_attack()
