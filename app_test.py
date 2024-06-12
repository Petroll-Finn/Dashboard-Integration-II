# Befehl um selectbox in Menu hinzuzufügen
select_event = st.sidebar.selectbox('How do you want to find data?',
                                    ['By event name', 'By GPS'])

if select_event == 'By GPS':
    # -- Set a GPS time:        
    str_t0 = st.sidebar.text_input('GPS Time', '1126259462.4')    # -- GW150914
    t0 = float(str_t0)

    st.sidebar.markdown("""
    Example times in the H1 detector:
    * 1126259462.4    (GW150914) 
    * 1187008882.4    (GW170817) 
    * 1128667463.0    (hardware injection)
    * 1132401286.33   (Koi Fish Glitch) 
    """)

else:
    chosen_event = st.sidebar.selectbox('Select Event', eventlist)
    t0 = datasets.event_gps(chosen_event)
    detectorlist = list(datasets.event_detectors(chosen_event))
    detectorlist.sort()
    st.subheader(chosen_event)
    st.write('GPS:', t0)


# Befehl um sidebar im Menu zu erstellen
st.sidebar.markdown('## Set Plot Parameters')
dtboth = st.sidebar.slider('Time Range (seconds)', 0.1, 8.0, 1.0)  # min, max, default
dt = dtboth / 2.0

st.sidebar.markdown('#### Whitened and band-passed data')
whiten = st.sidebar.checkbox('Whiten?', value=True)
freqrange = st.sidebar.slider('Band-pass frequency range (Hz)', min_value=10, max_value=maxband, value=(30,400))