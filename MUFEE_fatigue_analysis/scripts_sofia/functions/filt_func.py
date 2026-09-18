# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:15:08 2021

@author: Blai
"""

from scipy.signal import butter, lfilter, filtfilt
from scipy.signal import freqz
import numpy as np

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
    return y
	

def data_filter_butterworth (data_frame, lowcut, lowcut_force, highcut, data_freq, filter_order):
    #data_frame[-1:] = 0
    filt_data_frame = data_frame[:-1].copy(deep=True)
    filt_data_frame_noAbs = data_frame[:-1].copy(deep=True)
    filt_data_frame['Force'] = np.abs(butter_bandpass_filter(data_frame['Force'].dropna(), lowcut_force, highcut, data_freq, filter_order, 'low'))            
    filt_data_frame['Biceps'] = np.abs(butter_bandpass_filter(data_frame['Biceps'].dropna(), lowcut, highcut, data_freq, filter_order, 'band'))            
    filt_data_frame_noAbs['Force'] = butter_bandpass_filter(data_frame['Force'].dropna(), lowcut_force, highcut, data_freq, filter_order, 'low')            
    filt_data_frame_noAbs['Biceps'] = butter_bandpass_filter(data_frame['Biceps'].dropna(), lowcut, highcut, data_freq, filter_order, 'band')            
    
    return filt_data_frame, filt_data_frame_noAbs

def data_filter_butterworth_emg (data_frame, lowcut, highcut, data_freq, filter_order):
    #data_frame[-1:] = 0
    filt_data_frame = data_frame[:].copy(deep=True)
    filt_data_frame_noAbs = data_frame[:].copy(deep=True)
    filt_data_frame['chan1'] = np.abs(butter_bandpass_filter(data_frame['chan1'].dropna(), lowcut, highcut, data_freq, filter_order, 'band'))            
    filt_data_frame_noAbs['chan1'] = butter_bandpass_filter(data_frame['chan1'].dropna(), lowcut, highcut, data_freq, filter_order, 'band')            
    
    return filt_data_frame, filt_data_frame_noAbs