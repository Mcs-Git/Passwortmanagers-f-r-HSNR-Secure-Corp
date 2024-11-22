import keyring as kr
import os
import bcrypt as end_encryption
from cryptography.hazmat.primitives import hashes, hmac

def password_encryption(entered_password):
    if not os.path.exists("users_db.txt"):
        key = os.urandom(256)
        kr.set_password("Secret","Key",key)
        print(type(key))
    generated_key = kr.get_password("Secret", "Key").encode("ASCII")
    print("Password", type(generated_key))
    h = hmac.HMAC(generated_key, hashes.SHA256())
    entry_toByte = entered_password.encode("ASCII")
    h.update(entry_toByte)
    signature = h.finalize()

    password_hashed = end_encryption.hashpw(signature, end_encryption.gensalt())
    print("Signature3: ", password_hashed.hex())
    return password_hashed


#Erstellung eines/einer Benutzer:in
class Benutzer:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __str__(self):
        return f"{[self.name, password_encryption(self.password)]}"



#print(password_encryption('Mc123'))
#var = "Hey".encode("ASCII")
#print(var)
user_name = input("Benutzername: ")
user_password = input("Benutzerpasswort: ")
user_obj = Benutzer(user_name, user_password)
print(user_obj)

#Überprüft, ob die Datei existiert
if not os.path.exists("users_db.txt"):
    with open("users_db.txt", "w"):
        pass

with open("users_db.txt", "a") as f:
    f.write(f"{user_obj}\n")

#b'\x90\x03\x01z\x984A\x7f\xb5\xbf\xcb}\xe7l\xd9\x9e0\xf79jNi`\x89\xcc\xef\xbc\x1e)=\xb61\x97A\x01\x1a\xdb\x10\xf5`Mu\xea\xd5\xceE\x91\xd6`\xed-\x83;bu\xb7\xb3\x04\x90|\x96\x9d\xaf$\x88\xea\xd6gHr\x92\x12\x88\x8c\x80i]6\xf9{\xe0mJ\xfdEZ\x1b\xa1\x11\x92\xd90D\xb3nR\xd4$x\x1d\xd6\xb8w`3"\'Y\x04\\\x1b\x94\xc9Nb\x83%o\x06W\x117N\x82\x8d\xb6\x85-\xfd\xb8\xca\xe5\x8e\xd6\x12\xb6\x90\xb1\xd
