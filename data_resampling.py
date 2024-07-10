import os
import pandas as pd
import json

### resamplen der Daten und ersetzen des Resultlinks

def resample_and_changeLink_ekg_data(input_folder, output_folder, new_result_link_Var, old_result_link_Var, datalink, step=5,):
    
    # Laden der JSON-Datei
    with open(datalink, 'r') as file:
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
            new_result_link = f'{new_result_link_Var}{filename}'
            old_result_link = f'{old_result_link_Var}{filename}'

            for person in data:
                for ekg_test in person['ekg_tests']:
                    if ekg_test['result_link'].replace("\\", "/") == old_result_link:
                        ekg_test['result_link'] = new_result_link


    with open("data/person_db_aktuell.json", 'w') as file:
        json.dump(data, file, indent=4)



if __name__ == "__main__":
    input_folder = os.path.join('Data', 'ekg_data')
    output_folder = os.path.join('Data', 'resampled_data')

    old_link = "data/ekg_data/"
    new_link = "data/resampled_data/"

    resample_and_changeLink_ekg_data(input_folder, output_folder, new_link, old_link)



        
