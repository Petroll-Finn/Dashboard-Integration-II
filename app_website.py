import streamlit as st
import pandas as pd
from Personen import read_data, Klasse_ekgdata, Klasse_person
# from Vorlesung_3 import read_pandas
# from Vorlesung_4 import funktions
from PIL import Image
from streamlit_option_menu import option_menu


with st.sidebar: 
    selected = option_menu (menu_title= "Menu", options= ["Personen", "Freie Aufgaben"])


if selected == "Personen":

    st.title("# EKG APP")# Zwei tabs erzeugen

    tab1, tab2 = st.tabs(["Versuchsperson Informationen", "EKG-Daten"])

 # Text im ersten Tab 
    with tab1:

        st.subheader('Versuchsperson Informationen')
        # Zwei Spalten erzeugen
        col1, col2 = st.columns(2, gap = "large")

        # Text in der ersten Spalte
        with col1:
            ### !!! NAMEN EINFÜGEN!!!
            list_person_names = read_data.get_person_list()
            # print (list_person_names)

            # Session State wird leer angelegt, solange er noch nicht existiert
            if 'current_user' not in st.session_state:
                st.session_state.current_user = 'None'

            # Dieses Mal speichern wir die Auswahl als Session State
            st.session_state.current_user = st.selectbox('Versuchsperson wählen', options = list_person_names, key="sbVersuchsperson")
            # st.write (st.session_state.current_user)

            # Json Daten Laden
            Person_Json = read_data.load_person_data()

            ### KLASSE PERSON
            # Weise Personen ID zu
            for names, ID_vergabe in zip(list_person_names, range(len(list_person_names))):
                if st.session_state.current_user == names:
                    ID_person = ID_vergabe + 1
            
            # Erstelle Instanz Person
            Person_Dict = Klasse_person.Person.load_by_id(ID_person)
            Instanz_von_Current_user = Klasse_person.Person(Person_Dict)

            # Personen Daten
            df = pd.DataFrame(columns=['Spalte1', 'Spalte2'])
            df = df._append({'Spalte1': "Vorname: ", 'Spalte2': read_data.find_person_data_by_name(st.session_state.current_user)["firstname"]}, ignore_index=True)
            df = df._append({'Spalte1': "Nachname: ", 'Spalte2': read_data.find_person_data_by_name(st.session_state.current_user)["lastname"]}, ignore_index=True)
            df = df._append({'Spalte1': "Geburtsjahr: ", 'Spalte2': str (read_data.find_person_data_by_name(st.session_state.current_user)["date_of_birth"])}, ignore_index=True)
            df = df._append({'Spalte1': "Alter: ", 'Spalte2': str (Instanz_von_Current_user.calc_age())}, ignore_index=True)
            df = df._append({'Spalte1': "Maximale Herzfrequenz: ", 'Spalte2': str (Instanz_von_Current_user.calc_max_heart_rate())}, ignore_index=True)
            
            st.dataframe(df.values)

            #Testen
            # st.write (str (Instanz_von_Current_user.calc_age()))
            # st.write (str (Instanz_von_Current_user.calc_max_heart_rate()))


           # Bild in der zweiten Spalte
        with col2:
            ### !!! BILD EINFÜGEN!!!

            # Anlegen des Session State. Bild, wenn es kein Bild gibt
            if 'picture_path' not in st.session_state:
                st.session_state.picture_path = 'data/pictures/none.jpg'

            # Suche den Pfad zum Bild, aber nur wenn der Name bekannt ist
            if st.session_state.current_user in list_person_names:
                st.session_state.picture_path = read_data.find_person_data_by_name(st.session_state.current_user)["picture_path"]

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
        EKG_Dict = Klasse_ekgdata.EKGdata.load_by_id (st.session_state.current_EKG_test)
        Instanz_von_Current_EKG = Klasse_ekgdata.EKGdata(EKG_Dict)

        fig_Ekg = Instanz_von_Current_EKG.plot_time_series()
        st.plotly_chart(fig_Ekg)

        # st.metric(label="Dateiname", value = Instanz_von_Current_EKG.data)
        st.markdown ("**Dateiname:**" )
        st.write (Instanz_von_Current_EKG.data[14:])

        st.metric(label="Durchschnittliche Herzrate [Bpm] im angezeigten Zeitfenster", value = round(Instanz_von_Current_EKG.estimate_hr(), 2))










