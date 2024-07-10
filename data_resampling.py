import os
import pandas as pd
import json

### resamplen der Daten und ersetzen des Resultlinks

def resample_and_changeLink_ekg_data(input_folder, output_folder, step=5):

    # Laden der JSON-Datei
    with open("data/person_db.json", 'r') as file:
        data = json.load(file)

    # Durchlaufe alle Dateien im Eingabeordner
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            # Vollständiger Pfad zur Datei
            file_path = os.path.join(input_folder, filename)

            # TXT-Datei laden
            df = pd.read_csv(file_path, sep='\t', header=None)

            # Nur jeden fünften Datenpunkt auswählen
            df_resampled = df.iloc[::step, :]

            # Speichern der resampelten Daten
            output_file_path = os.path.join(output_folder, filename).replace("\\", "/")
            df_resampled.to_csv(output_file_path, sep='\t', index=False, header=False)

            # Ändern des Resultlinks
            new_result_link = f'data/resampled_data/{filename}'

            for person in data:
                for ekg_test in person['ekg_tests']:
                    old_result_link = f'data/ekg_data/{filename}'
                    if ekg_test['result_link'].replace("\\", "/") == old_result_link:
                        ekg_test['result_link'] = new_result_link


    with open("data/person_db_resampled.json", 'w') as file:
        json.dump(data, file, indent=4)


# Aufruf der Funktion
input_folder = os.path.join('Data', 'ekg_data')
output_folder = os.path.join('Data', 'resampled_data')

resample_and_changeLink_ekg_data(input_folder, output_folder)



        
