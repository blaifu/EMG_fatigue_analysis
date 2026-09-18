import streamlit as st
import pandas as pd
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

st.title("EMG FATIGUE ANALYSIS APP")

st.markdown("""Aquesta APP serveig per fer l'anàlisi d'un fitxes d'EMG en tasques de fatiga a través de contraccions continues""")


uploaded_file = st.file_uploader(
    "Selecciona el fitxer EMG",
    type=["xlsx"]
)

if uploaded_file is not None:
    raw_EMG_data_frame = pd.read_excel(uploaded_file) 
    # Crear figura
    fig, ax = plt.subplots(figsize=(12,4))
    ax.plot(raw_EMG_data_frame['chan1'])
    ax.set_xlabel('Mostres')
    ax.set_ylabel('EMG')
    ax.set_title('Senyal EMG')

# Mostrar a Streamlit
st.pyplot(fig)
    # pcnt0_emg = st.number_input(
    #     "Inici contracció",
    #     min_value=0,
    #     max_value=len(emg_df_noAbs)-1,
    #     value=1000
    # )
    
    # pcnt100_emg = st.number_input(
    #     "Final contracció",
    #     min_value=0,
    #     max_value=len(emg_df_noAbs)-1,
    #     value=5000
    # )
    
    # emg_total_frames = pcnt100_emg - pcnt0_emg
    
    # pcnt20_emg = int(emg_total_frames*0.2+pcnt0_emg)
    # pcnt40_emg = int(emg_total_frames*0.4+pcnt0_emg)
    # pcnt60_emg = int(emg_total_frames*0.6+pcnt0_emg)
    # pcnt80_emg = int(emg_total_frames*0.8+pcnt0_emg)
    
    # for pcnt in [pcnt0_emg, pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg, pcnt100_emg]:
    #     plt.axvline(pcnt, color='red')
    
    
    # #######COMPUTATION OF EMG VARIABLES##########
    
    # #Computation of RMS for each test portion
    # biceps_RMS = RMS_calculation (emg_df['chan1'], [pcnt0_emg, pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg], [pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg, pcnt100_emg])
    
    # #Computation of EMG Frequency variables for each contraction   
    # biceps_MNF, biceps_MDF = mean_median_frequency_computation ([pcnt0_emg, pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg], [pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg, pcnt100_emg], emg_df_noAbs['chan1'], 'chan1')
    
    
    # ########EXPORTING VARIABLES#########
    
    
    # export_df = pd.DataFrame({'Biceps_RMS_per_stage': biceps_RMS,
    #                           'Biceps_MNF_per_stage': biceps_MNF,
    #                           'Biceps_MDF_per_stage': biceps_MDF
    #                           })
    # xls_df_export_concurrent(export_df, export_file)