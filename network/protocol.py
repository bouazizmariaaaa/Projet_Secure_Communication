import json

class SecureProtocol:
    @staticmethod
    def create_message(algorithm, mode, key, iv, ciphertext):
        return json.dumps({
            "algorithm": algorithm,
            "mode": mode,
            "key": key,
            "iv": iv,
            "ciphertext": ciphertext
        })

    @staticmethod
    def parse_message(json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
