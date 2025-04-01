# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 15:10:15 2025

@author: vaucoi
"""

import serial

import csv
from datetime import datetime
import os
import time






# Set up serial communication

port = "COM5"  # Change to match your Arduino port (e.g., "/dev/ttyUSB0" for Linux/macOS)
baudrate = 115200  # Matches your Arduino baud rate
ser = serial.Serial(port, baudrate, timeout=60)
ser.reset_input_buffer()
ser.reset_output_buffer()
time.sleep(1)
date_format = datetime.now().strftime("%Y-%m-%d-%Hh%Mm%Ss")

# Wait for Arduino to be ready
print("Waiting for Arduino to initialize...")
#ser.readline()  # Read initial data from Arduino


# Prompt user for servo angle
servo_angle = input("Enter the servo angle (0-180): ")


# Send the angle to Arduino

ser.write(f"{servo_angle}\n".encode('utf-8'))  # Send the angle to Arduino
print(f"Sent servo angle: {servo_angle}")



# Wait for Arduino to confirm angle set (optional)
# You can check if the Arduino prints a confirmation message after setting the servo



# File path for saving data
csv_filename = os.path.join(os.getcwd(), "NeoD_2.0_35.00mm_20.59mm_5.00mm_(5901K75)_N-S_400mm_{0}.csv".format(date_format)) # Material_MaxPull_OD_HD_Thck_(57...)_Orientation (N-S)_RodLength_TIMEDATE.csv


# Open the CSV file for writing

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "Intensity"])  # CSV header


    print(f"Saving data to: {csv_filename}")
    print("Starting data collection... Press Ctrl+C to stop.")



    try:

        while True:

            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                #print(f"Received: {data}")  # Debugging print
                values = data.split(',')

                if len(values) == 2:  # Expecting 2 values (intensity, time)
                    try:
                        intensity = float(values[0])  # Light intensity
                        timestamp = float(values[1])  # Time (s)


                        writer.writerow([timestamp, intensity])  # Save data

                        file.flush()  # Force write to disk

                        # print(f"Saved: {timestamp}, {intensity}")  # Debugging print
                    except ValueError:

                        print(f"Skipping invalid data: {data}")

                else:

                    print(f"Skipping malformed line: {data}")



    except KeyboardInterrupt:

        print("\nData collection stopped.")
        #ser.write("180".encode('utf-8'))  # Send the angle to Arduino
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.close()

