import json 
def create_message (algorithm, ciphertext,key,mode:None, iv:None):
  list = {
        "algorithm": algorithm,
        "mode": mode,
        "key": key,
        "iv": iv,
        "ciphertext": ciphertext
    }
  return json.dumps(list)
def decrypte_message (json_message):
  return json.loads(json_message)
  
  
