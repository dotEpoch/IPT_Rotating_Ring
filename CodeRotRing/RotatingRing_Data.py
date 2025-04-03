# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 15:02:08 2025

@author: vaucoi
"""

import pandas as pd
import matplotlib.pyplot as plt 
import os
import numpy as np

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



path_listSN = [
    #"../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h22m43s.csv",

    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h43m05s.csv",
    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h50m30s.csv",
    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h53m18s.csv",
    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h55m38s.csv",
    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h58m03s.csv",
    
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h03m38s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h00m46s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-15h58m00s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h22m43s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h16m59s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h13m59s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h12m48s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h08m11s.csv"
]

path_listNS = [
    #"../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_S-N_774mm_2025-03-27-16h22m43s.csv",

    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h43m05s.csv",
    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h50m30s.csv",
    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h53m18s.csv",
    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h55m38s.csv",
    # "../DataRotRing/400mm_Medium_Rod_(1msRes)/NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_2025-04-01-15h58m03s.csv",
    
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-26-15h28m54s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-26-15h24m14s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-27-15h53m45s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-26-15h50m50s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-26-15h47m18s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-26-15h44m36s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-26-15h42m41s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-26-15h40m30s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-26-15h38m25s.csv",
    "../DataRotRing/NeoD_1.1_25.98mm_21.99mm_10.00mm_(5901K72)_N-S_774mm_2025-03-26-15h31m12s.csv"
]


total_fall_timesSN = []
for path in path_listSN:
    time, intensity, fall_time, bounds, min_value = extract_data(path, 100)
    total_fall_timesSN.append(fall_time)
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
    
total_fall_timesNS = []
for path in path_listNS:
    time, intensity, fall_time, bounds, min_value = extract_data(path, 100)
    total_fall_timesNS.append(fall_time)
    # raw_time, raw_temperature = extract_raw(path)
    # rise_time, rise_temperature = extract_rise(path, 100)
    # osc_time, osc_temperature = extract_osc(path, 100)
    truncated_path = os.path.basename(path)
    
    ### Raw
    plt.plot(time, intensity, color='blue')
    plt.annotate(f"-> Fall Time: {fall_time}ms", (fall_time + 25, min_value))
    plt.xlim(bounds)
    plt.title(f"Raw Data: \n {truncated_path}")
    plt.xlabel('Time (ms)')
    plt.ylabel('Temperature (C)')
    plt.legend()
    #plt.style.use('science')
    plt.show()
    
# plot final
plt.scatter(np.arange(len(path_listNS)), total_fall_timesNS, color='blue', label='N-S')
plt.axhline(y=np.mean(total_fall_timesNS), color='blue', linestyle='--', alpha=0.6)
plt.scatter(np.arange(len(path_listSN)), total_fall_timesSN, color='red', label='S-N')
plt.axhline(y=np.mean(total_fall_timesSN), color='red', linestyle='--', alpha=0.6)
plt.grid()
plt.title("Total Times")
plt.xlabel('Sample #')
plt.ylabel('Fall Time (ms)')
plt.legend()
#plt.style.use('science')
plt.show()

