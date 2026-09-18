# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 17:19:48 2021

@author: Blai
"""
from tkinter import filedialog
from tkinter import *
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
pd.options.mode.chained_assignment = None


#Opens a GUI window to find and select a file
def GUI_file_selection (start_folder):
    root = Tk()
    root.lift()
    filename_path = filedialog.askopenfilename(initialdir=start_folder, title="Select a file")
    root.withdraw()
    return filename_path

#data imports
#read in various data files and loads them to various dataFrames stored in a dictionary in absolute values
def load_data_frame (filename_path, number_of_rows_skipped, raw_df_header):
    skipped = number_of_rows_skipped
    data_frame = pd.read_csv(filename_path, sep='\t', skiprows=skipped, header=None , index_col=False)
    data_frame.columns = raw_df_header
    return data_frame

#Opens a GUI window to find and select a file as loads it as a dataFrame
def GUI_excel_to_dataframe (start_folder, skiped_rows, header_names):
    root = Tk()
    root.lift()
    file_path = filedialog.askopenfilename(initialdir=start_folder, title="Select a file")
    root.withdraw()
    data_frame = pd.read_excel(file_path, skiprows=skiped_rows, index_col=False)
    return data_frame

def load_excel_to_df_from_GUI(start_folder):
    file_path = GUI_excel_to_dataframe (start_folder)
    df = pd.read_excel(file_path, header=0)
    return df

def load_csv_to_df_from_GUI(start_folder, sep, header):
    file_path = GUI_excel_to_dataframe (start_folder)
    df = pd.read_csv(file_path, sep=sep, header=header, index_col=False)
    return df



#splits a file's absolute path into the name of the file and the path to that file
def filename_and_path_splitter (filename_path):
    split_position = filename_path.rfind('/')
    path = filename_path[0:split_position+1]
    filename = filename_path[split_position+1:]
    return path, filename

#creates a list with all files from a root directory which is one level above a selected one with GUI
def find_files_GUI (start_folder, key_word, id_list):
    path, filename = filename_and_path_splitter(GUI_file_selection(start_folder))
    path=path[:-3]
    file_list = []
    path_list = []
    for subject in id_list:
        id_path = path+subject
        for root, directoy, all_files in os.walk(id_path):
            for file in all_files:
                print (file)
                if key_word in file:
                    print('yes')
                    file_list.append(file)
                    path_list.append (id_path)
    return file_list, path_list

#creates a list with all files from a root directory which is one level above a selected one with GUI
def find_files_GUI_same (start_folder, key_word, id_list):
    path, filename = filename_and_path_splitter(GUI_file_selection(start_folder))
    path=path[:]
    file_list = []
    path_list = []
    for root, directoy, all_files in os.walk(path):
        for file in all_files:
            print (file)
            if key_word in file:
                print('yes')
                file_list.append(file)
                path_list.append (path)
    return file_list, path_list

#read in various csv/txt data files and loads them to various dataFrames stored in a dictionary
def load_various_data_frames (path, file_list, skiped, sep, header):
    data_frames={}
    for file in file_list:
            file_path=path + file
            data_frames[file] = pd.read_csv(file_path, sep=sep, skiprows=skiped, header=header, index_col=False)
    return data_frames