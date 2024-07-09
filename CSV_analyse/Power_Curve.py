import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

def load_activity(path = "data/activity.csv"):
    df = pd.read_csv(path)
    return df



def find_best_effort (df, time_window, frequenz = 1):

    # Fenstergröße anpassen basierend auf der Frequenz
    adjusted_window = time_window * frequenz
    
    # Rolling mean berechnen mit dem angepassten Fenster
    df['RollingMean'] = df['PowerOriginal'].rolling(window=adjusted_window).mean()
    
    # Maximalen Wert der RollingMean-Spalte finden
    max_value = df['RollingMean'].max()
    
    return max_value



def return_df_for_plotting (df, frequenz = 1, window_lenghts = list(range(1, 1806))):
    df_BestEffort = pd.DataFrame(columns=['Duration [s]', 'Best Effort[W]'])

    for lenght, i in zip (window_lenghts, range(1, 1806)):
        df_BestEffort.loc[i] = [lenght, find_best_effort(df, lenght, frequenz)]

    # print (df_BestEffort["Duration [s]"])
    return df_BestEffort

# [1,5,15,30,45,60,90,120,240,300,360,420,480,540,600,720,840,960,1080,1200,1320,1440,1560,1680,1800]
# [1,5,15,30,45,60,90,120,240,300,360,420,480]



def make_plot_PowerCurve(df, untere_Grenze = 1, obere_Grenze = 300, frequenz = 1 ):
    df_plot = return_df_for_plotting(df, frequenz)

    # Bereich für die Vergrößerung festlegen
    zoom_start = untere_Grenze
    zoom_end = obere_Grenze

    # Erstellen des Plots
    fig = go.Figure()

    # Gesamte Linie hinzufügen
    fig.add_trace(go.Scatter(x=df_plot['Duration [s]'], y=df_plot['Best Effort[W]'], mode='lines', name='Power Curve', line=dict(color='blue', width=2)))

    
    x = df_plot['Duration [s]']
    y = df_plot['Best Effort[W]']
    fig.add_trace(go.Scatter(x=x[(x >= zoom_start) & (x <= zoom_end)], y=y[(x >= zoom_start) & (x <= zoom_end)], mode='lines', name='Zoomed', line=dict(color='lightblue', width=2)))
    fig.add_trace(go.Scatter(x=x[(x < zoom_start) | (x > zoom_end)], y=[None] * len(x[(x < zoom_start) | (x > zoom_end)]), mode='lines', showlegend=False))

    custom_ticks = np.arange(0, 1806, 200)
    custom_tick_labels = [str(int(tick)) for tick in custom_ticks]

    # Layout anpassen
    fig.update_layout(
        title='Power Curve',
        xaxis=dict(title='Duration [s]', tickmode='array', tickvals=custom_ticks, ticktext=custom_tick_labels),
        yaxis=dict(title='Best Effort [W]')
    )

    return fig



def make_plot_PowerCurve_zoomed (df,  untere_Grenze = 1, obere_Grenze = 300, frequenz = 1):
    df_plot = return_df_for_plotting(df, frequenz)

    # Bereich für die Anzeige festlegen
    display_start = untere_Grenze
    display_end = obere_Grenze

    # Daten für den Anzeigebereich filtern
    df_display = df_plot[(df_plot['Duration [s]'] >= display_start) & (df_plot['Duration [s]'] <= display_end)]

    # Erstellen des Plots
    fig = go.Figure()

    # Gesamte Linie hinzufügen
    fig.add_trace(go.Scatter(x=df_display['Duration [s]'], y=df_display['Best Effort[W]'], mode='lines', name='Power Curve', line=dict(color='lightblue', width=2)))

    custom_ticks = np.array ([5, 30, 60, 90, 120, 150, 180, 210, 240, 300,  360,  420,  480, 540,  600,  660,  720,  780,  840,  900,  
                              960, 1020, 1080, 1140, 1200, 1260, 1320, 1380, 1440, 1500, 1560, 1620, 1680, 1740, 1800 ])
    custom_tick_labels = [str(int(tick)) for tick in custom_ticks]

    # Layout anpassen
    fig.update_layout(
        title='Vergrößerte Power Curve',
        xaxis=dict(title='Duration [s]', tickmode='array', tickvals=custom_ticks, ticktext=custom_tick_labels),
        yaxis=dict(title='Best Effort [W]')
    )

    return fig


def make_plot_PowerCurve_Einfach (df, frequenz = 1):

    df_for_plot = return_df_for_plotting (df, frequenz)
    fig = px.line(df_for_plot, x='Duration [s]', y='Best Effort[W]', title='Power Curve')

    fig.show()
    return fig





if __name__ == '__main__':
    print ("hallo von funktions")

    df = load_activity()
    # print(df.head())
    # df['RollingMean'] = df['PowerOriginal'].rolling(window=3).max()
    # print(df.head())

    # print (return_df_for_plotting(df))
    return_df_for_plotting(df)

    print (find_best_effort(df, 10))
    # print (return_df_for_plotting (df))

    make_plot_PowerCurve_Einfach (df)

    df2 = pd.DataFrame(columns=['Spalte1', 'Spalte2'])
    # new_row = {'Spalte1111': 3, 'Spalte2': 3 * 10}
    # df2.loc[1] = [1, 1 * 10]
    # Neue Zeile zum DataFrame hinzufügen
    # df2 = df2._append(new_row, ignore_index=True)
    # print (df2)

