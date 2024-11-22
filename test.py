import os
import json
from cryptography.fernet import Fernet
from getpass import getpass
import secrets
import string

# Pfade für Dateien
USER_DB_PFAD = "benutzer.json"
PASSWORT_DB_PFAD = "passwoerter.json"
SCHLUESSEL_DATEI = "schluessel.key"

# Verschlüsselungsschlüssel laden oder erstellen
def lade_schluessel():
    if not os.path.exists(SCHLUESSEL_DATEI):
        schluessel = Fernet.generate_key()
        with open(SCHLUESSEL_DATEI, "wb") as datei:
            datei.write(schluessel)
    else:
        with open(SCHLUESSEL_DATEI, "rb") as datei:
            schluessel = datei.read()
    return schluessel

# Initialisiere Verschlüsselung
schluessel = lade_schluessel()
cipher = Fernet(schluessel)

# Benutzer-Datenbank laden oder erstellen
def lade_benutzer_db():
    if not os.path.exists(USER_DB_PFAD):
        with open(USER_DB_PFAD, "w") as datei:
            json.dump({}, datei)
    with open(USER_DB_PFAD, "r") as datei:
        return json.load(datei)

def speichere_benutzer_db(daten):
    with open(USER_DB_PFAD, "w") as datei:
        json.dump(daten, datei)

# Passwort-Datenbank laden oder erstellen
def lade_passwort_db():
    if not os.path.exists(PASSWORT_DB_PFAD):
        with open(PASSWORT_DB_PFAD, "w") as datei:
            json.dump({}, datei)
    with open(PASSWORT_DB_PFAD, "r") as datei:
        return json.load(datei)

def speichere_passwort_db(daten):
    with open(PASSWORT_DB_PFAD, "w") as datei:
        json.dump(daten, datei)

# Benutzerregistrierung
def registrieren():
    benutzer_db = lade_benutzer_db()
    print("=== Registrierung ===")
    while True:
        benutzername = input("Benutzername: ").strip()
        if not benutzername:
            print("Der Benutzername darf nicht leer sein.")
            continue
        if benutzername in benutzer_db:
            print("Dieser Benutzername existiert bereits.")
            continue
        break

    while True:
        passwort = getpass("Passwort: ")
        passwort_bestaetigen = getpass("Passwort bestätigen: ")
        if passwort != passwort_bestaetigen:
            print("Passwörter stimmen nicht überein.")
        elif not passwort:
            print("Das Passwort darf nicht leer sein.")
        else:
            break

    benutzer_db[benutzername] = cipher.encrypt(passwort.encode()).decode()
    speichere_benutzer_db(benutzer_db)
    print("Registrierung erfolgreich!")
    return benutzername

# Benutzeranmeldung
def anmelden():
    benutzer_db = lade_benutzer_db()
    print("=== Anmeldung ===")
    while True:
        benutzername = input("Benutzername: ").strip()
        if not benutzername or benutzername not in benutzer_db:
            print("Ungültiger Benutzername.")
            continue
        passwort = getpass("Passwort: ")
        gespeichertes_passwort = cipher.decrypt(benutzer_db[benutzername].encode()).decode()
        if passwort == gespeichertes_passwort:
            print("Anmeldung erfolgreich!")
            return benutzername
        else:
            print("Falsches Passwort.")

# Passwort generieren
def generiere_passwort(laenge=12):
    zeichen = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(zeichen) for _ in range(laenge))

# Passwort speichern
def speichere_passwort(benutzername, seite, benutzer, passwort):
    datenbank = lade_passwort_db()
    if benutzername not in datenbank:
        datenbank[benutzername] = {}
    datenbank[benutzername][seite] = {
        "benutzer": benutzer,
        "passwort": cipher.encrypt(passwort.encode()).decode()
    }
    speichere_passwort_db(datenbank)
    print(f"Passwort für {seite} gespeichert.")

# Passwort abrufen
def abrufen_passwort(benutzername, seite):
    datenbank = lade_passwort_db()
    if benutzername not in datenbank or seite not in datenbank[benutzername]:
        print("Kein Eintrag gefunden.")
        return
    eintrag = datenbank[benutzername][seite]
    print(f"Benutzer: {eintrag['benutzer']}")
    print(f"Passwort: {cipher.decrypt(eintrag['passwort'].encode()).decode()}")

# Hauptmenü
def hauptmenue(benutzername):
    while True:
        print("\n=== Passwortmanager Menü ===")
        print("1. Passwort speichern")
        print("2. Passwort abrufen")
        print("3. Passwort generieren")
        print("4. Abmelden")
        auswahl = input("Option wählen: ")
        if auswahl == "1":
            seite = input("Seitenname: ").strip()
            benutzer = input("Benutzername: ").strip()
            passwort = getpass("Passwort (leer lassen für zufälliges): ").strip()
            if not passwort:
                passwort = generiere_passwort()
                print(f"Generiertes Passwort: {passwort}")
            speichere_passwort(benutzername, seite, benutzer, passwort)
        elif auswahl == "2":
            seite = input("Seitenname: ").strip()
            abrufen_passwort(benutzername, seite)
        elif auswahl == "3":
            print(f"Generiertes Passwort: {generiere_passwort(int(input('Länge: ')))}")
        elif auswahl == "4":
            print("Abgemeldet.")
            break
        else:
            print("Ungültige Auswahl.")

# Programmstart
if __name__ == "__main__":
    print("Willkommen im Passwortmanager!")
    while True:
        print("\n1. Registrieren")
        print("2. Anmelden")
        print("3. Beenden")
        auswahl = input("Option wählen: ")
        if auswahl == "1":
            registrieren()
        elif auswahl == "2":
            benutzername = anmelden()
            if benutzername:
                hauptmenue(benutzername)
        elif auswahl == "3":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl.")
