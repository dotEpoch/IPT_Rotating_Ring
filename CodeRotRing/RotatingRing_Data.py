# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 15:02:08 2025

@author: vaucoi
"""

import pandas as pd
import matplotlib.pyplot as plt 

def extract_data(path, value):
    data_frame = pd.read_csv(path, sep=',')
    
    time = data_frame[['Time (s)']]
    intensity = data_frame[['Intensity']]
    
    # start_value = data_frame.idxmin(axis=0, )['Temperature(C)'] # index of Beginning data collection
    # offset = data_frame[['Time(s)']].iloc[start_value].values # Normalize such that beginning is 0
    # peak_time = data_frame['Time(s)'].loc[data_frame['Temperature(C)'] >= value].iloc[1] # Get time where target_temperature is reached


    # time = data_frame[['Time(s)']].iloc[start_value:].sub(offset)
    # temperature = data_frame[['Temperature(C)']].iloc[start_value:]
    
    return time, intensity



path_list = [
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h22m43s.csv"
]

for path in path_list:
    time, intensity = extract_data(path, 100)
    # raw_time, raw_temperature = extract_raw(path)
    # rise_time, rise_temperature = extract_rise(path, 100)
    # osc_time, osc_temperature = extract_osc(path, 100)
    
    ### Raw
    plt.plot(time, intensity)
    plt.title("Raw Data")
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (C)')
    plt.legend()
    plt.style.use('science')
    plt.show()

