import sys
import time
from os.path import exists
import keyring as kr
import os
from cryptography.hazmat.primitives import hashes, hmac
import re
import secrets
import random


# Erstellung eines/einer Benutzer:in
class Benutzer:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __str__(self):
        # Rückgabe einer String-Repräsentation des Benutzers, einschließlich des verschlüsselten Passworts
        return f"{[self.name, password_encryption(self.password+self.name)]}"

# Verschlüsselt das Passwort und Gib einen Hashwert in hexadezimal raus.
# Verwendet HMAC mit einem sicher generierten Schlüssel, der im Schlüsselbund(keyring) des Systems gespeichert ist
def password_encryption(entered_password):

    if not os.path.exists("users_db.txt"): # Überprüft, ob die Datei "users_db.txt" existiert
        key = os.urandom(32) # Generieren eines zufälligen 32-Byte-Schlüssels
        kr.set_password("Secret","Key",key) # Speichert der Schüssel in der Bibliothek "keyring"

    # Abrufen des generierten Schlüssels aus keyring
    generated_key = kr.get_password("Secret", "Key").encode("ASCII")
    entry_toByte = entered_password.encode("ASCII")

    # Erstellen eines HMAC-Objekts mit SHA-256
    h = hmac.HMAC(generated_key, hashes.SHA256())
    h.update(entry_toByte)
    signature = h.finalize()

    return signature.hex() # Gib die hexadezimale Darstellung der Signatur zurück.

# Gib eine Liste von allen Benutzern oder Passwörtern abhängig von dem index_to_fetch aus:
#  0 = Benutzer
#  1 = Passwörter
def fetch_data(index_to_fetch):
    file_table = []
    users_data_table = []
    with open("users_db.txt", "r") as f:
        for line in f.readlines():
            file_table.append(line.strip("[\n]").split(","))
    for i in range(0, len(file_table)):
        result = str(file_table[i][index_to_fetch]).split("'")[1]
        users_data_table.append(result)
    return users_data_table



# Fügt den Benutzer in der Datenbank hinzu
def post_data(user_obj):
    # Überprüft, ob die Datei existiert
    if not os.path.exists("users_db.txt"):
        with open("users_db.txt", "w"):
            pass
    # Anhängen des neuen Benutzers zur Datei
    with open("users_db.txt", "a") as f:
        f.write(f"{user_obj}\n")

# Überprüft, ob der Benutzername existiert
def username_verification(username_entered):
    if username_entered in fetch_data(0): # Prüf, ob der Benutzername in der Liste der Benutzer enthalten ist
        return True
    else:
        return False

# Überprüft das Passwort gegen die gespeicherte Hashes
def password_verification(password_entered):
    hashed_password = password_encryption(password_entered)
    if hashed_password in fetch_data(1): # Vergleich des gehashten Passworts mit gespeicherten Hashes
        return True
    else:
        return False


#Fragt, ob das Passwort automatisch oder selbst generiert sein soll
def choice():
    choice_input = input("Möchten Sie ein Passwort generieren lassen. J=Ja/N=Nein: ").strip().upper()
    match choice_input:
        case "J":
            # Generieren und Anzeigen eines zufälligen Passworts
            user_password = generate_password()
            print(f"Ihr generiertes Passwort lautet: {user_password}")
            time.sleep(5)
            return  user_password  # Generiertes Passwort zurückgeben
        case "N":
            while True:
                user_password = input("Eigenes Benutzerpasswort: ")
                check = password_validation(user_password) # # Überprüf das Passwort.
                if check:
                    return  user_password

        # Ungültige Eingaben behandeln
        case _:
            print("Ungültige Eingabe.")
            print("--------------------------------------------------------------------------")
            time.sleep(1)
            choice()


# Registriert einen neuen Benutzer
def registration():
    while True:
        print("\n--- Registrierung ---")
        username = input("Benutzername: ")
        if username_validation(username):
            break

    if os.path.exists("users_db.txt"):
        if not username_verification(username.strip()): # Stell sicher, dass der Benutzername eindeutig ist.
            while True:
                user_password = choice() # Frag den Benutzer nach seinem Passwort
                check = password_validation(user_password) # Überprüf das Passwort.
                if check:
                    break
            user_obj = Benutzer(username, user_password)
            post_data(user_obj) # Speichert den neuen Benutzer in der Datenbank.
            print("Sie wurden erfolgreich registriert.")
            audit_log(username, "registriert und eingeloggt")
            time.sleep(1)
            login_options(username) # Zeig die Login-Optionen an
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

#Loggt einen Benutzer ein
def login():
    print("\n--- Einloggen ---")
    attempts = 0
    trial = 4
    username = input("Benutzername: ")
    user_password = input("Benutzerpasswort: ")
    if  os.path.exists("users_db.txt"):
        if username_verification(username) and password_verification(user_password+username) and not account_blocked(username):
            if two_factor_auth_console():
                audit_log(username,"eingeloggt")
                time.sleep(1)
                login_options(username)
        elif username_verification(username):
            # Umgang mit wiederholten Passwortfehlern und Kontosperre
            if not account_blocked(username):
                while True:
                    attempts = attempts + 1
                    trial = trial - 1
                    print("Das eingegebene Passwort ist falsch.\nBitte versuchen sie es erneut.")
                    audit_log(username,"Passwort fehlgeschlagen")
                    print(f"Versuche übrig: {trial}")
                    time.sleep(1)
                    user_password = input("Benutzerpasswort: ")
                    if attempts >= 3:
                        print("Dieses Konto wurde gesperrt.\nBitte wenden Sie an den/die Administrator:in, um es zu entsperren.")
                        blocked_account(username)
                        audit_log(username, "gesperrt")
                        print("--------------------------------------------------------------------------\n")
                        time.sleep(2)
                        main_menu()
                        break

                    if password_verification(user_password+username):
                        if two_factor_auth_console():
                            audit_log(username, "eingeloggt")
                            time.sleep(1)
                            login_options(username)
                        break
            else:
                account_blocked(username)

        else:
            print("Dieser Benutzer existiert nicht.\nSie müssen sich zuerst anmelden .")
            print("--------------------------------------------------------------------------")
            time.sleep(1)
            registration()
    else:
        print("Dieser Benutzer existiert nicht.\nSie müssen sich zuerst registrieren .")
        print("--------------------------------------------------------------------------")
        time.sleep(1)
        registration()


# Validiert den Benutzernamen gegen festgelegte Kriterien
def username_validation(username):
    # Überprüft, ob der Benutzername mit einem Buchstaben beginnt und nur zulässige Zeichen enthält
    pattern = "^[A-Za-z][A-Za-z0-9_]{3,15}$"
    if re.search(pattern,username):
        return True
    else:
        # Detaillierte Validierungsfehler für unterschiedliche Längen und Zeichen
        match(len(username)):
            case l if len(username.strip(" ")) == 0: print("Ein Leerer Benutzername ist nicht erlaubt.")
            case l if l < 4: print("Der Benutzername muss mindestens 4 Zeichen enthalten.")
            case l if l > 16: print("Der Benutzername muss maximal 16 Zeichen enthalten.")
            case l if re.search("^[0-9_]",username): print("Der Benutzername kann nicht mit einer Ziffer oder einem Unterstrich anfangen.")
            case _: print("Sonderzeichen (außer: _(Unterstrich)) , Leerzeichen und Sonderbuchstaben(ä,ü,ö,ß usw) sind nicht erlaubt")
        return False



# Prüft, ob ein Passwort schwach, mittel oder stark ist
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
            print(f"Passwortstärke: Passwort erfüllt alle Anforderungen.")
            time.sleep(1)
            return True
        else:
            print("Sonderzeichen (außer: _(Unterstrich)) , Leerzeichen und Sonderbuchstaben(ä,ü,ö,ß usw) sind nicht erlaubt")
            return False
    except ValueError:
        print("Oops ein unerwarteter Fehler ist aufgetreten")
        time.sleep(1)
        main_menu()


# Ändert Passwörter
def change_password(username):
    while True:
        new_password = choice() # Fragt nach einem neuen Passwort (vom Benutzer oder automatisch generiert)
        check = password_validation(new_password) # Validiert das neue Passwort
        if check:
            break
    if username in fetch_data(0): # Überprüft, ob der Benutzername existiert
        index_of_userFound = fetch_data(0).index(username)  # Index des Benutzers im Datensatz
        old_hashed_password = fetch_data(1)[index_of_userFound]  # Altes gehashtes Passwort holen
        new_hashed_password = password_encryption(new_password+username)  # Verschlüsselt das neues Passwort
        old_dataObject = f"{[username, old_hashed_password]}"

        # Aktualisiert die Datenbank, indem das alte Passwort durch das neue ersetzt wird
        try:
            with open("users_db.txt", "r") as fr:
                lines = fr.readlines()

                with open("users_db.txt", "w") as fw:
                    for line in lines:
                        if old_dataObject != line.strip("\n"):
                            fw.write(line)
                with open("users_db.txt", "a") as fa:
                    fa.write(f"{[username, new_hashed_password]}\n")
                    audit_log(username, "Passwort geaendert")  # Protokolliert die Passwortänderung
        except ValueError:
            return "Oops ein Problem ist aufgetreten"




#Generiert ein zufälliges Passwort
def generate_password():
    # Liste der Zeichen, die im Passwort verwendet werden sollen
    zeichen = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz!@#$%^&*()-_=+{};:,<.>0123456789"
    pw = ""
    length = secrets.choice(range(12, 21)) # Wählt eine zufällige Länge für das Passwort (12–20 Zeichen)
    for _ in range(length):
        pw = pw+secrets.choice(zeichen) # Baut das Passwort zeichenweise auf
    return  pw

#Haupseite-Optionen
def main_menu():
    print("Willkommen im Passwort-Manager für HSNR Secure Corp!")
    print("Wählen Sie eine Option")
    print("1.Einloggen")
    print("2.Registrieren")
    print("Q = Quit")
    user_choice = input()

    # Menüoptionen basierend auf Benutzereingaben
    match user_choice.upper():
        case "1": login()
        case "2": registration()
        case "Q":
            print("Wir wünschen Ihnen noch einen schönen Tag! :)")
            sys.exit()
        case _:
            print("Bitte treffen Sie eine gültige Auswahl")
            print("--------------------------------------------------------------------------")
            time.sleep(2)
            main_menu()

# Zeigt die Funktionalitäten, die einem Benutzer nach dem Einloggen zur Verfügung stehen
def login_options(username):
    print("--------------------------------------------------------------------------")
    print(f"\n--- Willkommen {username} ---")
    print("Bitte wählen Sie aus zwischen")
    print("1. Mein Passwort ändern")
    print("Oder")
    print("2. Abmelden")
    user_choice = input()


    match user_choice:
        case "1":
            change_password(username) # Ruft die Passwortänderungsfunktion auf
            print("Ihr Passwort wurde erfolgreich geändert und gespeichert.")
            time.sleep(2)
            login_options(username)
        case "2":
            audit_log(username, "ausgeloggt") # Protokolliert das Ausloggen
            print("Wir wünschen Ihnen noch einen schönen Tag! :)")
            print("--------------------------------------------------------------------------")
            main_menu()
        case _:
            print("Bitte treffen Sie eine gültige Auswahl")
            print("--------------------------------------------------------------------------")
            time.sleep(2)
            login_options(username)


# Funktion: Zufälligen Code generieren
def generate_otp():
    return random.randint(100000, 999999)  # Generiert einen 6-stelligen zufälligen Code

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
        print("Der Code ist abgelaufen. Bitte versuchen Sie, sich noch einmal einzuloggen.")
        print("--------------------------------------------------------------------------")
        time.sleep(3)
        main_menu()
        return False

    # Codevalidierung
    if user_code == otp:
        print("2FA erfolgreich! Zugriff gewährt.")
        return True
    else:
        print("Ungültiger Code. Zugriff verweigert.")
        print("--------------------------------------------------------------------------")
        time.sleep(3)
        main_menu()
        return False

# Speichert jede Aktivität des Benutzers wie Ein- und Ausloggen, Kontosperrung und Passwortänderung in einer Datei
def audit_log(user_name,change):
    if not os.path.exists("log.txt"):
        with open(f"log.txt", "w") :
            pass
    # Nimmt die aktuelle Zeit, den Benutzernamen und die ausgeführte Aktionen auf
    with open("log.txt", "a") as f:
        f.write(f"{time.ctime(time.time())}          {user_name}          {change}.\n")


# Überprüft, ob ein Benutzerkonto gesperrt ist oder nicht
def account_blocked(username):
    if os.path.exists("blocked_accounts.txt"):
        arr = []
        # Liest gesperrte Konten aus der Datei
        with open(f"blocked_accounts.txt", "r") as fr:
            for name in fr.readlines():
                arr.append(name.strip("[\n]"))
        if username in arr:
            # Gib eine Nachricht aus, wenn das Konto gesperrt ist
            print("Dieses Konto ist gesperrt.\nBitte wenden Sie an den/die Administrator:in, um es zu entsperren.")
            print("--------------------------------------------------\n")
            time.sleep(2)
            main_menu()
            return True
        else:
            return False
    else:
        return False

# Füg ein gesperrtes Konto in einer Datei hinzu
def blocked_account(username):
    if not os.path.exists("blocked_accounts.txt"):
        with open(f"blocked_accounts.txt", "w") as f:
            f.write(f"{username}\n")
    with open("blocked_accounts.txt", "a") as f:
        f.write(f"{username}\n")

# Startet das Programm mit dem Hauptmenü
if __name__ == '__main__':
    main_menu()

