import pwlf
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from scipy import fftpack
from scipy.signal import periodogram
from scipy.integrate import cumtrapz  
from itertools import compress
import pandas as pd
from scipy import stats
from scipy.stats import linregress

#fitting functions
def piecewise_linear_fit (x, y, muscle, participant, plots_folder):
    my_pwlf = pwlf.PiecewiseLinFit(x, y)
    breaks = my_pwlf.fit(2)
    slopes = my_pwlf.calc_slopes()
    intercepts = my_pwlf.intercepts
    print(breaks)
   
    x_hat = np.linspace(x.min(), x.max(), 100)
    y_hat = my_pwlf.predict(x_hat)

    plt.figure()
    plt.plot(x, y, 'o')
    plt.plot(x_hat, y_hat, '-')
    plt.title(participant+'_'+muscle+'_pwlf')
    textbox='Inflection at: '+str(breaks[1])
    plt.figtext (0.5,0.8,textbox)
    plt.show()
    r_squared = my_pwlf.r_squared()
    cor_coef = np.sqrt(r_squared)
    #####Plot export####
    if os.path.isdir (plots_folder + '/' + participant) == False:
        os.mkdir (plots_folder + '/' + participant)
    plt.savefig(plots_folder + '/' + participant + '/' + participant+'_'+muscle+'_pwlf'  + '.png', dpi=300)
    return r_squared, cor_coef, breaks, slopes, intercepts


    
def estimate_coef(x, y): 
    # number of observations/points 
    n = np.size(x) 
      
    # mean of x and y vector 
    m_x, m_y = np.mean(x), np.mean(y) 
      
    # calculating cross-deviation and deviation about x 
    SS_xy = np.sum(y*x) - n*m_y*m_x 
    SS_xx = np.sum(x*x) - n*m_x*m_x 
      
    # calculating regression coefficients 
    b_1 = SS_xy / SS_xx 
    b_0 = m_y - b_1*m_x 
      
    return(b_0, b_1) 

def plot_regression_line(x, y, b): 
    # plotting the actual points as scatter plot 
    plt.scatter(x, y, color = "m", 
               marker = "o", s = 30) 
  
    # predicted response vector 
    print (x)
    y_pred = b[0] + b[1]*np.asarray(x)
  
    # plotting the regression line 
    plt.plot(x, y_pred, color = "g") 
  
    # putting labels 
    plt.xlabel('x') 
    plt.ylabel('y') 
  
    # function to show plot 
    plt.show() 
#fitting functions
########Function for simple linear fitting#####
def lin_func (x, b, c):
    return b * x + c
def lin_fitting (xs, ys, data_type, plots_folder, participant):
    slope, intercept, rvalue, pvalue, stderr = linregress(xs,ys)
    plt.figure()
    plt.plot(xs, ys, '.', label='data')
    fitt_ys = lin_func(xs, slope, intercept)
    plt.plot(xs, lin_func(xs, slope, intercept), '--', label='fitted')
    plt.title('Linear fitted'+data_type)
    textbox = 'r = '+str(rvalue)
    plt.figtext (0.5,0.8,textbox)    
    # print('lin r = '+str(rvalue))
    plt.savefig(plots_folder + '/' + participant + '/' + participant+'_'+data_type+'_linfit'  + '.png', dpi=300)
    return slope, intercept, rvalue, fitt_ys

#######Functions for mono exponential fit######
def mono_exp_func(x, m, t, b):
    return m * np.exp(-t * x) + b

def mono_exp_fitting (xs, ys, data_type, plots_folder, participant):
    # perform the fit
    p0 = (2000, .1, 50) # start with values near those we expect
    params, cv = curve_fit(mono_exp_func, xs, ys, p0, maxfev=100000000)
    m, t, b = params
    # sampleRate = 20_000 # Hz
    # tauSec = (1 / t) / sampleRate
    
    # determine quality of the fit
    squaredDiffs = np.square(ys - mono_exp_func(xs, m, t, b))
    squaredDiffsFromMean = np.square(ys - np.mean(ys))
    rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
    r = np.sqrt(rSquared)
    # print(f"R² = {rSquared}")
    # print(f"mono exponential r = {r}")    
    # plot the results
    plt.figure()
    plt.plot(xs, ys, '.', label="data")
    plt.plot(xs, mono_exp_func(xs, m, t, b), '--', label="fitted")
    plt.title("Mono Exponential fitted"+data_type)
    textbox = 'r = '+str(r)
    plt.figtext (0.5,0.8,textbox)
    plt.savefig(plots_folder + '/' + participant + '/' + participant+'_'+data_type+'_mexpfit'  + '.png', dpi=300)
    fitt_ys = mono_exp_func(xs, m, t, b)
    
    return m, t, b, r, fitt_ys

####### Functions for double exponential fit#####
def bi_exp_func(x, a, b, c, d):
    return a * np.exp(b * x) + c * np.exp(d * x)


def bi_exp_fitting (xs, ys, data_type, plots_folder, participant):
    # perform the fit
    p0 = (700.0, 400.0, 400.0, 1.0) # start with values near those we expect
    params, cv = curve_fit(bi_exp_func, xs, ys, maxfev=100000000)
    a, b, c, d = params
    # sampleRate = 20_000 # Hz
    # tauSec = (1 / t) / sampleRate
    
    # determine quality of the fit
    squaredDiffs = np.square(ys - bi_exp_func(xs, a, b, c, d))
    squaredDiffsFromMean = np.square(ys - np.mean(ys))
    rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
    r = np.sqrt(rSquared)
    # print(f"R² = {rSquared}")
    # print(f"bi exponential r = {r}")
    # plot the results
    plt.figure()
    plt.plot(xs, ys, '.', label="data")
    plt.plot(xs, bi_exp_func(xs, a, b, c, d), '--', label="fitted")
    plt.title("Bi Exponential fitted"+data_type)
    textbox = 'r = '+str(r)
    plt.figtext (0.5,0.8,textbox)
    plt.savefig(plots_folder + '/' + participant + '/' + participant+'_'+data_type+'_bexpfit'  + '.png', dpi=300)
    fitt_ys = bi_exp_func(xs, a, b, c, d)
    return a, b, c, d, r, fitt_ys


def EMG_linear_regresion_fit (time, emg_rms):
    slope, intercept, r_value, p_value, std_err = stats.linregress(time, emg_rms)
    spline_coef = estimate_coef(time, emg_rms)
    plot_regression_line(time, emg_rms, spline_coef)
    emg_spline_df = pd.DataFrame.from_dict({'slope': [slope],'intercept': [intercept],'r-value': [r_value],'p-value': [p_value], 'std_err': [std_err]})
    return emg_spline_df
	
	
	




def plot_regression_line(x, y, b): 
    plt.figure()
    # plotting the actual points as scatter plot 
    plt.scatter(x, y, color = "m", 
               marker = "o", s = 30) 
  
    # predicted response vector 
    print (x)
    y_pred = b[0] + b[1]*np.asarray(x)
  
    # plotting the regression line 
    plt.plot(x, y_pred, color = "g") 
  
    # putting labels 
    plt.xlabel('x') 
    plt.ylabel('y') 
  
    # function to show plot 
    plt.show() 
