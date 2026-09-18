
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 16:04:29 2020

@author: Blai
"""
import sys
sys.path.append('./functions')
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats.stats import pearsonr
import streamlit as st

#Own functions import
from data_imports import *
from data_parsers import *
from filt_func import *
from data_exports import *
from emg_functions import *
from plotting_functions import *
import plotly.express as px
# #To activate plotting using QT manager - This is needed if using Spyder IDE
# try:
#     import IPython
#     shell = IPython.get_ipython()
#     shell.enable_matplotlib(gui='qt')
# except:
#     pass  


# #To avoid FutureWarnings
# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)


            
###########CONSTANT DEFINITION############
data_folder='./Data'
plots_folder = './Plots'
number_of_rows_skipped = 3


##### Filtering constants for Force and EMG ####
data_freq = 1000.0
lowcut = 20.0
highcut = 400.0
lowcut_force = 10.0
filter_order = 4


time_pause = 30

analysis_window = (2*data_freq) 
export_file = './Exported_data.xlsx'



##########END OF CONSTANT DEFINITION#########

######MAIN#######
# print ('Select one of the CF data files...')
# file_list, path_list = find_files_GUI (data_folder, 'CF_FE.txt', id_list)
#LOAD EMG FILE


#Load raw data frame and filter data
uploaded_file = st.file_uploader(
    "Selecciona el fitxer EMG",
    type=["xlsx"]
)

if uploaded_file is not None:

    raw_EMG_data_frame = pd.read_excel(uploaded_file)
    emg_df, emg_df_noAbs = data_filter_butterworth_emg (raw_EMG_data_frame, lowcut, highcut, data_freq, filter_order)


    #Plot EMG and then let select 2 ginput events

    fig = px.line(
        y=emg_df_noAbs['chan1']
    )
    
    st.plotly_chart(
        fig,
        use_container_width=True
)

    pcnt0_emg = st.number_input(
        "Inici contracció",
        min_value=0,
        max_value=len(emg_df_noAbs)-1,
        value=1000
    )
    
    pcnt100_emg = st.number_input(
        "Final contracció",
        min_value=0,
        max_value=len(emg_df_noAbs)-1,
        value=5000
    )
    
    emg_total_frames = pcnt100_emg - pcnt0_emg
    
    pcnt20_emg = int(emg_total_frames*0.2+pcnt0_emg)
    pcnt40_emg = int(emg_total_frames*0.4+pcnt0_emg)
    pcnt60_emg = int(emg_total_frames*0.6+pcnt0_emg)
    pcnt80_emg = int(emg_total_frames*0.8+pcnt0_emg)
    
    for pcnt in [pcnt0_emg, pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg, pcnt100_emg]:
        plt.axvline(pcnt, color='red')
    
    
    #######COMPUTATION OF EMG VARIABLES##########
    
    #Computation of RMS for each test portion
    biceps_RMS = RMS_calculation (emg_df['chan1'], [pcnt0_emg, pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg], [pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg, pcnt100_emg])
    
    #Computation of EMG Frequency variables for each contraction   
    biceps_MNF, biceps_MDF = mean_median_frequency_computation ([pcnt0_emg, pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg], [pcnt20_emg, pcnt40_emg, pcnt60_emg, pcnt80_emg, pcnt100_emg], emg_df_noAbs['chan1'], 'chan1')
    
    
    ########EXPORTING VARIABLES#########
    
    
    export_df = pd.DataFrame({'Biceps_RMS_per_stage': biceps_RMS,
                              'Biceps_MNF_per_stage': biceps_MNF,
                              'Biceps_MDF_per_stage': biceps_MDF
                              })
    xls_df_export_concurrent(export_df, export_file)