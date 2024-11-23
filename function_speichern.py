import keyring as kr
import os
from cryptography.hazmat.primitives import hashes, hmac



#Verchlüsselt das Passwort und Gib einen Hashwert in hexadezimal raus.
def password_encryption(entered_password):
    if not os.path.exists("users_db.txt"):
        key = os.urandom(256)
        kr.set_password("Secret","Key",key)
    generated_key = kr.get_password("Secret", "Key").encode("ASCII")
    entry_toByte = entered_password.encode("ASCII")
    h = hmac.HMAC(generated_key, hashes.SHA256())
    h.update(entry_toByte)

    signature = h.finalize()
    return signature.hex()

#Gib eine Liste von allen Benutzern oder Passwörtern abhängig von dem index_to_retrieve aus:
#  0 = Benutzer
#  1 = Passwörter
def retrieve_data(index_to_retrieve):
    file_table = []
    hash_users_table = []
    with open("users_db.txt", "r") as f:
        for line in f.readlines():
            file_table.append(line.strip("[\n]").split(","))

    for i in range(0, len(file_table)):
        hash_password = str(file_table[i][index_to_retrieve]).split("'")[1]
        hash_users_table.append(hash_password)
    return hash_users_table

#Überprüft der Benutzername
def user_verification(username_entered):
    if username_entered in retrieve_data(0):
        return True
    else:
        return False

#Überprüft der Benutzerpasswort
def password_verification(password_entered):
    hashed_password = password_encryption(password_entered)
    if hashed_password in retrieve_data(1):
        return True
    else:
        return False

#Erstellung eines/einer Benutzer:in
class Benutzer:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __str__(self):
        return f"{[self.name, password_encryption(self.password+self.name)]}"

if __name__ == '__main__':
    user_name = input("Benutzername: ")
    user_password = input("Benutzerpasswort: ")
    user_obj = Benutzer(user_name, user_password)
    print(user_obj)


    #Überprüft, ob die Datei existiert
    if not os.path.exists("users_db.txt"):
        with open("users_db.txt", "w"):
            pass
    #Fügt den neuen Benutzer zur Datei hinzu.
    with open("users_db.txt", "a") as f:
        f.write(f"{user_obj}\n")
    result = password_verification("Thomasuser")
    print(result)

