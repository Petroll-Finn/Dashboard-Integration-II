import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import neurokit2 as nk
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks

# %% Objekt-Welt


class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen
    @staticmethod
    def load_Data(link):
        file = open(link)
        person_data = json.load(file)
        return person_data
    
    @staticmethod
    def load_by_id (id_EKG, person_data_Dict):
        # Lädt EKG-Daten aus einer JSON-Datei.
        person_data = person_data_Dict
        
        # print (len(person_data))
        for eintrag_person in range(len(person_data)):
            # print (eintrag_person)
            for eintrag_EKG_tests in person_data[eintrag_person]["ekg_tests"]:
                # print (eintrag_EKG_tests)
                if eintrag_EKG_tests["id"] == id_EKG:
                    # print (eintrag_EKG_tests)
                    return eintrag_EKG_tests



    def __init__(self, ekg_dict):
    # Initialisiert die EKGdata-Klasse mit EKG-Daten.
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        
        self.start_wert = None
        self.end_wert = None
        self.frequenz_Faktor = None

    
    def set_empty_values(self, start, end, frequenz_Faktor):
    # Setzt die Start- und Endwerte sowie den Frequenzfaktor.
        self.start_wert = start
        self.end_wert = end
        self.frequenz_Faktor = frequenz_Faktor


    def make_plot(self):
        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV", labels ='signal')

    
    def df_for_plotting (self):
    #Bereitet den DataFrame für das Plotten vor.
        df_plotting = self.df

        df_plotting['Zeit in ms'] = df_plotting['Zeit in ms'] - (df_plotting.at[0, 'Zeit in ms'] - 2 ) # um immer bei 0s zu beginnen
        df_plotting = df_plotting.assign(**{'Zeit in ms': df_plotting['Zeit in ms'] / 1000})

        return df_plotting
    
    def return_df_bereich (self):
    # Gibt den DataFrame im angegebenen Bereich zurück.

        df_overall = self.df_for_plotting()
        df_bereich = df_overall.loc[(df_overall['Zeit in ms'] >= self.start_wert) & (df_overall['Zeit in ms'] <= self.end_wert)]

        return df_bereich

    def find_peaks (self):
    # Findet die Spitzen in den EKG-Daten.
        df_overall = self.df_for_plotting ()

        peaks_indizes_overall, Messwerte_Peaks_overall = find_peaks(df_overall['Messwerte in mV'], height=345)

        df_bereich = self.return_df_bereich ()
        peaks_indizes_bereich, Messwerte_Peaks_bereich = find_peaks(df_bereich['Messwerte in mV'], height=345)

        return peaks_indizes_overall, peaks_indizes_bereich


    def plot_time_series(self):
     # Plottet die Zeitreihe der EKG-Daten mit markierten Spitzen.   
        df_plotting = self.df_for_plotting ()
        self.peaks, _ = self.find_peaks()

        self.fig = go.Figure()
        self.fig.add_scatter (x = df_plotting['Zeit in ms'], y=df_plotting['Messwerte in mV'], mode='lines', name='Signal')
        self.fig.add_scatter (x = df_plotting['Zeit in ms'][self.peaks], y=df_plotting['Messwerte in mV'][self.peaks], mode='markers', name='Peaks', marker=dict(color='red', size=10))
        self.fig.update_layout(title='Plot des Ekg Signals mit Peaks', xaxis_title='Zeit [s]', yaxis_title='Amplitude [Mv]')
        self.fig.update_xaxes(range=[(self.start_wert), (self.end_wert)])
        return self.fig 

    
    def estimate_hr(self):
        # Berechnung der Durchschnittlichen Herzrate im Gesamten Bereich
        self.peaks_1, _ = self.find_peaks()
        peak_differenz_1 = [self.peaks_1[i+1] - self.peaks_1[i] for i in range(len(self.peaks_1)-1)]
        durchschnittliche_peak_diff_1 = sum(peak_differenz_1) / len(peak_differenz_1)
        hr_overall= 60 / (durchschnittliche_peak_diff_1 / self.frequenz_Faktor)

        # Berechnung der Durchschnittlichen Herzrate im Ausgewählten Bereich
        _, self.peaks_2 = self.find_peaks()
        peak_differenz_2 = [self.peaks_2[i+1] - self.peaks_2[i] for i in range(len(self.peaks_2)-1)]

        # division durch Null Error beheben, wenn nur ein Peak im Bereich
        if len(peak_differenz_2) == 0:
            hr_bereich = 0

        else:
            durchschnittliche_peak_diff_2 = sum(peak_differenz_2) / len(peak_differenz_2)
            hr_bereich= 60 / (durchschnittliche_peak_diff_2 / self.frequenz_Faktor) 
        

        return hr_overall, hr_bereich
    
    def plot_heartrate(self, window_size=5):
        # Plottet die Herzrate über die Zeit im ausgewählten Bereich.
        df_plotting = self.df_for_plotting()
        peaks, _ = find_peaks(df_plotting['Messwerte in mV'], height=350)
        peak_zeiten = df_plotting['Zeit in ms'].iloc[peaks].values
        
        hr_werte = []
        hr_zeiten = []
        
        for i in range(0, len(peak_zeiten) - window_size):
            window = peak_zeiten[i:i + window_size + 1]
            interval = window[-1] - window[0]
            hr = 60 * (len(window) - 1) / interval
            hr_werte.append(hr)
            hr_zeiten.append(window[0])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = hr_zeiten, y = hr_werte, mode='lines', name='Herzrate über Zeit', line=dict(color='green')))
        fig.update_layout(title='Herzrate über Zeit im ausgewählten Bereich', xaxis_title='Zeit [s]', yaxis_title='Herzrate [bpm]')
        fig.update_xaxes(range=[(self.start_wert), (self.end_wert)])
        
        return fig
    
    def return_Test_Datum (self):
        # Gibt das Datum des EKG-Tests zurück.
        datum = self.date
        return (datum)
    
    def return_Länge_Zeitreihe (self):
        # Gibt die Länge der Zeitreihe zurück.
        df = self.df
        zeit = len(df) / (self.frequenz_Faktor)
        return zeit
    
    def compute_hrv_overall(self):
        # Berechnet die Herzratenvariabilität (HRV) der EKG-Daten im gesamten Bereich
        ecg_signal = self.df['Messwerte in mV'].values
        signals, info = nk.ecg_process(ecg_signal, sampling_rate = self.frequenz_Faktor)
        hrv_overall = nk.hrv_time(signals, sampling_rate = self.frequenz_Faktor)
        return hrv_overall
    
    def compute_hrv_Bereich(self):
        # Berechnet die Herzratenvariabilität (HRV) der EKG-Daten im ausgewählten Bereich
        df_bereich = self.return_df_bereich ()
        ecg_signal = df_bereich['Messwerte in mV'].values
        signals, info = nk.ecg_process(ecg_signal, sampling_rate = self.frequenz_Faktor)
        hrv_Bereich = nk.hrv_time(signals, sampling_rate = self.frequenz_Faktor)
        return hrv_Bereich


if __name__ == "__main__":
    # print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")

    person_data = json.load(file)
    # print(person_data)
    
    ekg_dict1 = person_data[0]["ekg_tests"][0]
    print(ekg_dict1)
    ekg = EKGdata (ekg_dict1)
    ekg.set_empty_values (100, 104, 500)

    # print (ekg.df)

    # print (ekg.return_Länge_Zeitreihe())

    hrv = ekg.compute_hrv()
    print(hrv)
    print(hrv["HRV_MeanNN"])
    # print (ekg.estimate_hr())
    # print (ekg.test())
    
    # tuple1= ekg.find_peaks()
    # print (tuple1[1])

    
    # print (ekg.find_peaks())
    # print (ekg.df_for_plotting())
    

    # print(ekg.df.head())
    # EKGdata.find_peaks(1)

    # print (ekg.return_Test_Datum())
    
    # ekg.find_peaks()



    fig = ekg.plot_time_series()
    # fig.show()
    
    fig2 = ekg.plot_heartrate ()
    # fig2.show()

    # fig3 = ekg.make_plot ()
    # fig3.show()


# %%
