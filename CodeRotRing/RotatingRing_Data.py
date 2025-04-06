# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 15:02:08 2025

@author: vaucoi
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import please_plot as pp
import scienceplots


### --------------- Functions & Classes --------------- ###

# def extract_data(path, value):
#     data_frame = pd.read_csv(path, sep=',')
    
#     # Flag unsorted files
#     is_unsorted = not data_frame['Time (s)'].is_monotonic_increasing
#     if is_unsorted:
#         truncated_path = os.path.basename(path)
#         print(f" Unsorted file detected: {truncated_path}")
    
#     # Filter and sort data
#     data_frame = data_frame[data_frame['Intensity'] <= 600]  # Remove high intensities
#     #data_frame = data_frame.sort_values(by='Time (s)')
    
        
#     time = data_frame[['Time (s)']]
#     intensity = data_frame[['Intensity']]
    
#     min_value = data_frame.min(axis=0, )['Intensity'] # index of Beginning data collection
#     # offset = data_frame[['Time(s)']].iloc[start_value].values # Normalize such that beginning is 0
#     dip_time = data_frame['Time (s)'].loc[data_frame['Intensity'] <= (min_value+25)] # Get time where target_temperature is reached
#     fall_time = dip_time.iloc[0]

#     # time = data_frame[['Time(s)']].iloc[start_value:].sub(offset)
#     # temperature = data_frame[['Temperature(C)']].iloc[start_value:]
    
#     return time, intensity, fall_time, (fall_time-300, fall_time+300), min_value


def extract_data(path, value=None, max_time_jump=5.0):
    """
    Processes time-series data with:
    - Automatic removal of time outliers (non-sequential points)
    - Intensity filtering (>600 removal)
    - Fall time detection
    - Analysis window calculation
    
    Args:
        path: CSV file path
        value: Optional parameter (unused)
        max_time_jump: Maximum allowed time difference between consecutive points (seconds)
        
    Returns: (clean_time, clean_intensity, fall_time, window, min_value)
    """
    try:
        df = pd.read_csv(path)
        if not all(col in df.columns for col in ['Time (s)', 'Intensity']):
            raise ValueError("Missing required columns: 'Time (s)' and/or 'Intensity'")
            
        # Filter high intensities
        df = df[df['Intensity'] <= 600].copy()
        
        # Calculate time differences and find outliers
        df['time_diff'] = df['Time (s)'].diff()
        time_outliers = np.abs(df['time_diff']) > max_time_jump
        
        # Remove outliers and keep only clean sequential data
        clean_df = df[~time_outliers].copy()
        
        if len(clean_df) < 2:
            raise ValueError("Not enough valid data points after cleaning")
            
        # Calculate metrics
        clean_time = clean_df['Time (s)']
        clean_intensity = clean_df['Intensity']
        min_value = clean_intensity.min()
        
        # Fall time detection (first point within tolerance of minimum)
        threshold = min_value + 25
        fall_mask = clean_intensity <= threshold
        fall_time = clean_time.loc[fall_mask].iloc[0] if fall_mask.any() else None
        window = (fall_time - 300, fall_time + 300)
        
        return clean_time, clean_intensity, fall_time, window, min_value
    
    except Exception as e:
        print(f"Error processing {path}: {str(e)}")
        return None, None, None, None, None




class Magnet:
    def __init__(self, name, material, pull_rating, outer_diameter, hole_diameter, thickness, marker):
        self.pull_rating = pull_rating    # in lbs
        self.outer_diameter = outer_diameter  # in mm
        self.hole_diameter = hole_diameter    # in mm
        self.thickness = thickness        # in mm
        self.material = material
        self.marker = marker
        
        self.mean_fall_time = None
        self.std_fall_time = None
        self.fall_times = None
        
        # Extract orientation and truncate name
        if "N-S" in name:
            self.orientation = "N-S"
            self.name = name.replace("_N-S", "")
        elif "S-N" in name:
            self.orientation = "S-N"
            self.name = name.replace("_S-N", "")
        else:
            self.orientation = "Not specified"
            self.name = name

    def __str__(self):
        return (
            f"Magnet: {self.name} ({self.orientation})\n"
            f"  - Pull rating: {self.pull_rating} lbs\n"
            f"  - Outer diameter: {self.outer_diameter} mm\n"
            f"  - Hole diameter: {self.hole_diameter} mm\n"
            f"  - Thickness: {self.thickness} mm\n"
            f"Mean Fall time for {self.name} in the {self.orientation}: {self.mean_fall_time} " u"\u00B1" f" {self.std_fall_time}\n"
        )
    # @mean_fall_time.setter
    # def mean_fall_time(self, new_mean):
    #     self.
    
    def volume(self):
        width = self.outer_diameter - self.hole_diameter
        volume = width * self.thickness * 2*np.pi
        return volume
    
    def max_tilt(self, rod_diameter):
        eff_rod_length = np.sqrt(self.hole_diameter**2+self.thickness**2-rod_diameter**2)
        eff_area = self.thickness*self.hole_diameter
        max_angle = np.arcsin(2*eff_rod_length/eff_area)
        return np.degrees(max_angle)
    #def space(self):


        
        

def getMagnet(folder):
    # Magnet(name, material, pull_rating, outer_diameter, hole_diameter, thickness)
    if "5704K16" in folder:
        return Magnet(folder, "AlNiCo", 3.0, 38.10, 28.575, 19.05, marker='X')
    elif "5901K71" in folder:
        return Magnet(folder, "NeoD", 0.6, 25.98, 21.99, 5.00, marker='*')
    elif "5901K72" in folder:
        return Magnet(folder, "NeoD", 1.1, 25.98, 21.99, 10.00, marker='+')
    elif "5901K73" in folder:
        return Magnet(folder, "NeoD", 2.0, 29.99, 16.00, 5.00, marker='v')
    elif "5901K75" in folder:
        return Magnet(folder, "NeoD", 2.0, 35.00, 20.59, 5.00, marker='^')
    else:
        raise ValueError(f"Unknown magnet serial in folder: {folder}")



### --------------- Main Body --------------- ###
fall_times_by_directory = {}

for root, dirs, files in os.walk(r'..\DataRotRing\Finally', topdown=False):
    for path in files:
        #print(os.path.join(root, path))
        time, intensity, fall_time, bounds, min_value = extract_data(os.path.join(root, path), 100)
        truncated_path = os.path.basename(path)
        parent_directory = os.path.basename(root)
        
        if parent_directory not in fall_times_by_directory:
            fall_times_by_directory[parent_directory] = []
            fall_times_by_directory[parent_directory].append(fall_time/1000)
        else: 
            fall_times_by_directory[parent_directory].append(fall_time/1000)


### MAKE RINGS
all_rings = []

for directory, fall_times in fall_times_by_directory.items():
    mean_fall = round(np.mean(fall_times), 3)
    std_fall = round(np.std(fall_times), 3)
    
    ring_magnet = getMagnet(directory)
    ring_magnet.fall_times = fall_times
    ring_magnet.mean_fall_time = mean_fall
    ring_magnet.std_fall_time = std_fall
    all_rings.append(ring_magnet)


### WE HAVE all rings --> do stuff with them
for ring in all_rings:
    print(ring)
    
plt.style.use('ieee')
font = {'size': 10}
plt.rc('font', **font)

pp.plot_fall_time_boxplot(all_rings)
pp.plotOD(all_rings)
pp.plotHD(all_rings)
pp.plotThick(all_rings)
pp.plotPull(all_rings)
    
    



