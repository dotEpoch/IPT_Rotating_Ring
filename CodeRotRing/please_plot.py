# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 17:27:51 2025

@author: vince
"""

import pandas as pd

import os
import numpy as np
import scienceplots
import matplotlib.pyplot as plt
import matplotlib
import scienceplots

plt.rcParams.update({'axes.titlesize': 'Large'})

### --------------- Helper Functions ------------ ###

def plot_magnet_fall_times(ring_magnet):
    plt.plot(np.arange(len(ring_magnet.fall_times)), ring_magnet.fall_times, color='blue')
    plt.axhline(ring_magnet.mean_fall_time, linestyle='--', color='navy', alpha=0.5)
    #plt.xlim(bounds)
    plt.title(f"Fall Times {ring_magnet.name} for {ring_magnet.orientation} orientation")
    plt.xlabel('Sample #')
    plt.ylabel('Fall Time')
    #plt.legend()
    plt.grid()
    plt.show()
    


""" >>> plot_fall_time_boxplot <<<
Creates a box plot of fall times for different magnet serial numbers.

Args:
    magnet_fall_times (dict): Dictionary where:
        - keys are magnet serial numbers (e.g., '5901K75')
        - values are lists of fall times for that magnet
"""  
def plot_fall_time_boxplot(all_rings):
    labels = []
    data = []
    
    for ring in all_rings:
        labels.append(ring.name)
        data.append(ring.fall_times)  # Filter out None values
        
            # pos = start_pos + i * (box_width + spacing) + box_width/2
            # x_positions.append(pos)
    
    plt.figure(figsize=(5, 4))
    box = plt.boxplot(data, 
                      patch_artist=True, 
                      labels=labels,
                      medianprops={'linewidth':0},
                      meanline=True,
                      showmeans=True,
                      meanprops={'linestyle': '-', 'color': 'black', 'linewidth':1}
                      )
    if len(labels) > 5:
        plt.xticks(rotation=45)
    
    # Customize colors
    colors = color=plt.cm.tab20(np.arange(len(box)+2))
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
        
    plt.title('Fall Time Distribution by Magnet Serial Number')
    plt.xlabel('Magnet Serial Number')
    plt.ylabel('Fall Time (seconds)')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    




def plotOD(all_rings):
    # Group rings by outer diameter
    sorted_rings = sorted(all_rings, key=lambda x: x.outer_diameter)

    from collections import defaultdict
    diameter_groups = defaultdict(list)
    for ring in sorted_rings:
        diameter_groups[ring.outer_diameter].append(ring)
    
    box_width = 0.4  # Width of each individual box
    spacing = 0.00   # Space between boxes at same diameter
    
    orientation_colors = {'N-S': 'blue', 'S-N': 'red', 'Other': 'green'}  # Add more as needed
    
    x_positions = []
    x_labels = []
    fig, ax = plt.subplots(figsize=(5, 4))
    for diameter, rings in diameter_groups.items():
        n_rings = len(rings)
        total_width = n_rings * box_width + (n_rings - 1) * spacing
        start_pos = diameter - total_width/2
        
        for i, ring in enumerate(rings):
            # Calculate position for this box
            pos = start_pos + i * (box_width + spacing) + box_width/2
            x_positions.append(pos)
            
            # Get color based on orientation
            color = orientation_colors.get(ring.orientation)
            
            # Create boxplot for this single ring
            box = ax.boxplot(ring.fall_times, 
                           positions=[pos],
                           widths=box_width,
                           patch_artist=True,
                           showmeans=True,
                           meanline=True,
                           meanprops={'color': 'black', 'linewidth': 1, 'linestyle': '-'},
                           medianprops={'linewidth': 0}
                           )
            for patch in box['boxes']: #box color setter
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
    
    # Make Plot prettier
    x_labels.append((diameter, f"{diameter} mm\n({n_rings} rings)"))
    unique_diameters = sorted(diameter_groups.keys())
    ax.set_xticks(unique_diameters)
    ax.set_xticklabels([f"{d} mm\n({len(diameter_groups[d])//2} rings)" for d in unique_diameters])
    ax.set_xlabel('Outer Diameter (mm)')
    ax.set_ylabel('Fall Time (s)')
    ax.set_title('Fall Time Distribution by Outer Diameter and Orientation')
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
    




def plotHD(all_rings):
    # Group rings by outer diameter
    sorted_rings = sorted(all_rings, key=lambda x: x.hole_diameter)

    from collections import defaultdict
    diameter_groups = defaultdict(list)
    for ring in sorted_rings:
        diameter_groups[ring.hole_diameter].append(ring)
    
    box_width = 0.4  # Width of each individual box
    spacing = 0.00   # Space between boxes at same diameter
    
    orientation_colors = {'N-S': 'blue', 'S-N': 'red', 'Other': 'green'}  # Add more as needed
    
    x_positions = []
    x_labels = []
    fig, ax = plt.subplots(figsize=(5, 4))
    for diameter, rings in diameter_groups.items():
        n_rings = len(rings)
        total_width = n_rings * box_width + (n_rings - 1) * spacing
        start_pos = diameter - total_width/2
        
        for i, ring in enumerate(rings):
            # Calculate position for this box
            pos = start_pos + i * (box_width + spacing) + box_width/2
            x_positions.append(pos)
            
            # Get color based on orientation
            color = orientation_colors.get(ring.orientation)
            
            # Create boxplot for this single ring
            box = ax.boxplot(ring.fall_times, 
                           positions=[pos],
                           widths=box_width,
                           patch_artist=True,
                           showmeans=True,
                           meanline=True,
                           meanprops={'color': 'black', 'linewidth': 1, 'linestyle': '-'},
                           medianprops={'linewidth': 0}
                           )
            for patch in box['boxes']: #box color setter
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
    
    # Make Plot prettier
    x_labels.append((diameter, f"{diameter} mm\n({n_rings} rings)"))
    unique_diameters = sorted(diameter_groups.keys())
    ax.set_xticks(unique_diameters)
    ax.set_xticklabels([f"{d} mm\n({len(diameter_groups[d])//2} rings)" for d in unique_diameters])
    ax.set_xlabel('Hole Diameter (mm)')
    ax.set_ylabel('Fall Time (s)')
    ax.set_title('Fall Time Distribution by Hole Diameter and Orientation')
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
    



def plotThick(all_rings):
    # Group rings by outer diameter
    sorted_rings = sorted(all_rings, key=lambda x: x.thickness)

    from collections import defaultdict
    diameter_groups = defaultdict(list)
    for ring in sorted_rings:
        diameter_groups[ring.thickness].append(ring)
    
    box_width = 0.4  # Width of each individual box
    spacing = 0.00   # Space between boxes at same diameter
    
    orientation_colors = {'N-S': 'blue', 'S-N': 'red', 'Other': 'green'}  # Add more as needed
    
    x_positions = []
    x_labels = []
    fig, ax = plt.subplots(figsize=(5, 4))
    for diameter, rings in diameter_groups.items():
        n_rings = len(rings)
        total_width = n_rings * box_width + (n_rings - 1) * spacing
        start_pos = diameter - total_width/2
        
        for i, ring in enumerate(rings):
            # Calculate position for this box
            pos = start_pos + i * (box_width + spacing) + box_width/2
            x_positions.append(pos)
            
            # Get color based on orientation
            color = orientation_colors.get(ring.orientation)
            
            # Create boxplot for this single ring
            box = ax.boxplot(ring.fall_times, 
                           positions=[pos],
                           widths=box_width,
                           patch_artist=True,
                           showmeans=True,
                           meanline=True,
                           meanprops={'color': 'black', 'linewidth': 1, 'linestyle': '-'},
                           medianprops={'linewidth': 0}
                           )
            for patch in box['boxes']: #box color setter
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
    
    # Make Plot prettier
    x_labels.append((diameter, f"{diameter} mm\n({n_rings} rings)"))
    unique_diameters = sorted(diameter_groups.keys())
    ax.set_xticks(unique_diameters)
    ax.set_xticklabels([f"{d} mm\n({len(diameter_groups[d])//2} rings)" for d in unique_diameters])
    ax.set_xlabel('Thickness (mm)')
    ax.set_ylabel('Fall Time (s)')
    ax.set_title('Fall Time Distribution by Thickness')
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
    
    
    
    
def plotPull(all_rings):
    # Group rings by outer diameter
    sorted_rings = sorted(all_rings, key=lambda x: x.pull_rating)

    from collections import defaultdict
    diameter_groups = defaultdict(list)
    for ring in sorted_rings:
        diameter_groups[ring.pull_rating].append(ring)
    
    box_width = 0.1  # Width of each individual box
    spacing = 0.00   # Space between boxes at same diameter
    
    orientation_colors = {'N-S': 'blue', 'S-N': 'red', 'Other': 'green'}  # Add more as needed
    
    x_positions = []
    x_labels = []
    fig, ax = plt.subplots(figsize=(5, 4))
    for diameter, rings in diameter_groups.items():
        n_rings = len(rings)
        total_width = n_rings * box_width + (n_rings - 1) * spacing
        start_pos = diameter - total_width/2
        
        for i, ring in enumerate(rings):
            # Calculate position for this box
            pos = start_pos + i * (box_width + spacing) + box_width/2
            x_positions.append(pos)
            
            # Get color based on orientation
            color = orientation_colors.get(ring.orientation)
            
            # Create boxplot for this single ring
            box = ax.boxplot(ring.fall_times, 
                           positions=[pos],
                           widths=box_width,
                           patch_artist=True,
                           showmeans=True,
                           meanline=True,
                           meanprops={'color': 'black', 'linewidth': 1, 'linestyle': '-'},
                           medianprops={'linewidth': 0}
                           )
            for patch in box['boxes']: #box color setter
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
    
    # Make Plot prettier
    x_labels.append((diameter, f"{diameter} lbs\n({n_rings} rings)"))
    unique_diameters = sorted(diameter_groups.keys())
    ax.set_xticks(unique_diameters)
    ax.set_xticklabels([f"{d} lbs\n({len(diameter_groups[d])//2} rings)" for d in unique_diameters])
    ax.set_xlabel('Pull Rating (lbs)')
    ax.set_ylabel('Fall Time (s)')
    ax.set_title('Fall Time Distribution by Pull Rating')
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()    
# def plotODold(all_rings):

#     fig, ax = plt.subplots()
#     colors = plt.cm.viridis(np.linspace(0, 1, len(all_rings)))
    
#     # Plot each point with a different color and label
#     for ring_magnet in all_rings:
#         x=ring_magnet.outer_diameter
#         y=ring_magnet.mean_fall_time
#         yerr=ring_magnet.std_fall_time
#         if ring_magnet.orientation == 'N-S':
#             color = 'blue'
#         else:
#             color = 'red'
        
#         ax.boxplot(
#             x, y,
#              # Use current color
            
#             label= f'{ring_magnet.name} ({ring_magnet.orientation})'
#         )
#         ax.errorbar(
#             x, y,
#             yerr=yerr,
#             capsize=5,
#             color=color  # Match error bar color to point
#         )
#     plt.title("Fall Time evolution versus Outer Ring Diameter")
#     plt.xlabel('Outer Diameter (mm)')
#     plt.ylabel('Fall Time (s)')
#     plt.grid(True)
#     plt.legend()
#     plt.show()