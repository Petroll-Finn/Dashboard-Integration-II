# Dashboard-Integration-II
von Till und Finn

Die Webseite ermöglicht die Verwaltung von Benutzern und deren EKG-Daten. Benutzer können hinzugefügt, aktualisiert und deren EKG-Daten analysiert werden. Die EKG-Daten werden visuell dargestellt und mithilfe von Herzratenvariabilitätsanalysen ausgewertet. Zusätzlich können CSV-Dateien analysiert werden.

## Anfoderungen:

Stellen Sie sicher, dass Sie alle im requirements.txt erwähnten Bibliotheken installiert haben.

Um alle eine Bibliotheken gleichzeitig zu Installieren verwenden Sie folgenden Befehl:

pip install -r requirements.txt

## Webseite öffnen:

Um die Webseite zu öffnen führen Sie Klasse_ekgdata.py, Klasse_person.py und read_data.py aus um zu überprüfen, dass das Installieren der Bibliotheken geklappt hat.

Geben Sie danach folgenden Befehl in Ihr Terminal ein um die Webseite in ihrem Browser zu offnen:

python -m streamlit run app_website.py


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

Resample-Option: Benutzer kann wählen, ob die geresampleten Daten verwendet werden sollen

Versuchsperson auswählen: Eine Person aus einer Liste von Versuchspersonen auswählen

Versuchsperson Informationen:
    Personendaten anzeigen: Vorname, Nachname, Geburtsjahr, Alter und maximale Herzfrequenz der ausgewählten Person anzeigen.
EKG-Daten:
    EKG-Daten anzeigen und analysieren: EKG-Daten der ausgewählten Person anzeigen und analysieren. Es werden verschiedene Plots und Herzratenberechnungen durchgeführt.

### CSV-Analyse

Analyse von CSV-Daten: Benutzer können CSV-Daten analysieren und Ergebnisse anzeigen lassen. Diese Funktionalität ist jedoch im bereitgestellten Code nicht detailliert beschrieben.




