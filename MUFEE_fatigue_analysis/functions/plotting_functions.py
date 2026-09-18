import matplotlib.pyplot as plt
import os

#data_plotting functions
def plot_export_RMS_clean (set_intensities, emg_RMS_clean, plots_folder, participant, muscle):
    x = list()
    y = list()
    num = 0
    for intensity in set_intensities:
        for trial in emg_RMS_clean[intensity]:
            y.append(trial)
            x.append(num+1)
            num = num + 1
    plt.figure()
    plt.scatter(x,y)
    plt.title(participant+'_'+muscle+'_RMS_clean')
    if os.path.isdir (plots_folder + '/' + participant) == False:
        os.mkdir (plots_folder + '/' + participant)
    plt.savefig(plots_folder + '/' + participant + '/' + participant + '_' + muscle + '_RMS_clean'  + '.png', dpi=300)


def plot_export_RMS_clean (set_intensities, emg_RMS_clean, plots_folder, participant, muscle):
    x = list()
    y = list()
    num = 0
    for intensity in set_intensities:
        for trial in emg_RMS_clean[intensity]:
            y.append(trial)
            x.append(num+1)
            num = num + 1
    plt.figure()
    plt.scatter(x,y)
    plt.title(participant+'_'+muscle+'_RMS_clean')
    if os.path.isdir (plots_folder + '/' + participant) == False:
        os.mkdir (plots_folder + '/' + participant)
    plt.savefig(plots_folder + '/' + participant + '/' + participant + '_' + muscle + '_RMS_clean'  + '.png', dpi=300)


def plot_export_force (force_data, emg_onsets, emg_offsets, force_requests, participant, plots_folder):
    plt.figure ()
    plt.plot(force_data)
    for intensity in emg_onsets:
        for line in emg_onsets[intensity]:
            plt.axvline(line, color='green')
        for line in emg_offsets[intensity]:
            plt.axvline(line, color='red')
    for force in force_requests:
        plt.axhline (force, color = 'purple')
    plt.title(participant + '_force_with_on-offsets')
    if os.path.isdir (plots_folder + '/' + participant) == False:
        os.mkdir (plots_folder + '/' + participant)
    plt.savefig(plots_folder + '/' + participant + '/' + participant + '_force'  + '.png', dpi=300)

