import streamlit as st
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.signal import butter, lfilter, filtfilt
from scipy.signal import freqz
from scipy.signal import periodogram

#FUNCTIONS#
def butter_bandpass(lowcut, highcut, fs, order, filter_type):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    if filter_type == 'band':
        b, a = butter(order, [low, high], btype='bandpass')
    elif filter_type == 'low':
        b, a = butter(order, low, btype='lowpass')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order, filter_type):
    b, a = butter_bandpass(lowcut, highcut, fs, order, filter_type)
    y = filtfilt(b, a, data)
    plt.figure()
    plt.plot(y)
    return y

def data_filter_butterworth_emg (data_frame, lowcut, highcut, data_freq, filter_order):
    filt_data_frame = butter_bandpass_filter(data_frame.dropna(), lowcut, highcut, data_freq, filter_order, 'band')                  
    return filt_data_frame

def RMS_calculation (EMG_signal, computation_onsets, computation_offsets):
    muscle_RMS = []
    analysis_window = (computation_offsets[0] - computation_onsets[0])/1000
    for i in range(0,len(computation_onsets)):
        muscle_RMS.append ((np.sum(np.square(EMG_signal.iloc[computation_onsets[i]:computation_offsets[i]]))/analysis_window)**0.5)
    return muscle_RMS
def mean_median_frequency_computation (EMG_onsets, EMG_offsets, data_frame_nAbs, muscle):
    mean_freq_data = list()
    median_freq_data = list()
    number_of_plots = len(EMG_onsets)+2
    number_of_rows = 30
    number_of_cols = 3
    fig, ax = plt.subplots(number_of_rows, number_of_cols)
    col_num = 0
    row_num = 0
    for frame in range(0, len(EMG_onsets)):
        onset = EMG_onsets[frame]
        offset = EMG_offsets[frame]
        sampling_rate = 1000
        signal= data_frame_nAbs.iloc[onset:offset]
        freqs, power = periodogram(signal, fs=sampling_rate, window='hamming')
        ax[row_num][col_num].plot(freqs, power)
        ax[row_num][col_num].set_title('PSD - Stage: ' + str(frame*20) +' to '+str(frame*20+20) +' - '+muscle)
        recur_sum_power = list ()
        for frame in range(0, len(freqs)):
            if recur_sum_power == []:
                recur_sum_power.append(power[frame])
            else:
                recur_sum_power.append(recur_sum_power[-1]+power[frame])
        median_freq_data.append(list(compress(freqs, recur_sum_power>=recur_sum_power[-1]/2))[0]) 
        mean_freq_data.append(np.sum(freqs*power)/np.sum(power))
        row_num = row_num + 1
        if row_num >29:
            row_num = 0
            col_num = col_num + 1
    return mean_freq_data, median_freq_data
##################################
########CONSTANTS#################
data_freq = 1000.0
lowcut = 20.0
highcut = 400.0
filter_order = 4





###################################
###############MAIN##################
st.title("EMG FATIGUE ANALYSIS APP")

st.markdown("""Aquesta APP serveig per fer l'anàlisi d'un fitxes d'EMG en tasques de fatiga a través de contraccions continues""")


uploaded_file = st.file_uploader(
    "Selecciona el fitxer EMG",
    type=["xlsx"]
)

if uploaded_file is not None:
    raw_EMG_data_frame = pd.read_excel(uploaded_file) 
    #FILTRATGE DADES
    filt_data = data_filter_butterworth_emg(raw_EMG_data_frame['chan1'], lowcut, highcut, data_freq, filter_order)
    
    # Crear figura
    fig = px.line(
        raw_EMG_data_frame,
        y='chan1',
        title='Senyal EMG'
    )

    #SELECTOR FINESTRA
    st.plotly_chart(fig, use_container_width=True)
    pcnt0_emg = st.number_input(
        "Inici contracció",
        min_value=0,
        max_value=len(filt_data),
        value=1000)
    
    pcnt100_emg = st.number_input(
        "Final contracció",
        min_value=0,
        max_value=len(filt_data),
        value=5000)
    
    emg_total_frames = pcnt100_emg - pcnt0_emg
    
    pcnt20_emg = int(emg_total_frames*0.2+pcnt0_emg)
    pcnt40_emg = int(emg_total_frames*0.4+pcnt0_emg)
    pcnt60_emg = int(emg_total_frames*0.6+pcnt0_emg)
    pcnt80_emg = int(emg_total_frames*0.8+pcnt0_emg)
    
    onsets = [pcnt0_emg, pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg]
    offsets = [pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg, pcnt100_emg]
    # for pcnt in [pcnt0_emg, pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg, pcnt100_emg]:
    #     plt.axvline(pcnt, color='red')
    
    
    # #######COMPUTATION OF EMG VARIABLES##########
    
    # #Computation of RMS for each test portion
    biceps_RMS = RMS_calculation (filt_data['chan1'], [pcnt0_emg, pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg], [pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg, pcnt100_emg])
    
    # #Computation of EMG Frequency variables for each contraction   
    RMS = RMS_calculation (filt_data, onsets, offsets)
    MNF, MDF = mean_median_frequency_computation (onsets, offsets, filt_data, 'chan1')
    
    st.table(RMS)
    st.table(MDF)
    st.table(MNF)
    # ########EXPORTING VARIABLES#########
    
    
    # export_df = pd.DataFrame({'Biceps_RMS_per_stage': biceps_RMS,
    #                           'Biceps_MNF_per_stage': biceps_MNF,
    #                           'Biceps_MDF_per_stage': biceps_MDF
    #                           })
    # xls_df_export_concurrent(export_df, export_file)