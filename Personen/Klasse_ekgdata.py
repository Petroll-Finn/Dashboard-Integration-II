import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.signal import find_peaks

# %% Objekt-Welt

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen
    @staticmethod
    def load_Data():
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data
    
    @staticmethod
    def load_by_id (id_EKG):
        person_data = EKGdata.load_Data()
        # print (len(person_data))
        for eintrag_person in range(len(person_data)):
            # print (eintrag_person)
            for eintrag_EKG_tests in person_data[eintrag_person]["ekg_tests"]:
                # print (eintrag_EKG_tests)
                if eintrag_EKG_tests["id"] == id_EKG:
                    # print (eintrag_EKG_tests)
                    return eintrag_EKG_tests



    def __init__(self, ekg_dict, start_wert, end_wert):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.start_wert = start_wert
        self.end_wert = end_wert

    def make_plot(self):
        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV", labels ='signal')

    
    def return_df_for_Plotting (self):
        df_plotting = self.df
        df_plotting['Zeit in ms'] = df_plotting['Zeit in ms'] / 500 # umrechnen in Sekunden für Plot
        df_plotting = df_plotting.loc[(df_plotting['Zeit in ms'] >= self.start_wert) & (df_plotting['Zeit in ms'] <= self.end_wert)] #entfernung von Zeile die nicht im Zeitfenster liegen
        # print (df_plotting)
        return df_plotting
    

    def test (self):
        df = self.return_df_for_Plotting()
        return df


    def find_peaks (self):
        
        df = self.return_df_for_Plotting ()

        # print (df)

        peaks_indizes, Messwerte_bei_Peaks = find_peaks(df['Messwerte in mV'], height=350)
        # list_Messwerte_bei_Peaks = Messwerte_bei_Peaks ['peak_heights']
        peaks_ganze_Zeitreihe_Indizes, Messwerte_Peaks_ganze_Zeitreihe_ = find_peaks(self.df['Messwerte in mV'], height=350)
        print ("ich werde ausgeführt")
        return peaks_indizes, peaks_ganze_Zeitreihe_Indizes


    def plot_time_series(self):
        #Funktion für Plotten der Ekg signale
        df = self.return_df_for_Plotting()
        
        # print (self.test())

        print (df)

        self.peaks, _ = self.find_peaks()
        
        # df_head['Zeit in ms'] = df_head['Zeit in ms'] / 500 # umrechenn in Sekunden für Plot

        self.fig = go.Figure()
        self.fig.add_scatter (x = df['Zeit in ms'], y = df['Messwerte in mV'], mode='lines', name='Signal')
        self.fig.add_scatter (x = df['Zeit in ms'][self.peaks], y = df['Messwerte in mV'][self.peaks], mode='markers', name='Peaks', marker=dict(color='red', size=10))
        self.fig.update_layout(title='Plot des Ekg Signals mit Peaks', xaxis_title='Zeit [s]', yaxis_title='Amplitude [Mv]')

        return self.fig 
    


    def estimate_hr(self):
        #Funktion für Berechnung der Herzrate
        self.peaks, _ = self.find_peaks()
        peak_differenz = [self.peaks[i+1] - self.peaks[i] for i in range(len(self.peaks)-1)]
        durchschnittliche_peak_diff = sum(peak_differenz) / len(peak_differenz)
        Herzrate= 60 / (durchschnittliche_peak_diff / 500) # 500 wegen aufnamen der Daten in [2 ms] schritten

        return Herzrate
    
    def return_Test_Datum (self):
        datum = self.date
        return (datum)
    
    def return_Länge_Zeitreihe (self):
        df = self.df
        zeit = len(df) / 500
        return zeit



if __name__ == "__main__":
    # print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")

    person_data = json.load(file)
    # print(person_data)
    
    ekg_dict1 = person_data[0]["ekg_tests"][0]
    print(ekg_dict1)
    ekg = EKGdata (ekg_dict1, 30, 40)
    # print (ekg.df)

    # print (ekg.test())
    
    # tuple1= ekg.find_peaks()
    # print (tuple1[1])

    # print (ekg.return_df_for_Plotting())
    # print (ekg.find_peaks())


    # print(ekg.df.head())
    # EKGdata.find_peaks(1)

    # print (ekg.return_Test_Datum())
    # print (ekg.return_Länge_Zeitreihe())
    
    

    fig = ekg.plot_time_series()
    fig.show()
    # print (EKGdata.load_by_id(4))




# %%
