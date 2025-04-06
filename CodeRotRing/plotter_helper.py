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
matplotlib.rcParams.update(matplotlib.rcParamsDefault)

import scienceplots
plt.style.use(['science'])

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
    plt.style.use(['science'])
    plt.show()
    
    
    
def plot_fall_time_boxplot(magnet_fall_times):
    """
    Creates a box plot of fall times for different magnet serial numbers.
    
    Args:
        magnet_fall_times (dict): Dictionary where:
            - keys are magnet serial numbers (e.g., '5901K75')
            - values are lists of fall times for that magnet
    """
    labels = []
    data = []
    
    for serial, times in magnet_fall_times.items():
        if len(times) > 0:  # Only include magnets with data
            labels.append(serial)
            data.append([t for t in times if t is not None])  # Filter out None values
    
    if not data:
        print("No valid fall time data to plot")
        return
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Create box plot
    box = plt.boxplot(data, patch_artist=True, labels=labels)
    
    # Customize colors
    colors = plt.cm.viridis(np.linspace(0, 1, len(labels)))
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    
    # Add plot elements
    plt.title('Fall Time Distribution by Magnet Serial Number')
    plt.xlabel('Magnet Serial Number')
    plt.ylabel('Fall Time (seconds)')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Rotate x-axis labels if needed
    if len(labels) > 5:
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()
    


def plotOD(all_rings):
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Group rings by outer diameter
    sorted_rings = sorted(all_rings, key=lambda x: x.outer_diameter)

    from collections import defaultdict
    diameter_groups = defaultdict(list)
    for ring in sorted_rings:
        diameter_groups[ring.outer_diameter].append(ring)
    
    # Prepare plot parameters
    box_width = 0.4  # Width of each individual box
    spacing = 0.00   # Space between boxes at same diameter
    
    # For color consistency
    orientation_colors = {'N-S': 'blue', 'S-N': 'red', 'Other': 'green'}  # Add more as needed
    
    # Create custom legend elements
    #legend_elements = [Patch(facecolor=color, label=orient, alpha=0.6) 
                     # for orient, color in orientation_colors.items()]
    
    # Track x positions and labels
    x_positions = []
    x_labels = []
    
    # Plot each group
    for diameter, rings in diameter_groups.items():
        n_rings = len(rings)
        total_width = n_rings * box_width + (n_rings - 1) * spacing
        start_pos = diameter - total_width/2
        
        for i, ring in enumerate(rings):
            # Calculate position for this box
            pos = start_pos + i * (box_width + spacing) + box_width/2
            x_positions.append(pos)
            
            # Get color based on orientation
            color = orientation_colors.get(ring.orientation, 'gray')
            
            # Create boxplot for this single ring
            box = ax.boxplot(ring.fall_times, 
                           positions=[pos],
                           widths=box_width,
                           patch_artist=True,
                           showmeans=True,
                           meanline=True,
                           meanprops={'color': 'black', 'linewidth': 2, 'linestyle': '-'},
                           medianprops={'linewidth': 0}
                           )
            for patch in box['boxes']: #box color setter
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
        
        # Add diameter label at base
        x_labels.append((diameter, f"{diameter} mm\n({n_rings} rings)"))
    
    # Make Plot prettier
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