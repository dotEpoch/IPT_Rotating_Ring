# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 15:02:08 2025

@author: vaucoi
"""

import pandas as pd
import matplotlib.pyplot as plt 
import os
import numpy as np


### --------------- Functions & Classes --------------- ###

def extract_data(path, value):
    data_frame = pd.read_csv(path, sep=',')
    
    time = data_frame[['Time (s)']]
    intensity = data_frame[['Intensity']]
    
    min_value = data_frame.min(axis=0, )['Intensity'] # index of Beginning data collection
    # offset = data_frame[['Time(s)']].iloc[start_value].values # Normalize such that beginning is 0
    dip_time = data_frame['Time (s)'].loc[data_frame['Intensity'] <= (min_value+15)] # Get time where target_temperature is reached
    fall_time = dip_time.iloc[0]

    # time = data_frame[['Time(s)']].iloc[start_value:].sub(offset)
    # temperature = data_frame[['Temperature(C)']].iloc[start_value:]
    
    return time, intensity, fall_time, (fall_time-300, fall_time+300), min_value

class Magnet: 
    def __init__(self, name, pull_rating, outer_diameter, hole_diameter, thickness, ):
        self.name = name
        self.pull_rating = pull_rating
        self.outer_diameter = outer_diameter
        self.hole_diameter = hole_diameter
        self.thickness = thickness
    
    #def set_mean_



### --------------- Main Body --------------- ###
total_fall_times = []
for root, dirs, files in os.walk(r'..\DataRotRing\Finally', topdown=False):
    for path in files:
        print(os.path.join(root, path))
        
        time, intensity, fall_time, bounds, min_value = extract_data(os.path.join(root, path), 100)
        total_fall_times.append(fall_time)
        # raw_time, raw_temperature = extract_raw(path)
        # rise_time, rise_temperature = extract_rise(path, 100)
        # osc_time, osc_temperature = extract_osc(path, 100)
        truncated_path = os.path.basename(path)
        
        ### Raw
        plt.plot(time, intensity, color='red')
        plt.annotate(f"-> Fall Time: {fall_time}ms", (fall_time + 25, min_value))
        plt.xlim(bounds)
        plt.title(f"Raw Data: \n {truncated_path}")
        plt.xlabel('Time (ms)')
        plt.ylabel('Temperature (C)')
        plt.legend()
        #plt.style.use('science')
        plt.show()











# total_fall_timesSN = []
# for path in path_listSN:
#     time, intensity, fall_time, bounds, min_value = extract_data(path, 100)
#     total_fall_timesSN.append(fall_time)
#     # raw_time, raw_temperature = extract_raw(path)
#     # rise_time, rise_temperature = extract_rise(path, 100)
#     # osc_time, osc_temperature = extract_osc(path, 100)
#     truncated_path = os.path.basename(path)
    
#     ### Raw
#     plt.plot(time, intensity, color='red')
#     plt.annotate(f"-> Fall Time: {fall_time}ms", (fall_time + 25, min_value))
#     plt.xlim(bounds)
#     plt.title(f"Raw Data: \n {truncated_path}")
#     plt.xlabel('Time (ms)')
#     plt.ylabel('Temperature (C)')
#     plt.legend()
#     #plt.style.use('science')
#     plt.show()
    
# total_fall_timesNS = []
# for path in path_listNS:
#     time, intensity, fall_time, bounds, min_value = extract_data(path, 100)
#     total_fall_timesNS.append(fall_time)
#     # raw_time, raw_temperature = extract_raw(path)
#     # rise_time, rise_temperature = extract_rise(path, 100)
#     # osc_time, osc_temperature = extract_osc(path, 100)
#     truncated_path = os.path.basename(path)
    
#     ### Raw
#     plt.plot(time, intensity, color='blue')
#     plt.annotate(f"-> Fall Time: {fall_time}ms", (fall_time + 25, min_value))
#     plt.xlim(bounds)
#     plt.title(f"Raw Data: \n {truncated_path}")
#     plt.xlabel('Time (ms)')
#     plt.ylabel('Temperature (C)')
#     plt.legend()
#     #plt.style.use('science')
#     plt.show()
    
# # plot final
# plt.scatter(np.arange(len(path_listNS)), total_fall_timesNS, color='blue', label='N-S')
# plt.axhline(y=np.mean(total_fall_timesNS), color='blue', linestyle='--', alpha=0.6)
# plt.scatter(np.arange(len(path_listSN)), total_fall_timesSN, color='red', label='S-N')
# plt.axhline(y=np.mean(total_fall_timesSN), color='red', linestyle='--', alpha=0.6)
# plt.grid()
# plt.title("Total Times")
# plt.xlabel('Sample #')
# plt.ylabel('Fall Time (ms)')
# plt.legend()
# #plt.style.use('science')
# plt.show()

