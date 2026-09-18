# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 12:34:19 2021

@author: Blai
"""
#IMPORTS
import os
import pandas as pd


#Exports dataframe to xlsx without overwriting
def xls_df_export_concurrent (df, export_file):
    if os.path.isfile(export_file):
        excel_data_frame = pd.read_excel(export_file, index_col=False, dtype=str)
        final_df = df.append(excel_data_frame)
        final_df.to_excel(export_file, header = True, index= False)
    else:
        df.to_excel(export_file, header = True, index= False)
		
		

def export_emgth_variables (export_file, participant, fdp_EMGth, fds_EMGth, fcr_EMGth, 
                            r_squared_fdp, r_squared_fds, r_squared_fcr, 
                            cor_coef_fdp, cor_coef_fds, cor_coef_fcr, 
                            fdp_n_removed_trials, fds_n_removed_trials, 
                            fcr_n_removed_trials, sum_total_trials):
    export_dic = {'ID': [participant], 'fdp_EMGth': [fdp_EMGth], 
                           'fds_EMGth': [fds_EMGth],'fcr_EMGth': [fcr_EMGth], 
                            'fdp Coef det': [r_squared_fdp], 'fds Coef det': [r_squared_fds],
                            'fcr Coef det': [r_squared_fcr],'fdp r': [cor_coef_fdp],
                            'fds r': [cor_coef_fds], 'fcr r': [cor_coef_fcr], 
                            'fdp removed trials': [fdp_n_removed_trials], 
                            'fds removed trilas': [fds_n_removed_trials], 
                            'fcr removed trials': [fcr_n_removed_trials],
                            'total num trials (all muscles)': [sum_total_trials]}
    export_df = pd.DataFrame.from_dict(export_dic, orient='columns')
    if os.path.isfile(export_file):
        excel_df = pd.read_excel(export_file, index_col=False)
        final_df = excel_df.append(export_df)
        final_df.to_excel(export_file, header = True, index= False)
    else:
        export_df.to_excel(export_file, header = True, index= False)
