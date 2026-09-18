#event detection functions
######### Functions related to contractions onset ##########
def compute_contraction_force_threshold (data_frame):
    MVC = data_frame['Force'].max()
    MVC_25pc = float(MVC)*0.25
    contraction_force_th = MVC_25pc*0.5
    return contraction_force_th, MVC

def find_force_onsets (data_frame, contraction_force_th):
    force_thresholds = abs(data_frame['Force']-contraction_force_th)
    event_list = recursive_near_zero_finder(force_thresholds, data_frame['Force'], 1)
    return event_list




def recursive_near_zero_finder (serie, force_data, cut_value):
    event_list=list()
    last_row = 0
    for row in range(0,serie.shape[0]):
        if row > (last_row+(1000*7)):
            if row < (serie.shape[0]-10):
                if force_data[row]<force_data[row+10]:
                    if serie.iloc[row] <= cut_value:
                        if serie.iloc[row]<serie.iloc[row+1] and serie.iloc[row]<serie.iloc[row-1]:
                            event_list.append(row)
                            last_row = row
        else:
            continue
    return event_list