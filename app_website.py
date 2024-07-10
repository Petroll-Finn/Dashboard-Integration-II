import streamlit as st
import pandas as pd
import math

from Personen import read_data, Klasse_ekgdata, Klasse_person
from CSV_analyse import Einteilung_Zonen, Power_Curve

from PIL import Image
from streamlit_option_menu import option_menu


with st.sidebar: 
    selected = option_menu (menu_title= "Menu", options= ["Personen", "CSV Analyse"])


if selected == "Personen":

    st.title("# EKG APP")# Zwei tabs erzeugen

    st.subheader("Geresamplete Daten Verwenden?")
    # Checkbox erstellen
    agree = st.checkbox("Ja, geresamplete Daten Verwenden")
    
    # Überprüfen ob Checkbox aktiviert ist
    if agree:
        st.write("Es werden die geresamplte Daten Verwendet.")
        frequenz_faktor = 100 #für richtige berechnung der Herzrate, 100 wegen aufnamen der Daten in [10 ms] schritten
        link = "data/person_db_resampled.json"
    else:
        st.write("Es werden die originalen Daten genutzt")
        frequenz_faktor = 500 #für richtige berechnung der Herzrate, 500 wegen aufnamen der Daten in [2 ms] schritten
        link = "data/person_db.json"    

    ### !!! NAMEN EINFÜGEN!!!
    list_person_names = read_data.get_person_list(link)
    # print (list_person_names)

    # Session State wird leer angelegt, solange er noch nicht existiert
    if 'current_user' not in st.session_state:
        st.session_state.current_user = 'None'

    # Dieses Mal speichern wir die Auswahl als Session State
    st.session_state.current_user = st.selectbox('Versuchsperson wählen', options = list_person_names, key="sbVersuchsperson")
    # st.write (st.session_state.current_user)

    # Json Daten Laden
    Person_Json = read_data.load_person_data(link)

    ### KLASSE PERSON
    # Weise Personen ID zu
    for names, ID_vergabe in zip(list_person_names, range(len(list_person_names))):
        if st.session_state.current_user == names:
            ID_person = ID_vergabe + 1
            
    # Erstelle Instanz Person
    Person_Dict = Klasse_person.Person.load_by_id(ID_person)
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
            df_Personendaten = df_Personendaten._append({'Spalte1': "Vorname: ", 'Spalte2': read_data.find_person_data_by_name(st.session_state.current_user, link)["firstname"]}, ignore_index=True)
            df_Personendaten = df_Personendaten._append({'Spalte1': "Nachname: ", 'Spalte2': read_data.find_person_data_by_name(st.session_state.current_user, link)["lastname"]}, ignore_index=True)
            df_Personendaten = df_Personendaten._append({'Spalte1': "Geburtsjahr: ", 'Spalte2': str (read_data.find_person_data_by_name(st.session_state.current_user, link)["date_of_birth"])}, ignore_index=True)
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
                st.session_state.picture_path = read_data.find_person_data_by_name(st.session_state.current_user, link)["picture_path"]

            # Öffne das Bild und Zeige es an
            # image = Image.open("../" + st.session_state.picture_path)
            
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
        EKG_Dict = Klasse_ekgdata.EKGdata.load_by_id (st.session_state.current_EKG_test, link)
        Instanz_von_Current_EKG = Klasse_ekgdata.EKGdata(EKG_Dict)
        
        
        # Zeitbereich auswählen
        st.subheader("Zeitbereich auswählen")

        start_wert, end_wert = st.slider(
                'Wähle den Bereich',
                min_value=0 , max_value= math.ceil(Instanz_von_Current_EKG.return_Länge_Zeitreihe()), value=(1, 20)
            )

        st.write(f'ausgewählter Start Wert: {start_wert}, ausgewählter End Wert: {end_wert}')

        Instanz_von_Current_EKG.set_empty_values(start_wert, end_wert, frequenz_faktor)

        
        # erstellen des Plots für das EKG Signal
        fig_Ekg = Instanz_von_Current_EKG.plot_time_series()
        st.plotly_chart(fig_Ekg)

        tab3, tab4 = st.tabs(["Daten", "Eigenschaften der Herz Frequenz"])

        with tab3:
            # st.markdown ("**Dateiname:**" )
            # st.write (Instanz_von_Current_EKG.data[14:])           

            # st.markdown ("**Durchschnittliche Herzrate [Bpm] im angezeigten Zeitfenster:**" )
            # st.write (str(round(Instanz_von_Current_EKG.estimate_hr(), 2)))
            
            st.metric(label="**Länge der gesamten Zeitreihe in Sekunden:**", value = round(Instanz_von_Current_EKG.return_Länge_Zeitreihe(), 2))
            st.metric(label="**Testdatum:**", value = Instanz_von_Current_EKG.return_Test_Datum())
            st.metric(label="**Dateiname:**", value = Instanz_von_Current_EKG.data[14:])
        
        with tab4:

            Herzrate_Overall, _ = Instanz_von_Current_EKG.estimate_hr()
            _, Herzrate_Bereich = Instanz_von_Current_EKG.estimate_hr()
            st.metric(label="**Durchschnittliche Herzrate [Bpm] in der gesamten Zeit:**", value = round(float(Herzrate_Overall),2))
            st.metric(label="**Durchschnittliche Herzrate [Bpm] im angezeigten Zeitfenster:**", value = round(float(Herzrate_Bereich),2))

            if round(float(Herzrate_Bereich),2) == 0:
                st.write ("Keine Berechnung möglich, da weniger als 2 Peaks im Zeitfenster vorliegen. Bitte wählen sie ein längeres Zeitfenster aus.")
            
            fig_Heartrate = Instanz_von_Current_EKG.plot_heartrate()
            st.plotly_chart(fig_Heartrate)

if selected == "CSV Analyse":

    st.title("# CSV Analyse")# Zwei tabs erzeugen
    tab11, tab12 = st.tabs(["Einteilung Zonen", "Power Curve"])

    with tab11:
            
            eingabe_wert = st.number_input('Geben sie ihre maximale Herzfrequenz ein:', min_value=120, max_value=250, value = 190)
    
            df = Einteilung_Zonen.load_activity()
            fig = Einteilung_Zonen.make_plot_EKG(df,eingabe_wert)
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
                data = Einteilung_Zonen.calc_time_and_average_in_Zones(df,eingabe_wert)
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








