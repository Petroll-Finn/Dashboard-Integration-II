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



    def __init__(self, ekg_dict, head_Werte = 2000):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.head_Werte = head_Werte

    def make_plot(self):
        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV", labels ='signal')

    
    def df_for_plotting (self):
        df_plotting = self.df
        # df_plotting['Zeit in ms'] = df_plotting['Zeit in ms'].astype(float)/ 500 # umrechnen in Sekunden für Plot

        df_plotting['Zeit in ms'] = df_plotting['Zeit in ms'] - (df_plotting.at[0, 'Zeit in ms'] - 2 ) # um immer bei 0 zu beginnen
        df_plotting['Zeit in ms'] = df_plotting['Zeit in ms'] / 1000
        return df_plotting

    def find_peaks (self):
        # df_head = self.df_for_plotting ()

        df_head = self.df

        peaks_indizes, Messwerte_bei_Peaks = find_peaks(df_head['Messwerte in mV'], height=350)
        # list_Messwerte_bei_Peaks = Messwerte_bei_Peaks ['peak_heights']

        peaks_ganze_Zeitreihe_Indizes, Messwerte_Peaks_ganze_Zeitreihe_ = find_peaks(self.df['Messwerte in mV'], height=350)

        return peaks_indizes, peaks_ganze_Zeitreihe_Indizes


    def plot_time_series(self):
        df_head = self.df_for_plotting ()

        # df_head = self.df
        # df_head['Zeit in ms'] = df_head['Zeit in ms'] / 1000

        print (df_head)

        self.peaks, _ = self.find_peaks()
        # print (self.peaks[0])

        self.fig = go.Figure()
        self.fig.add_scatter (x=df_head['Zeit in ms'], y=df_head['Messwerte in mV'], mode='lines', name='Signal')
        self.fig.add_scatter (x=df_head['Zeit in ms'][self.peaks], y=df_head['Messwerte in mV'][self.peaks], mode='markers', name='Peaks', marker=dict(color='red', size=10))
        self.fig.update_layout(title='Plot des Ekg Signals mit Peaks', xaxis_title='Zeit [s]', yaxis_title='Amplitude [Mv]')

        return self.fig 
    
    
    def estimate_hr(self):
        self.peaks, _ = self.find_peaks()
        peak_differenz = [self.peaks[i+1] - self.peaks[i] for i in range(len(self.peaks)-1)]
        durchschnittliche_peak_diff = sum(peak_differenz) / len(peak_differenz)
        Herzrate= 60 / (durchschnittliche_peak_diff / 500) # 500 wegen aufnamen der Daten in [2 ms] schritten

        # _, self.peaks_ganze_zeitreihe = self.find_peaks()
        # peak_differenz = [self.peaks_ganze_zeitreihe[i+1] - self.peaks_ganze_zeitreihe[i] for i in range(len(self.peaks_ganze_zeitreihe)-1)]
        # durchschnittliche_peak_diff = sum(peak_differenz) / len(peak_differenz)
        # Herzrate= 60 / (durchschnittliche_peak_diff / 500) # 500 wegen aufnamen der Daten in [2 ms] schritten

        # print (Herzrate)
        return Herzrate
    
    def return_Test_Datum (self):
        datum = self.date
        return (datum)
    
    def return_Länge_Zeitreihe (self):
        df = self.df
        zeit = len(df) / 500
        return zeit



#df_plotting['Zeit in ms'] = df_plotting['Zeit in ms'] / 500 # umrechnen in Sekunden für Plot

if __name__ == "__main__":
    # print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")

    person_data = json.load(file)
    # print(person_data)
    
    ekg_dict1 = person_data[1]["ekg_tests"][0]
    print(ekg_dict1)
    ekg = EKGdata (ekg_dict1)
    # print (ekg.df)

    # print (ekg.test())
    
    # tuple1= ekg.find_peaks()
    # print (tuple1[1])

    
    # print (ekg.find_peaks())


    # print(ekg.df.head())
    # EKGdata.find_peaks(1)

    # print (ekg.return_Test_Datum())
    print (ekg.return_Länge_Zeitreihe())
    
    

    fig = ekg.plot_time_series()
    fig.show()
    # print (EKGdata.load_by_id(4))




# %%
