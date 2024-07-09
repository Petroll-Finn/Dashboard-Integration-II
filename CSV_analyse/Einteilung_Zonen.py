import pandas as pd
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def load_activity(path="data/activity.csv"):
    df = pd.read_csv(path)
    return df


def mittelwert (df):
    mittelwert_Leistung = df['PowerOriginal'].mean()
    #print(mittelwert_Leistung)

    return mittelwert_Leistung


def max_Leistung (df):
    max_Leistung = df['PowerOriginal'].max()
    #print(max_Leistung)
    return max_Leistung


def max_Herzfrequenz (df):
    max_Herzfrequenz = df["HeartRate"].max()
    # print(max_Herzfrequenz)
    return max_Herzfrequenz


def time():
    points = 1804
    total_seconds = 30 * 60 + 5
    time_points = np.linspace(0, total_seconds, points)
    return (time_points)


def calc_Zones (max_HR):
    list_Zones = [0.5*max_HR, 0.6*max_HR, 0.7*max_HR, 0.8*max_HR, 0.9*max_HR, 1*max_HR]
    # print (list_Zones)

    return list_Zones




def make_plot_EKG (df, max_HR):
    
    liste_mit_zonen = calc_Zones (max_HR)

    fig = go.Figure()

    # Erstellen der Subplots mit zwei y-Achsen
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=time(), y= df['HeartRate'], name="EKG-Daten", line=dict(color='red')), secondary_y=False,)
    fig.add_trace(go.Scatter(x=time(), y= df['PowerOriginal'], name="Power-Daten", line=dict(color='blue')), secondary_y=True,)
    
    
    
    fig.update_layout(
        title_text="EKG und Power ",
        xaxis_title="time [s]",
        yaxis_title="Heart Rate [BPM]",
        yaxis2_title="Power [w]",
        legend = dict(  x=1.15,       # Position der Legende auf der x-Achse (rechts vom Plot)
                        y=1,          # Position der Legende auf der y-Achse (oben)
                        xanchor='left', # Legende von der linken Seite der Position ausrichten
                        yanchor='top', # Legende von der oberen Seite der Position ausrichten
                        bordercolor='grey', # Randfarbe der Legende
                        borderwidth=2  # Randbreite der Legende
        ))
    
    fig.add_shape(
    type="rect",
    x0=0, x1=1805,  # Zeit in Sekunden
    y0=liste_mit_zonen[0], y1=liste_mit_zonen[1],  # Y-Achsenbereich, um den gesamten Diagramm zu überdecken
    xref='x', yref='y',
    fillcolor="grey",
    opacity=1,
    layer="below",
    line_width=1,
    showlegend=True,
    name='Zone 1 (50-60 %)'
    )

    fig.add_shape(
    type="rect",
    x0=0, x1=1805,  # Zeit in Sekunden
    y0=liste_mit_zonen[1], y1=liste_mit_zonen[2],  # Y-Achsenbereich, um den gesamten Diagramm zu überdecken
    xref='x', yref='y',
    fillcolor="lightgreen",
    opacity=1,
    layer="below",
    line_width=1,
    showlegend=True,
    name='Zone 2 (60-70 %)'
    )

    fig.add_shape(
    type="rect",
    x0=0, x1=1805,  # Zeit in Sekunden
    y0=liste_mit_zonen[2], y1=liste_mit_zonen[3],  # Y-Achsenbereich, um den gesamten Diagramm zu überdecken
    xref='x', yref='y',
    fillcolor="green",
    opacity=0.5,
    layer="below",
    line_width=1,
    showlegend=True,
    name='Zone 3 (70-80 %)'
    )

    fig.add_shape(
    type="rect",
    x0=0, x1=1805,  # Zeit in Sekunden
    y0=liste_mit_zonen[3], y1=liste_mit_zonen[4],  # Y-Achsenbereich, um den gesamten Diagramm zu überdecken
    xref='x', yref='y',
    fillcolor="yellow",
    opacity=0.5,
    layer="below",
    line_width=1,
    showlegend=True,
    name='Zone 4 (80-90 %)'
    )

    fig.add_shape(
    type="rect",
    x0=0, x1=1805,  # Zeit in Sekunden
    y0=liste_mit_zonen[4], y1=liste_mit_zonen[5],  # Y-Achsenbereich, um den gesamten Diagramm zu überdecken
    xref='x', yref='y',
    fillcolor="red",
    opacity=0.3,
    layer="below",
    line_width=1,
    showlegend=True,
    name='Zone 5 (90-100 %)'
    )

    
    # fig.show()
    return fig


def calc_time_and_average_in_Zones (df,max_HR):
    heart_rate = df['HeartRate']
    power = df ['PowerOriginal']
    # print (heart_rate)
    list = calc_Zones (max_HR)
    Zone1= 0
    Zone2= 0
    Zone3= 0
    Zone4= 0
    Zone5= 0

    Werte_Zone1 = []
    Werte_Zone2 = []
    Werte_Zone3 = []
    Werte_Zone4 = []
    Werte_Zone5 = []

    for i, a in zip (heart_rate, power):
        if i >= list [0] and i < list[1]:
            Zone1 += 1
            Werte_Zone1.append (a)
        if i >= list [1] and i < list[2]:
            Zone2 += 1
            Werte_Zone2.append (a)
        if i >= list [2] and i < list[3]:
            Zone3 += 1
            Werte_Zone3.append (a)
        if i >= list [3] and i < list[4]:
            Zone4 += 1
            Werte_Zone4.append (a)
        if i >= list [4] and i < list[5]:
            Zone5 += 1
            Werte_Zone5.append (a)

    if len(Werte_Zone1) == 0:
        mean1 = 0
    else:
        mean1 = sum(Werte_Zone1) / len(Werte_Zone1)
    
    if len(Werte_Zone2) == 0:
        mean2 = 0
    else:
        mean2 = sum(Werte_Zone2) / len(Werte_Zone2)
    
    if len(Werte_Zone3) == 0:
        mean3 = 0
    else:
        mean3 = sum(Werte_Zone3) / len(Werte_Zone3)
    
    if len(Werte_Zone4) == 0:
        mean4 = 0
    else:
        mean4 = sum(Werte_Zone4) / len(Werte_Zone4)

    if len(Werte_Zone5) == 0:
        mean5 = 0
    else:
        mean5 = sum(Werte_Zone5) / len(Werte_Zone5)
    
    dict = {"Zone": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5" ], 
            "verbrachte Zeit in Minuten ": [round ((Zone1/60),2), round ((Zone2/60),2), round ((Zone3/60),2), round ((Zone4/60),2), round ((Zone5/60),2)],
            "Durchschnittliche Leistung in Watt": [round(mean1,2), round (mean2,2), round(mean3,2), round(mean4, 2), round(mean5, 2)]}
    
    return dict



if __name__ == '__main__':
    
    df = load_activity()
    # print (max_Herzfrequenz(df))

    print (calc_time_and_average_in_Zones(df,130))
    
    
    # calc_time_in_Zones (df, 190)
    # calc_Zones(100)
    # print (mittelwert(df))
    # print (max_Leistung (df))
    # make_plot_EKG(df, 210)





