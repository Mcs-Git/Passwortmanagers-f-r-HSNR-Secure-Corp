ALIM, FRANKEL, YASIN PRÄSENTIEREN: DEN  PASSWORTMANAGER FÜR DAS HSNR
Einleitung
 Zweck der Anwendung:
     Der Passwort-Manager wurde entwickelt, um Benutzerkonten sicher zu verwalten. Die Anwendung bietet Funktionen zur Benutzerregistrierung, Passwortverschlüsselung, Zwei-Faktor-Authentifizierung 
    (2FA), Kontosperrung und einem Audit-Log, das sicherheitsrelevante Aktionen dokumentiert. Ziel ist 
    es, die Sicherheit von Benutzerkonten zu gewährleisten und gleichzeitig eine benutzerfreundliche 
    Bedienung in der Konsole zu bieten.
 Zielgruppe:
   Unsere Zielgruppe ist das HSNR und Unternehmen im Allgemeinen, die eine konsolenbasierte,  einfache Lösung für die sichere Passwortverwaltung suchen.
 Systemanforderungen:
   Python-Version: ≥ 3.7
 Erforderliche Bibliotheken:cryptography,keyring,os,secrets,re,time,random and sys 
Installation
 Schritt-für-Schritt-Anleitung (Entwicklungsprozess):
 1. Problemdefinition und Planung
   Wir haben damit begonnen, die Anforderungen für den Passwortmanager zu definieren.
   Die Schlüsselfunktionen wurden festgelegt:
     1. Registrierung und Anmeldung von Benutzern.
     2. Passwortverschlüsselung und Prüfung der Passwortstärke.
     3. Zwei-Faktor-Authentifizierung.
     4. Kontosperrung.
     5. Protokollierung sicherheitsrelevanter Aktionen (Audit-Log).
 2. Auswahl der Technologien und Bibliotheken
   Für die Umsetzung wurden folgende Bibliotheken ausgewählt:
     -cryptography: Zur Passwortverschlüsselung (HMAC-SHA256).
     -keyring: Zum sicheren Speichern von Schlüsseln.
     -re: Für die Validierung von Benutzernamen und Passwörtern.
     -secrets: Zur sicheren Generierung von Passwörtern und Einmalcodes.
     -os: Für Dateioperationen.
     -random: Für die Erstellung von zufälligen Bestätigungscodes.
     -time: Für Countdown-Timer, Zeitstempel und kurze Pausen zur Verbesserung der  Nutzererfahrung.
     -sys:  Für die Beendigung der Programmausführung.
 3. Entwicklung der Kernfunktionen
   1. Benutzerverwaltung:
     Eine Klasse Benutzer wurde implementiert, um Benutzername und ein verschlüsseltes Passwort zu speichern.
     Methoden zur Registrierung (registration) und Anmeldung (login) wurden entwickelt.
   2. Passwortverschlüsselung:
   Eine Funktion password_encryption wurde erstellt, die:
     Passwörter mit einem geheimen Schlüssel kombiniert.
     HMAC-SHA256 verwendet, um einen sicheren Hash zu erzeugen.
   3. Passwortstärkeprüfung:
     Eine Funktion password_validation wurde implementiert, die:
     Passwortkriterien (z. B. Länge, Großbuchstaben, Sonderzeichen) prüft.
     Benutzerfeedback zu schwachen oder unzulässigen Passwörtern gibt.
   4. Zwei-Faktor-Authentifizierung (2FA):
     Eine Methode two_factor_auth_console generiert einen zeitlich begrenzten, zufälligen Code.
     Der Benutzer muss diesen Code eingeben, um Zugri zu erhalten.
   5. Kontosperrung:
     Nach drei fehlgeschlagenen Login-Versuchen wird ein Benutzerkonto automatisch gesperrt.
     Gesperrte Konten werden in einer separaten Datei (blocked_accounts.txt) gespeichert und 
     sind für normale Anmeldungen unzugänglich.
 6. Audit-Log:
   Die Funktion audit_log dokumentiert Aktionen mit Zeitstempel, Benutzername und Aktivität.
 4. Integration der Funktionen
   Die Kernfunktionen wurden in eine Menüstruktur integriert:
     Das Hauptmenü (main_menu) bietet Optionen für Anmeldung, Registrierung und Beenden.
     Nach erfolgreicher Anmeldung zeigt login_options Benutzern zusätzliche Optionen (z. B. Passwort ändern).
 5. Fehlerbehandlung und Sicherheit
   Es wurden mehrere Sicherheitsmaßnahmen implementiert:
     1. Gesperrte Konten: Wenn ein Benutzer dreimal das falsche Passwort eingibt, wird sein Konto gesperrt (blocked_account).
     2. Keine Klartextspeicherung: Passwörter und sensitive Daten werden nur verschlüsselt gespeichert.
     3. Validierung: Eingaben werden mit Regex überprüft, um Sicherheitslücken zu minimieren.
     Für die Benutzerfreundlichkeit wurden hilfreiche Fehlermeldungen und Wiederholungsmöglichkeiten implementiert.
 6. Testen
   Jede Funktion wurde einzeln getestet:
     Passwortprüfung: Testfälle für gültige und ungültige Passwörter.
     Registrierung: Überprüfung, ob neue Benutzer korrekt gespeichert werden.
     2FA: Simulation verschiedener Szenarien (richtiger/falscher Code, Zeitablauf).
     Integrationstests: Das Zusammenspiel aller Funktionen wurde getestet, um sicherzustellen, dass das Programm stabil läuft.
 7. Abschluss und Dokumentation
   Der Code wurde kommentiert, um die Nachvollziehbarkeit zu gewährleisten.
   Eine detaillierte Dokumentation (diese!) wurde erstellt, um Installation, Nutzung und technische Details zu erläutern.
  Benutzerhandbuch
   Funktionsbeschreibung:
     1. Registrierung:
       Benutzer können ein Konto erstellen, indem sie einen Benutzernamen und ein Passwort eingeben.Das Passwort kann selbst erstellt oder automatisch generiert werden.
     2. Passwortprüfung:
       Das Passwort wird anhand von Kriterien wie Länge, Zahlen, Großbuchstaben und  Sonderzeichen geprüft.
     3. Passwortverschlüsselung:
       Passwörter werden mit einem HMAC-SHA256-Algorithmus verschlüsselt und sicher gespeichert.
     4. Zwei-Faktor-Authentifizierung (2FA):
       Beim Login wird ein zeitlich begrenzter 6-stelliger Code in der Konsole angezeigt, den der Benutzer eingeben muss.
     5. Kontosperrung:
       Nach drei fehlgeschlagenen Login-Versuchen wird ein Benutzerkonto automatisch gesperrt.
     6. Audit-Log:
       Alle sicherheitsrelevanten Aktionen (z. B. Login, Passwortänderung, Kontosperrung) werden in einer Log-Datei gespeichert.
  Bedienoberfläche:
    Das Programm ist vollständig konsolenbasiert und bietet ein Hauptmenü:
     1: Einloggen
     2: Registrieren
     Q: Beenden
  Technische Dokumentation
   Architektur:
     Konsolenbasiertes System ohne komplexe Softwarearchitektur.
   Funktionale Aufteilung:
     -Benutzerverwaltung
     -Passwortprüfung und -verschlüsselung
     -2FA-Mechanismus
     -Kontosperrung
     -Audit-Logging
   Algorithmen:
     1. Passwortverschlüsselung:
       HMAC-SHA256 wird mit einem geheimen Schlüssel verwendet.Passwörter werden mit einem Benutzernamen-String kombiniert, um sowohl Kollisionen zu vermeiden als auch Sicherheit zu erhöhen.
     2. Passwortprüfung:
       Regex-Muster prüfen auf:
         Mindestlänge von 12 Zeichen.Zahlen, Großbuchstaben, Sonderzeichen.
     3. 2FA:
       Ein zufälliger 6-stelliger Code wird generiert und ist 30 Sekunden gültig.
   Datenstrukturen:
     1. Benutzer-Datenbank (users_db.txt):
       Enthält ein Array von dem Benutzernamen und dem gehashten Passwort.
       Format: ["Benutzername", "gehashtes Passwort"]
     2. Audit-Log (log.txt): 
        Protokolliert sicherheitsrelevante Aktionen in folgendem
        Format:Tue Dec 3 14:00:00 2024     Benutzername     Aktion.
     4. Sperrliste (blocked_accounts.txt):
       Enthält Benutzernamen gesperrter Konten.
   Schnittstellenbeschreibung:
     1. Benutzerklasse (Interface):
       Zweck: Repräsentiert einen Benutzer.
       Methoden:
         __init__(self, username, password_hashed): Initialisiert einen Benutzer.
         password_encryption(password): Verschlüsselt Passwörter.
     2. Funktionen (Services):
       -registration(): Verantwortlich für die Registrierung eines neuen Benutzers.
       -login(): Behandelt Benutzeranmeldung, Passwortprüfung und Zwei-Faktor-Authentifizierung.
       -audit_log(user_name, change): Protokolliert Benutzeraktionen in einer Logdatei.
       -change_password(username): Ermöglicht dem Benutzer, sein Passwort zu ändern.
