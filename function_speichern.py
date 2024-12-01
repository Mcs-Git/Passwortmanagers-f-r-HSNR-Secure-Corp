import time
from os import times

import keyring as kr
import os
from cryptography.hazmat.primitives import hashes, hmac
import re
import secrets
import random


#Erstellung eines/einer Benutzer:in
class Benutzer:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __str__(self):
        return f"{[self.name, password_encryption(self.password+self.name)]}"

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

#Gib eine Liste von allen Benutzern oder Passwörtern abhängig von dem index_to_fetch aus:
#  0 = Benutzer
#  1 = Passwörter
def fetch_data(index_to_fetch):
    file_table = []
    hash_users_table = []
    with open("users_db.txt", "r") as f:
        for line in f.readlines():
            file_table.append(line.strip("[\n]").split(","))

    for i in range(0, len(file_table)):
        hash_password = str(file_table[i][index_to_fetch]).split("'")[1]
        hash_users_table.append(hash_password)
    return hash_users_table

#Nimmt den Bneutzer in der Datenbank auf.
def post_data(user_obj):
    # Überprüft, ob die Datei existiert
    if not os.path.exists("users_db.txt"):
        with open("users_db.txt", "w"):
            pass
    # Fügt den neuen Benutzer zur Datei hinzu.
    with open("users_db.txt", "a") as f:
        f.write(f"{user_obj}\n")

#Überprüft den Benutzername in der Datei(users_db.txt)
def username_verification(username_entered):
    if username_entered in fetch_data(0):
        return True
    else:
        return False

#Überprüft das Benutzerpasswort in der Datei.name = name
        self.password = password(users_db.txt)
def password_verification(password_entered):
    hashed_password = password_encryption(password_entered)
    if hashed_password in fetch_data(1):
        return True
    else:
        return False


#Fragt,ob das Passwort automatisch oder selbst generiert sein soll
def choice():
    choice_input = input("Möchten Sie ein Passwort generieren lassen. J=Ja/N=Nein: ").strip().upper()
    match choice_input:
        case "J":
            user_password = generate_password()
            print(f"Ihr generiertes Passwort lautet: {user_password}")
            time.sleep(5)
            return  user_password  # Generiertes Passwort zurückgeben
        case "N":
            while True:
                user_password = input("Eigenes Benutzerpasswort: ")
                check = password_validation(user_password) # Passwortprüfung
                if check:
                    return  user_password
                    break # Passwort ist gültig
                #else: choice()
        case _:
            print("Ungültige Eingabe.")
            print("--------------------------------------------------------------------------")
            time.sleep(1)
            choice()


#Melde einen Benutzer an.
def registration():
    while True:
        print("\n--- Registrierung ---")
        username = input("Benutzername: ")
        if username_validation(username):
            break

    if os.path.exists("users_db.txt"):
        if not username_verification(username.strip()):
            while True:
                user_password = choice()
                check = password_validation(user_password)
                if check:
                    break
            user_obj = Benutzer(username, user_password)
            post_data(user_obj)
            print("Sie wurden erfolgreich registriert.")
            audit_log(username, "registriert und eingeloggt")
            time.sleep(1)
            login_options(username)
        else:
            print("Dieser Benutzername ist bereits vergeben.\nGeben Sie einen anderen ein")
            time.sleep(2)
            registration()
    else:
        user_password = choice()
        user_obj = Benutzer(username, user_password)
        post_data(user_obj)
        print("Sie wurden erfolgreich registriert.")
        audit_log(username, "registriert und eingeloggt")
        time.sleep(1)
        login_options(username)

#Logg einen Benutzer ein
def login():
    print("\n--- Einloggen ---")
    username = input("Benutzername: ")
    user_password = input("Benutzerpasswort: ")
    if  os.path.exists("users_db.txt"):
        if username_verification(username) and password_verification(user_password+username):
            if two_factor_auth_console():
                audit_log(username,"eingeloggt")
                time.sleep(1)
                login_options(username)
        else:
            print("Dieser Benutzer existiert nicht.\nSie müssen sich zuerst anmelden .")
            print("--------------------------------------------------------------------------")
            time.sleep(1)
            registration()
    else:
        print("Dieser Benutzer existiert nicht.\nSie müssen sich zuerst anmelden .")
        print("--------------------------------------------------------------------------")
        time.sleep(1)
        registration()


#Verifiziert,ob der Benutzername gilt oder nicht
def username_validation(username):
    #Beginn mit nur Buchstaben(Groß oder klein), dann besteht aus Buchstaben(Groß oder klein), Ziffern und Unterstrichen(_)
    #Anzahl von Zeichen  ist von 4  bis 16 begrenzt
    pattern = "^[A-Za-z][A-Za-z0-9_]{3,15}$"
    if(re.search(pattern,username)): return True
    else:
        #l = len(username)
        match(len(username)):
            case l if len(username.strip(" ")) == 0: print("Ein Leerer Benutzername ist nicht erlaubt.")
            case l if l < 4: print("Der Benutzername muss mindestens 4 Zeichen enthalten.")
            case l if l > 16: print("Der Benutzername muss maximal 16 Zeichen enthalten.")
            case l if re.search("^[0-9_]",username): print("Der Benutzername kann nicht mit einer Ziffer oder einem Unterstrich anfangen.")
            case _: print("Sonderzeichen (außer: _(Unterstrich)) , Leerzeichen und Sonderbuchstaben(ä,ü,ö,ß usw) sind nicht erlaubt")
        return False

def password_strenght(user_password):
    if len(user_password) < 12:
        print("Schwach: Mindestlänge von 12 Zeichen erforderlich.")
        time.sleep(1)
        return False
    if not any(char.isdigit() for char in user_password):
        print("Mittel: Zahlen fehlen.")
        time.sleep(1)
        return False
    if not any(char.isupper() for char in user_password):
        print("Mittel: Großbuchstaben fehlen.")
        time.sleep(1)
        return False
    if not any(char in "!@#$%^&*()-_=+{};:,<.>%" for char in user_password):
        print("Mittel: Sonderzeichen fehlen.")
        time.sleep(1)
        return False


# Prüft, ob ein Passwort schwach , mittel oder stark ist
def password_validation(user_password):
    pattern = "[A-Za-z0-9!@#$%^&*()-_=+{};:,<.>%]"
    try:
        if re.search(pattern, user_password) and not user_password.isspace():
            if len(user_password.strip()) == 0:
                print("Ein Leeres Passwort ist nicht erlaubt.")
                time.sleep(1)
                return  False

            if len(user_password) < 12:
                print("Schwach: Mindestlänge von 12 Zeichen erforderlich.")
                time.sleep(1)
                return False
            if not any(char.isdigit() for char in user_password):
                print("Mittel: Zahlen fehlen.")
                time.sleep(1)
                return False
            if not any(char.isupper() for char in user_password):
                print("Mittel: Großbuchstaben fehlen.")
                time.sleep(1)
                return False
            if not any(char in "!@#$%^&*()-_=+{};:,<.>%" for char in user_password):
                print("Mittel: Sonderzeichen fehlen.")
                time.sleep(1)
                return False
            print(f"Stark: Passwort erfüllt alle Anforderungen.")
            time.sleep(1)
            return True
        else:
            print("Sonderzeichen (außer: _(Unterstrich)) , Leerzeichen und Sonderbuchstaben(ä,ü,ö,ß usw) sind nicht erlaubt")
            return False
    except Exception:
        print("Oops ein unerwarteter Fehler ist aufgetreten")
        time.sleep(1)
        main_menu()


#Ändert Passwörter
def change_password(username):
    while True:
        new_password = choice()
        #new_password = input("Neue Passwort: ")
        check = password_validation(new_password)
        if check:
            break
    if username in fetch_data(0):
        index_of_userFound = fetch_data(0).index(username)
        old_hashed_password = fetch_data(1)[index_of_userFound]
        new_hashed_password = password_encryption(new_password+username)
        old_dataObject = f"{[username, old_hashed_password]}"
        try:
            with open("users_db.txt", "r") as fr:
                lines = fr.readlines()

                with open("users_db.txt", "w") as fw:
                    for line in lines:
                        if old_dataObject != line.strip("\n"):
                            fw.write(line)
                with open("users_db.txt", "a") as fa:
                    fa.write(f"{[username, new_hashed_password]}\n")
                    audit_log(username, "Passwort geaendert")
        except Exception as e:
            return "Oops ein Problem ist aufgetreten"




#Generiert ein zufälliges Passwort
def generate_password():
    #Liste der Zeichen, die im Passwort verwendet werden sollen
    zeichen = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz!@#$%^&*()-_=+{};:,<.>0123456789"
    pw = ""
    length = secrets.choice(range(12, 21))
    for _ in range(length):
        pw = pw+secrets.choice(zeichen)
    return  pw

def main_menu():
    print("Willkommen im Passwort-Manager für HSNR Secure Corp!")
    print("Wählen Sie eine Option")
    print("1.Einloggen")
    print("2.Registrieren")
    print("Q = Quit")
    choice = input()

    match choice.upper():
        case "1": login()
        case "2": registration()
        case "Q": print("Wir wünschen Ihnen noch einen schönen Tag! :)")
        case _:
            print("Bitte treffen Sie eine gültige Auswahl")
            print("--------------------------------------------------------------------------")
            time.sleep(2)
            main_menu()

def login_options(username):
    print("--------------------------------------------------------------------------")
    print(f"\n--- Willkommen {username} ---")
    print("Bitte wählen Sie aus zwischen")
    print("1. Mein Passwort ändern")
    print("Oder")
    print("2. Abmelden")
    choice = input()
    match choice:
        case "1":
            change_password(username)
            print("Ihr Passwort wurde erfolgreich geändert und gespeichert.")
            time.sleep(2)
            login_options(username)
        case "2":
            audit_log(username, "ausgeloggt")
            print("Wir wünschen Ihnen noch einen schönen Tag! :)")
            print("--------------------------------------------------------------------------")
            main_menu()
        case _:
            print("Bitte treffen Sie eine gültige Auswahl")
            print("--------------------------------------------------------------------------")
            time.sleep(2)
            login_options(username)

# Rotiert Passwörter
def password_rotation_check(user_name):
    # Datei mit Benutzerinformationen einlesen
    if os.path.exists("passwords_db.txt"):
        with open("passwords_db.txt", "r") as f:
            users = f.readlines()

        updated_users = []
        for user_entry in users:
            user_data = eval(user_entry.strip())  # Vorsicht bei eval, besser nur für kontrollierte Umgebungen
            if user_data[0] == user_name:
                erstelldatum = datetime.strptime(user_data[2], "%Y-%m-%d")
                if datetime.now() > erstelldatum + timedelta(minutes=1):
                    print(f"Passwort für Benutzer {user_name} muss geändert werden!")
                    return True
                else:
                    updated_users.append(user_entry)
            else:
                updated_users.append(user_entry)

        # Aktualisierte Benutzer zurückschreiben
        with open("passwords_db.txt", "w") as f:
            f.writelines(updated_users)
    return False



# Funktion: Zufälligen Code generieren
def generate_otp():
    return random.randint(100000, 999999)  # 6-stelliger zufälliger Code

# Funktion: 2FA-Authentifizierung in der Konsole
def two_factor_auth_console():
    otp = generate_otp()
    print("\n--- Zwei Faktor Authentifizierung ---")
    print(f"Ihr Einmalcode lautet: {otp}")
    print("Hinweis: Der Code ist für 30 Sekunden gültig.")

    # Wartezeit und Eingabeaufforderung
    start_time = time.time()
    user_code = int(input("Bitte geben Sie den Einmalcode ein: "))

    # Zeitüberprüfung
    elapsed_time = time.time() - start_time
    if elapsed_time > 30:
        print("Der Code ist abgelaufen. Bitte erneut versuchen.")
        return False

    # Codevalidierung
    if user_code == otp:
        print("2FA erfolgreich! Zugriff gewährt.")
        return True
    else:
        print("Ungültiger Code. Zugriff verweigert.")
        time.sleep(3)
        print("--------------------------------------------------------------------------")
        main_menu()
        return False

def audit_log(user_name,change):
    if not os.path.exists("log.txt"):
        with open(f"log.txt", "w") :
            pass

    with open("log.txt", "a") as f:
        f.write(f"{time.ctime(time.time())}          {user_name}          {change}.\n")


if __name__ == '__main__':
    main_menu()
    #audit_log("Frankel","Ausgeloggt")
    #password_scale = password_strength_check("mcfranjerrrrr3A.")
    #print(password_scale)
    #generate_otp()
    # Hauptprogramm
   #save_password("Mc123")
   #change_password()
   #print(change_password("mc123"))
   #print("['mcfrankel', '314ff953a08144b6532619281f70ba5da2e5472e7845bc42a64741fa331118b8']" == "['mcfrankel', '314ff953a08144b6532619281f70ba5da2e5472e7845bc42a64741fa331118b8']")
    #print(username_validation("än_ßhhnhnghtth"))
    #registration()
    #login()
    #gen()


    #print(password_verification("mc1234567"))

