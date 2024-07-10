import json
import os


def get_next_user_id(data):
    # Gibt die nächste verfügbare Benutzer-ID zurück
    if data:
        return max(person['id'] for person in data) + 1
    else:
        return 1

def get_next_ekg_id(data):
    # Gibt die nächste verfügbare EKG-ID zurück
    ekg_ids = [ekg['id'] for person in data for ekg in person['ekg_tests']]
    if ekg_ids:
        return max(ekg_ids) + 1
    else: 
        return 1

def manage_user(json_file, user_info, update=False):
    # Laden der JSON-Datei
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    user_found = False
    
    # Falls update=True, suche den Benutzer und aktualisiere die Daten
    if update:
        for person in data:
            if person['id'] == user_info['id']:
                person.update(user_info)
                user_found = True
                break
        if not user_found:
            raise ValueError("User not found.")
    else:
        # Falls update=False, füge den neuen Benutzer hinzu
        user_info['id'] = get_next_user_id(data)
        data.append(user_info)

    # Speichern der aktualisierten JSON-Datei
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    # Benutzung der Funktion
    json_file = 'data/person_db_test.json'

    # Neuen Benutzer hinzufügen
    # manage_user(json_file, new_user_info)

    # Bestehenden Benutzer aktualisieren
    # manage_user(json_file, updated_user_info, update=True)