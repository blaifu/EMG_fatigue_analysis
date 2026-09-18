def count_number_of_sets():
    last_set = input ('Introduce the last % of MVC that the participant completed: ')
    number_of_sets = (int(last_set)-25)/3
    return number_of_sets

def group_set_onsets(num_sets, force_onsets):
    grouped_trials={'25':[], '28':[], '31':[], '34':[], '37':[], '40':[], 
                  '43':[], '46':[], '49':[], '52':[], '55':[], '58':[],
                  '61':[], '64':[], '67':[], '70':[], '73':[], '76':[], 
                  '79':[], '82':[], '85':[], '88':[], '91':[], '94':[],
                  '97':[], '100':[]}
    num_trials = int(int(num_sets) * 5)
    intensity = 25
    for set_start in range (0,num_trials+5,5):
        set_end = set_start+5
        grouped_trials[str(intensity)] = force_onsets[set_start:set_end]
        intensity = intensity + 3
    return grouped_trials



def compute_requested_force_output (set_intenisities, MVC):
    intensities = list()
    for intensity in set_intensities:
        intensities.append(float(intensity))
        intensities[-1] = intensities[-1]*float(MVC)/100
    return intensities
    



def search_most_sable_two_sec (force_data, grouped_onsets, analysis_window, contraction_time, force_requests):
    emg_onsets = {}
    force_request_index = 0
    trial_counter = 0
    for intensity in grouped_onsets:
        print ('Set intensity: '+str(intensity))
        emg_onsets[intensity] = list()
        for trial_start in grouped_onsets[intensity]:
            print ('Trial start: ' + str(trial_start))
            contraction_end = int(trial_start) + contraction_time
            print ('Contraction end: ' + str(contraction_end))
            moving_averaged_force = {}
            for frame in range (int(trial_start), (contraction_end - int(analysis_window))):
                moving_averaged_force[frame] = np.abs(np.mean (force_data[frame:int(frame+analysis_window)])-force_requests[force_request_index])
            #we save the index (start of contraction) for the window with the closest mean value to the requested force
            key_list = list(moving_averaged_force.keys())
            val_list = list(moving_averaged_force.values())
            emg_onsets[intensity].append(key_list[val_list.index(min(val_list))])
            trial_counter = trial_counter + 1
            if trial_counter == 5:
                force_request_index = force_request_index + 1
                trial_counter = 0
            #plt.figure()
            #plt.plot(key_list, val_list)
    return emg_onsets
                            
    


def compute_grouped_offsets (grouped_onsets, analysis_window):
    grouped_offsets = {'25':[], '28':[], '31':[], '34':[], '37':[], '40':[], 
                  '43':[], '46':[], '49':[], '52':[], '55':[], '58':[],
                  '61':[], '64':[], '67':[], '70':[], '73':[], '76':[], 
                  '79':[], '82':[], '85':[], '88':[], '91':[], '94':[],
                  '97':[], '100':[]}
    for intensity in grouped_onsets:
        for trial in grouped_onsets[intensity]:
            print('EMG_onset is: '+str(trial))
            print ('EMG_offset should be: '+str (trial+2000))
            grouped_offsets[intensity].append(trial+analysis_window)
            print ('EMG_offset is: '+ str(grouped_offsets[intensity][-1]))
    return grouped_offsets
