import json

class SecureProtocol:
    @staticmethod
    def create_message(algorithm, mode, key, iv, ciphertext, **extra):
        data = {
            "algorithm": algorithm,
            "mode": mode,
            "key": key,
            "iv": iv,
            "ciphertext": ciphertext
        }
        data.update(extra)
        return json.dumps(data)

    @staticmethod
    def parse_message(json_str):
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
