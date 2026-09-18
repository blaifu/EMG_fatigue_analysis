import numpy as np
import copy as copy
from fitting_functions import *

#EMG functions
def review_trial_SD (emg_RMS):
    total_trials = 0
    count_removed_trials = 0
    for intensity in emg_RMS:
        print ('Analysis of the '+str(intensity)+' set:')
        trials_to_remove = list()
        for trial in emg_RMS[intensity]:
            total_trials = total_trials + 1
            emg_RMS_temp = copy.deepcopy(emg_RMS[intensity])
            emg_RMS_temp.remove(trial)
            mean = np.mean(emg_RMS_temp)
            sd = np.std(emg_RMS_temp)
            sd_diff = (trial-mean)/sd
            print ('The trial with value: '+ str(trial)+'is -->'+str(sd_diff)+' SDs above or below the mean')
            if abs(sd_diff) > 3:
                trials_to_remove.append(trial)
                print (str(trial)+ ' added for removal')
                count_removed_trials = count_removed_trials + 1
        if trials_to_remove == []:
            print ('No trials to remove')
        else:
            print ('Trials that will be removed : ' + str(trials_to_remove))
            emg_RMS[intensity].remove(trials_to_remove)
        
    return emg_RMS, count_removed_trials, total_trials

def emg_th_checking (emg_mean_RMS, set_intensities, breaks_emg):
    #vars to retain values form the first linear part of the bi-segmental regresion
    x = list ()
    y = list ()
    for index in range(0, len(emg_mean_RMS)):
        if float(set_intensities[index]) <= float(breaks_emg[1]):
            x.append(float(set_intensities[index]))
            y.append(float(emg_mean_RMS[index]))
    spline_coef = estimate_coef(np.array(x), np.array(y))
    #print (spline_coef)
    #plot_regression_line(x, y, spline_coef)
    y_prediction = spline_coef[0] + spline_coef[1]*np.asarray(set_intensities, dtype=float)
    sd_prediction = np.std(y_prediction)
    last_set_rms_3sd = y_prediction[-1]+sd_prediction*3
    if last_set_rms_3sd < emg_mean_RMS[-1]:
        emg_th = breaks_emg[1]
    else:
        emg_th = 'NaN'
    return emg_th
	
	
	
#EMG treatment functions
def RMS_calculation (EMG_signal, computation_onsets, computation_offsets):
    muscle_RMS = []
    analysis_window = (computation_offsets[0] - computation_onsets[0])/1000
    for i in range(0,len(computation_onsets)):
        muscle_RMS.append ((np.sum(np.square(EMG_signal.iloc[computation_onsets[i]:computation_offsets[i]]))/analysis_window)**0.5)
    return muscle_RMS
    
def compute_mean_set_RMS (RMS_dict):
    set_mean_RMS = list()
    for intensity in RMS_dict:
        set_mean_RMS.append(np.mean(RMS_dict[intensity]))
    return set_mean_RMS
        
def drop_non_used_intensities (grouped_onsets, set_intensities):
    for intensity in grouped_onsets:
        if grouped_onsets[intensity] == []:
            set_intensities.remove(intensity)
    return set_intensities

        
def drop_non_used_intensities_dict (grouped_onsets, dictionary):
    for intensity in grouped_onsets:
        if grouped_onsets[intensity] == []:
            dictionary.pop(intensity)
    return dictionary

def mean_median_frequency_computation (EMG_onsets, EMG_offsets, data_frame_nAbs, muscle):
    mean_freq_data = list()
    median_freq_data = list()
    number_of_plots = len(EMG_onsets)+2
    number_of_rows = 7
    fig, ax = plt.subplots(number_of_rows)
    row_num = 0
    for frame in range(0, len(EMG_onsets)):
        onset = EMG_onsets[frame]
        offset = EMG_offsets[frame]
        sampling_rate = 1000
        signal= data_frame_nAbs.iloc[onset:offset]
        freqs, power = periodogram(signal, fs=sampling_rate, window='hamming')
        ax[row_num].plot(freqs, power)
        ax[row_num].set_title('PSD - Stage: ' + str(frame*20) +' to '+str(frame*20+20) +' - '+muscle)
        recur_sum_power = list ()
        for frame in range(0, len(freqs)):
            if recur_sum_power == []:
                recur_sum_power.append(power[frame])
            else:
                recur_sum_power.append(recur_sum_power[-1]+power[frame])
        median_freq_data.append(list(compress(freqs, recur_sum_power>=recur_sum_power[-1]/2))[0]) 
        mean_freq_data.append(np.sum(freqs*power)/np.sum(power))
        row_num = row_num + 1
        if row_num%7 == 0:
            row_num = 0
            col_num = col_num + 1    
    ax[row_num].set_title('Mean Frequency '+muscle)
    ax[row_num].plot (mean_freq_data)
    row_num = row_num + 1
    if row_num%7 == 0:
        row_num = 0
        col_num = col_num + 1 
    ax[row_num].set_title('Median Frequency '+muscle)
    ax[row_num].plot (median_freq_data)
    return mean_freq_data, median_freq_data