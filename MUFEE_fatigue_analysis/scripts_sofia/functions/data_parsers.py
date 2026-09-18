# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 17:19:48 2021

@author: Blai
"""
import pandas as pd



#Returns the index of an element given a value
def find_serie_index_from_value (serie, value):
   index = serie[(serie == value) == True].index[0]
   return index

#Returns de index of each nearest zero crossing value
def zero_crossing_indexer (serie):
    crossing_index = []
    iteration = 0
    prev_frame = 1
    for frame in serie:
        if iteration != 0:
            if (prev_frame <= 0 and frame >= 0) or (prev_frame >= 0 and frame <= 0):
                if abs(prev_frame) > abs(frame):
                    crossing_index.append(iteration)
                else:
                    crossing_index.append(iteration-1)
                iteration = iteration + 1
                prev_frame = frame
            else:
                iteration = iteration + 1
                prev_frame = frame
        else: 
            prev_frame = frame
            iteration = iteration + 1
    return crossing_index

#Find closest value when only positive values in the series
def find_closest_value_index (serie, value):
    closest_index = abs(serie-value).idxmin()
    return closest_index
    


#data parser   
#splits a file's absolute path into the name of the file and the path to that file
def filename_and_path_splitter (filename_path):
    split_position = filename_path.rfind('/')
    path = filename_path[0:split_position+1]
    filename = filename_path[split_position+1:]
    return path, filename
#data parser
def filename_data_splitter (filename):
    filename_data = filename.split('_')
    participant = filename_data[0]
    session = filename_data[1]
    test = filename_data[2]
    trial = 1
    data_type = filename_data[3][0:2]
    return participant, session, test, trial, data_type
#data parser
def filename_data_splitter_AO_BF (filename):
    filename_data = filename.split('_')
    participant = filename_data[0]
    test = filename_data[1]
    trial = 1
    data_type = filename_data[2][0:2]
    return participant, test, trial, data_type

#data parser
def erase_last_string_part_from_list (file_list, splitting_char):
    part_name_list = []
    for file in file_list:
        split_position = file.rfind(splitting_char)
        part_name_list.append(file[:split_position])
    return part_name_list

#data parser
#creates a list with all files that contain the subtring
def find_files_containing_substring_numOfChar (path, substring, length):
    file_list = []
    for root, directoy, all_files in os.walk(path):
        for file in all_files:
            if substring in file and len(file)==length:
                file_list.append(file)
    return file_list