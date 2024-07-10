import streamlit as st
import pandas as pd
import math
import os
import json
from PIL import Image
from streamlit_option_menu import option_menu

import data_resampling
from Benutzer_Verwaltung import funktion_verwaltung
from Personen import read_data, Klasse_ekgdata, Klasse_person
from CSV_analyse import Einteilung_Zonen, Power_Curve


with st.sidebar: 
    selected = option_menu (menu_title= "Menu", options= ["Start Seite", "Benutzer Verwaltung", "Personen und EKG", "CSV Analyse"])

# Laden der Json Datei
json_file_link = 'data/person_db_aktuell.json' ### Verwendete Json Datei
data_json_aktuell = read_data.load_person_data(json_file_link)

input_folder = os.path.join('Data', 'ekg_data')
output_folder = os.path.join('Data', 'resampled_data')

frequenz_faktor = 100
old_link = "data/ekg_data/"
new_link = "data/resampled_data/"

# Daten werden nach Bedürfniss genutzt
data_resampling.resample_and_changeLink_ekg_data (input_folder, output_folder, new_link, old_link, json_file_link)


if selected == "Start Seite":
    
    st.title("# Start Seite")
    st.subheader ("Informationen")
    st.write ("""Die Webseite ermöglicht die Verwaltung von Benutzern und deren EKG-Daten. Benutzer können hinzugefügt, aktualisiert und deren EKG-Daten analysiert werden. Die EKG-Daten werden visuell dargestellt und mithilfe von Herzratenvariabilitätsanalysen ausgewertet. Zusätzlich können CSV-Dateien analysiert werden.""")


if selected == "Benutzer Verwaltung":

    st.title("# Benutzer Verwaltung")
    
    #Auswählen was man machen möchte
    option = st.selectbox("Aktion auswählen", ("Neuen Benutzer hinzufügen", "Bestehenden Benutzer aktualisieren"))

    if option == "Neuen Benutzer hinzufügen":

        user_id = funktion_verwaltung.get_next_user_id(data_json_aktuell)
        firstname = st.text_input("Vorname")
        lastname = st.text_input("Nachname")
        date_of_birth = st.number_input("Geburtsjahr", min_value=1940, max_value=2025, value =2000, step=1)

        # Bild hochladen
        uploaded_picture_Person = st.file_uploader("Bild Datei hochladen", type=["jpg", "jpeg", "png"])
        picture_path = None

        # link hinzufügen
        if uploaded_picture_Person is not None:
            picture_filename = f"{user_id}_{uploaded_picture_Person.name}"
            picture_path = f"data/pictures/{picture_filename}"
            with open(picture_path, "wb") as f:
                f.write(uploaded_picture_Person.getbuffer())
            st.success(f"Bild {uploaded_picture_Person.name} hochgeladen")

        # Ekg Datei hochladen
        uploaded_file_EKG = st.file_uploader("EKG Datei hochladen", type=["txt"])
        ekg_tests = []

        # link hinzufügen
        if uploaded_file_EKG is not None:
            ekg_id = funktion_verwaltung.get_next_ekg_id(data_json_aktuell)
            ekg_date = st.text_input("EKG Datum")
            ekg_filename = f"{user_id}_{ekg_id}_{uploaded_file_EKG.name}"
            ekg_result_link = f"data/ekg_data/{ekg_filename}"

            with open(ekg_result_link, "wb") as f:
                f.write(uploaded_file_EKG.getbuffer())
            st.success(f"Datei {uploaded_file_EKG.name} hochgeladen")

            ekg_tests.append({
                "id": ekg_id,
                "date": ekg_date,
                "result_link": ekg_result_link
            })

        user_info = {
            "id": user_id,
            "date_of_birth": date_of_birth,
            "firstname": firstname,
            "lastname": lastname,
            "picture_path": picture_path,
            "ekg_tests": ekg_tests }

        # anzeigen ob anfrage erfolgreich war
        if st.button("Benutzer hinzufügen"):
            funktion_verwaltung.manage_user(json_file_link, user_info)
            st.success("Neuer Benutzer hinzugefügt!")
            # st.session_state.data_json_aktuell = data_json_aktuell


    if option == "Bestehenden Benutzer aktualisieren":

        user_options = {f"{person['id']} - {person['firstname']} {person['lastname']}": person['id'] for person in data_json_aktuell}
        selected_user = st.selectbox("Wähle einen Benutzer", list(user_options.keys()))
        selected_user_id = user_options[selected_user]

        user_info = next((person for person in data_json_aktuell if person['id'] == selected_user_id), None)

        if user_info:
            firstname = st.text_input("Vorname", value=user_info['firstname'])
            lastname = st.text_input("Nachname", value=user_info['lastname'])
            date_of_birth = st.number_input("Geburtsjahr", min_value = 1940, max_value = 2025, step = 1, value = user_info['date_of_birth'])

            # Bilddatei aktualisieren
            if st.checkbox("Bild Datei aktualisieren"):
                uploaded_picture_Person_New = st.file_uploader("Neue Bild Datei hochladen", type=["jpg", "jpeg", "png"])
                if uploaded_picture_Person_New is not None:
                    picture_filename = f"{selected_user_id}_{uploaded_picture_Person_New.name}"
                    picture_path = f"data/pictures/{picture_filename}"
                    with open(picture_path, "wb") as f:
                        f.write(uploaded_picture_Person_New.getbuffer())
                    st.success(f"Bild {uploaded_picture_Person_New.name} hochgeladen")
                    user_info['picture_path'] = picture_path

            # Egk Datei aktualisieren
            if st.checkbox("EKG Datei hinzufügen"):
                uploaded_EKG_file_New = st.file_uploader("Neue EKG Datei hochladen", type=["txt"])
                if uploaded_EKG_file_New is not None:
                    ekg_id = funktion_verwaltung.get_next_ekg_id(data_json_aktuell)
                    ekg_date = st.text_input("EKG Datum")
                    ekg_filename = f"{selected_user_id}_{ekg_id}_{uploaded_EKG_file_New.name}"
                    ekg_result_link = f"data/ekg_data/{ekg_filename}"

                    with open(ekg_result_link, "wb") as f:
                        f.write(uploaded_EKG_file_New.getbuffer())
                    st.success(f"Datei {uploaded_EKG_file_New.name} hochgeladen")

                    user_info['ekg_tests'].append({
                        "id": ekg_id,
                        "date": ekg_date,
                        "result_link": ekg_result_link
                    })

            user_info['firstname'] = firstname
            user_info['lastname'] = lastname
            user_info['date_of_birth'] = date_of_birth

            # anzeigen ob anfrage erfolgreich war
            if st.button("Benutzer aktualisieren"):
                funktion_verwaltung.manage_user(json_file_link, user_info, update=True)
                st.success("Benutzer aktualisiert!")
                # st.session_state.data_json_aktuell = data_json_aktuell

    # if 'data' not in st.session_state:
    #     json_file = 'data/person_db_aktuell.json'
    #     with open(json_file, 'r') as file:
    #         st.session_state.data = json.load(file)
    


if selected == "Personen und EKG":

    st.title("# EKG APP")

    # st.subheader("Geresamplete Daten Verwenden?")
    # Checkbox erstellen
    # agree = st.checkbox("Ja, geresamplete Daten Verwenden")
    
    # Input und Output Ordner für Geresamplete Daten
    # input_folder = os.path.join('Data', 'ekg_data')
    # output_folder = os.path.join('Data', 'resampled_data')

    # frequenz_faktor = 100

    # Überprüfen ob Checkbox aktiviert ist
    # if agree:
    #     st.write("Es werden die geresamplten Daten Verwendet.")
    #     frequenz_faktor = 100 #für richtige berechnung der Herzrate, 100 wegen aufnamen der geresampleten Daten in [10 ms] schritten

    #     old_link = "data/resampled_data/"
    #     new_link = "data/ekg_data/"

    # else:
    #     st.write("Es werden die originalen Daten genutzt")
    #     frequenz_faktor = 500 #für richtige berechnung der Herzrate, 500 wegen aufnamen der Daten in [2 ms] schritten

    #     old_link = "data/ekg_data/"
    #     new_link = "data/resampled_data/"

    # old_link = "data/ekg_data/"
    # new_link = "data/resampled_data/"
    
    # # Daten werden nach Bedürfniss genutzt
    # data_resampling.resample_and_changeLink_ekg_data (input_folder, output_folder, new_link, old_link, json_file_link)

    ### !!! NAMEN EINFÜGEN!!!
    list_person_names = read_data.get_person_list(data_json_aktuell)


    # Session State wird leer angelegt, solange er noch nicht existiert
    if 'current_user' not in st.session_state:
        st.session_state.current_user = 'None'

    # Dieses Mal speichern wir die Auswahl als Session State
    st.session_state.current_user = st.selectbox('Versuchsperson wählen', options = list_person_names, key="sbVersuchsperson")


    ### KLASSE PERSON
    # Weise Personen ID zu
    for names, ID_vergabe in zip(list_person_names, range(len(list_person_names))):
        if st.session_state.current_user == names:
            ID_person = ID_vergabe + 1
    
    # Erstelle Instanz Person
    Person_Dict = Klasse_person.Person.load_by_id(ID_person, data_json_aktuell)
    Instanz_von_Current_user = Klasse_person.Person(Person_Dict)

    tab1, tab2 = st.tabs(["Versuchsperson Informationen", "EKG-Daten"])

    # Text im ersten Tab 
    with tab1:
        # Zwei Spalten erzeugen
        col1, col2 = st.columns(2, gap = "large")

        with col1:

            # Personen Daten
            st.subheader ('Personen Daten:')

            df_Personendaten = pd.DataFrame(columns=['Spalte1', 'Spalte2'])
            df_Personendaten = df_Personendaten._append({'Spalte1': "Vorname: ", 'Spalte2': read_data.find_person_data_by_name(st.session_state.current_user, data_json_aktuell)["firstname"]}, ignore_index=True)
            df_Personendaten = df_Personendaten._append({'Spalte1': "Nachname: ", 'Spalte2': read_data.find_person_data_by_name(st.session_state.current_user, data_json_aktuell)["lastname"]}, ignore_index=True)
            df_Personendaten = df_Personendaten._append({'Spalte1': "Geburtsjahr: ", 'Spalte2': str (read_data.find_person_data_by_name(st.session_state.current_user, data_json_aktuell)["date_of_birth"])}, ignore_index=True)
            df_Personendaten = df_Personendaten._append({'Spalte1': "Alter: ", 'Spalte2': str (Instanz_von_Current_user.calc_age())}, ignore_index=True)
            df_Personendaten = df_Personendaten._append({'Spalte1': "Maximale Herzfrequenz: ", 'Spalte2': str (Instanz_von_Current_user.calc_max_heart_rate())}, ignore_index=True)
            
            # st.dataframe(df_Personendaten.values)
            # st.table(df_Personendaten)

            # Index und Spaltennamen ausblenden
            df_Personendaten_styled = df_Personendaten.style.hide(axis='index').hide(axis='columns')

            # In HTML umwandeln
            html_table = df_Personendaten_styled.to_html()

            # Streamlit-Anzeige
            st.write(html_table, unsafe_allow_html=True)


           # Bild in der zweiten Spalte
        with col2:
            ### !!! BILD EINFÜGEN!!!

            # Anlegen des Session State. Bild, wenn es kein Bild gibt
            if 'picture_path' not in st.session_state:
                st.session_state.picture_path = 'data/pictures/none.jpg'

            # Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
            if st.session_state.current_user in list_person_names:
                st.session_state.picture_path = read_data.find_person_data_by_name(st.session_state.current_user, data_json_aktuell)["picture_path"]
            
            image = Image.open(st.session_state.picture_path)
            st.image(image)
  
        # st.session_state.current_test = st.selectbox('Test', options = [[1, " ruhe"],[2, " besl"]], key="sbTest")


 # Text im zweiten Tab
    with tab2:

        st.subheader('EKG-Daten')

        ### KLASSE EKG
        liste_ekg_tests = []
        for einträge in Person_Dict ['ekg_tests']:
            liste_ekg_tests.append(einträge['id'] )
        
        st.session_state.current_EKG_test = st.selectbox('EKG Test [ID]', options = liste_ekg_tests, key="sbEKG_Test")
       
        # Erstelle Instanz EKG test
        EKG_Dict = Klasse_ekgdata.EKGdata.load_by_id (st.session_state.current_EKG_test, data_json_aktuell)
        Instanz_von_Current_EKG = Klasse_ekgdata.EKGdata(EKG_Dict)
        
        Instanz_von_Current_EKG.set_empty_values(None, None, frequenz_faktor)
        
        # Zeitbereich auswählen
        st.subheader("Zeitbereich auswählen")

        start_wert, end_wert = st.slider(
                'Wähle den Bereich',
                min_value=0 , max_value= math.ceil(Instanz_von_Current_EKG.return_Länge_Zeitreihe()), value=(1, 20)
            )
        
        st.write(f'__ausgewählter Start Wert:__ {start_wert}')
        st.write(f'__ausgewählter End Wert:__   {end_wert}')

        Instanz_von_Current_EKG.set_empty_values(start_wert, end_wert, frequenz_faktor)

        # erstellen des Plots für das EKG Signal
        fig_Ekg = Instanz_von_Current_EKG.plot_time_series()
        st.plotly_chart(fig_Ekg)

        tab3, tab4 = st.tabs(["Daten", "Eigenschaften der Herzrate"])

        with tab3:

            st.metric(label="**Länge der gesamten Zeitreihe in Sekunden:**", value = round(Instanz_von_Current_EKG.return_Länge_Zeitreihe(), 2))
            st.metric(label="**Testdatum:**", value = Instanz_von_Current_EKG.return_Test_Datum())
            st.metric(label="**Dateipfad:**", value = Instanz_von_Current_EKG.data)
        
        with tab4:

            Herzrate_Overall, _ = Instanz_von_Current_EKG.estimate_hr()
            _, Herzrate_Bereich = Instanz_von_Current_EKG.estimate_hr()
            st.metric(label="**Durchschnittliche Herzrate [Bpm] in der gesamten Zeit:**", value = round(float(Herzrate_Overall),2))
            st.metric(label="**Durchschnittliche Herzrate [Bpm] im angezeigten Zeitfenster:**", value = round(float(Herzrate_Bereich),2))

            if round(float(Herzrate_Bereich),2) == 0:
                st.write ("Keine Berechnung möglich, da weniger als 2 Peaks im Zeitfenster vorliegen. Bitte wählen sie ein längeres Zeitfenster aus.")
            
            fig_Heartrate = Instanz_von_Current_EKG.plot_heartrate()
            st.plotly_chart(fig_Heartrate)
            
            st.subheader("Analyse der Herzvariabilität")
            Herzvariabilität_overall = Instanz_von_Current_EKG.compute_hrv_overall()
            Herzvariabilität_bereich = Instanz_von_Current_EKG.compute_hrv_Bereich()

            col11, col22 = st.columns(2)
            with col11:
                st.write ("__Im ganzen Zeit Bereich__")
                st.metric(label="**HRV Mittelwert [s]:**", value = (round ((Herzvariabilität_overall["HRV_MeanNN"]/ 1000 ),3  )))
                st.metric(label="**Maximale Zeit zwischen zwei Spitzen [s]:**", value = (round ((Herzvariabilität_overall["HRV_MinNN"]/ 1000 ),3  )))
                st.metric(label="**Minimale Zeit zwischen zwei Spitzen [s]:**", value = (round ((Herzvariabilität_overall["HRV_MaxNN"]/ 1000 ),3  )))
 
            with col22:
                st.write ("__Im ausgewählten Zeit Bereich__")
                st.metric(label="**HRV Mittelwert [s]:**", value = (round ((Herzvariabilität_bereich["HRV_MeanNN"]/ 1000 ),3  )))
                st.metric(label="**Maximale Zeit zwischen zwei Spitzen [s]:**", value = (round ((Herzvariabilität_bereich["HRV_MinNN"]/ 1000 ),3  )))
                st.metric(label="**Minimale Zeit zwischen zwei Spitzen [s]:**", value = (round ((Herzvariabilität_bereich["HRV_MaxNN"]/ 1000 ),3  )))


if selected == "CSV Analyse":

    st.title("# CSV Analyse")# Zwei tabs erzeugen
    tab11, tab12 = st.tabs(["Einteilung Zonen", "Power Curve"])

    with tab11:
            
            eingabe_wert_frequenz = st.number_input('Geben sie ihre maximale Herzfrequenz ein:', min_value=120, max_value=250, value = 190)
            # eingabe_wert_frequenz = Instanz_von_Current_user.calc_max_heart_rate()

            st.write ("Ihre Maximale Herzfrequenz beträgt " + str(eingabe_wert_frequenz))
            
            df = Einteilung_Zonen.load_activity()
            fig = Einteilung_Zonen.make_plot_EKG(df,eingabe_wert_frequenz)
            st.plotly_chart(fig)

            # Zwei tabs erzeugen
            tab13, tab14 = st.tabs(["Eigenschaften Leistung", "Eigenschaften der Zonen"])

            # Text im ersten Tab 
            with tab13:
                st.subheader('Eigenschaften Leistung')

                st.metric(label="Mittelwert Leistung [w]", value = round(Einteilung_Zonen.mittelwert (df), 4))
                st.metric(label="Maximale Leistung [w]", value = Einteilung_Zonen.max_Leistung (df))

            # Text im zweiten Tab
            with tab14:
                st.subheader('Verbrachte Zeit und Durchschnittliche Leistung der Zonen')
                data = Einteilung_Zonen.calc_time_and_average_in_Zones(df,eingabe_wert_frequenz)
                df_Zones = pd.DataFrame(data)
                df_Zones.set_index('Zone', inplace=True)
                st.dataframe(df_Zones)

    with tab12:
        # st.write ("Hier ist die Grafik der Power Curve")
        df = Power_Curve.load_activity()
        st.subheader('Eingabe der Frequenz')
        frequenz = st.number_input('Frequenz:', min_value=1, max_value=20, value = 1)

        st.subheader('Zeitfenster für vergrößerten Plot')
        # eingabe Vergrößerter Plot
        untere_Grenze = st.number_input('untere Grenze auf der X-achse in sekunden:', min_value=0, max_value=1805, value = 0)
        obere_Grenze_0 = st.number_input('obere Grenze auf der X-achse in sekunden:', min_value=0, max_value=1805, value = 300)

        obere_Grenze = obere_Grenze_0 + 5   #Um obere Grenze auch auf der X achse anzeigen zu lassen

        fig_1 = Power_Curve.make_plot_PowerCurve(df, untere_Grenze, obere_Grenze, frequenz)
        st.plotly_chart(fig_1)

        fig_2 = Power_Curve.make_plot_PowerCurve_zoomed(df, untere_Grenze, obere_Grenze, frequenz)
        st.plotly_chart(fig_2)








