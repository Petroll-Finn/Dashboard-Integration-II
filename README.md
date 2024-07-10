# Dashboard-Integration-II
von Till und Finn

## Funktionen der App:

### Benutzerverwaltung

    Neuen Benutzer hinzufügen:
        Benutzerinformationen eingeben: Vorname, Nachname und Geburtsjahr.
        Bild hochladen: Benutzer kann ein Bild hochladen.
        EKG-Datei hochladen: Benutzer kann eine EKG-Datei hochladen und das Datum des EKG-Tests angeben.
        Speichern: Neue Benutzerinformationen werden gespeichert.

    Bestehenden Benutzer aktualisieren:
        Benutzer auswählen: Aus einer Liste von vorhandenen Benutzern auswählen.
        Benutzerinformationen aktualisieren: Vorname, Nachname und Geburtsjahr können geändert werden.
        Bild aktualisieren: Ein neues Bild hochladen.
        EKG-Datei hinzufügen: Eine neue EKG-Datei hochladen und das Datum des EKG-Tests angeben.
        Speichern: Aktualisierte Benutzerinformationen werden gespeichert.

### Personen und EKG

    Resample-Option: Benutzer kann wählen, ob die geresampleten Daten verwendet werden sollen.
    Versuchsperson auswählen: Eine Person aus einer Liste von Versuchspersonen auswählen.
    Versuchsperson Informationen:
        Personendaten anzeigen: Vorname, Nachname, Geburtsjahr, Alter und maximale Herzfrequenz der ausgewählten Person anzeigen.
    EKG-Daten:
        EKG-Daten anzeigen und analysieren: EKG-Daten der ausgewählten Person anzeigen und analysieren. Es werden verschiedene Plots und Herzratenberechnungen durchgeführt.

### CSV-Analyse

    Analyse von CSV-Daten: Benutzer können CSV-Daten analysieren und Ergebnisse anzeigen lassen. Diese Funktionalität ist jedoch im bereitgestellten Code nicht detailliert beschrieben.

## Anfoderungen:

Stellen Sie sicher, dass Sie alle im requirements.txt erwähnten Bibliotheken installiert haben.

Um eine Bibliotheken zu Installieren verwenden Sie folgenden Befehl:

pip install "Name der Bibliothek"






python -m streamlit run app_website.py
