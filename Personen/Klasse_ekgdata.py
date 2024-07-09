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



    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        
        self.start_wert = None
        self.end_wert = None
    
    def set_start_und_end_wert(self, start, end):
        self.start_wert = start
        self.end_wert = end


    def make_plot(self):
        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        self.fig = px.line(self.df, x="Zeit in ms", y="Messwerte in mV", labels ='signal')

    
    def df_for_plotting (self):
        df_plotting = self.df

        df_plotting['Zeit in ms'] = df_plotting['Zeit in ms'] - (df_plotting.at[0, 'Zeit in ms'] - 2 ) # um immer bei 0s zu beginnen
        df_plotting = df_plotting.assign(**{'Zeit in ms': df_plotting['Zeit in ms'] / 1000})

        return df_plotting

    def return_df_bereich (self):
        df_overall = self.df_for_plotting()
        df_bereich = df_overall.loc[(df_overall['Zeit in ms'] >= self.start_wert) & (df_overall['Zeit in ms'] <= self.end_wert)]

        return df_bereich

    def find_peaks (self):
        df_overall = self.df_for_plotting ()

        peaks_indizes_overall, Messwerte_Peaks_overall = find_peaks(df_overall['Messwerte in mV'], height=345)

        df_bereich = self.return_df_bereich ()
        peaks_indizes_bereich, Messwerte_Peaks_bereich = find_peaks(df_bereich['Messwerte in mV'], height=345)

        return peaks_indizes_overall, peaks_indizes_bereich


    def plot_time_series(self):
        
        df_plotting = self.df_for_plotting ()

        print (df_plotting)
        print("hier")

        self.peaks, _ = self.find_peaks()
        # print (self.peaks[0])

        self.fig = go.Figure()
        self.fig.add_scatter (x = df_plotting['Zeit in ms'], y=df_plotting['Messwerte in mV'], mode='lines', name='Signal')
        self.fig.add_scatter (x = df_plotting['Zeit in ms'][self.peaks], y=df_plotting['Messwerte in mV'][self.peaks], mode='markers', name='Peaks', marker=dict(color='red', size=10))
        self.fig.update_layout(title='Plot des Ekg Signals mit Peaks', xaxis_title='Zeit [s]', yaxis_title='Amplitude [Mv]')
        self.fig.update_xaxes(range=[(self.start_wert), (self.end_wert)])
        return self.fig 

    
    def estimate_hr(self):
        print ("heartrate")
        #Berechnung der Durchschnittlichen Herzrate im Gesamten Bereich
        self.peaks_1, _ = self.find_peaks()
        peak_differenz_1 = [self.peaks_1[i+1] - self.peaks_1[i] for i in range(len(self.peaks_1)-1)]
        durchschnittliche_peak_diff_1 = sum(peak_differenz_1) / len(peak_differenz_1)
        hr_overall= 60 / (durchschnittliche_peak_diff_1 / 500) # 500 wegen aufnamen der Daten in [2 ms] schritten

        #Berechnung der Durchschnittlichen Herzrate im Ausgewählten Bereich
        _, self.peaks_2 = self.find_peaks()
        peak_differenz_2 = [self.peaks_2[i+1] - self.peaks_2[i] for i in range(len(self.peaks_2)-1)]

        #division durch Null Error beheben, wenn nur ein Peak im Bereich
        if len(peak_differenz_2) == 0:
            print (len(peak_differenz_2))
            hr_bereich = 0

        else:
            durchschnittliche_peak_diff_2 = sum(peak_differenz_2) / len(peak_differenz_2)
            print (len(peak_differenz_2))
            hr_bereich= 60 / (durchschnittliche_peak_diff_2 / 500) # 500 wegen aufnamen der Daten in [2 ms] schritten
        

        return hr_overall, hr_bereich
    
    def plot_heartrate(self, window_size=5):

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
    
    ekg_dict1 = person_data[0]["ekg_tests"][0]
    print(ekg_dict1)
    ekg = EKGdata (ekg_dict1)
    ekg.set_start_und_end_wert (100, 104)

    # print (ekg.df)

    print (ekg.return_Länge_Zeitreihe())
    print (ekg.estimate_hr())
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
