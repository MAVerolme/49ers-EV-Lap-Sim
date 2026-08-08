#   UNC Charlotte 49ers Track Map Generator
#   Created by : Matt Verolme
#   Last updated : 8/7/2026

#   Description :
#
#   Reads a MoTeC CSV export that contains Latitude and Longitude data.
#    
#   Converts GPS coordinates to X and Y coordinates in feet, centered around starting point
#
#   Fits a spline to the layout of the track. This helps eliminate noise
#
#   Generates evenly spaced points covering entire track
#
#   Determines cumulative distance and turn radius at each point.
#
#   Creates and saves CSV file that can be input into LapSim.py


#---------- Import Statements ----------

import csv
import math
import os
import tkinter as tk
from tkinter import ttk, filedialog

import numpy as np
from scipy.interpolate import make_splprep
from scipy.integrate import cumulative_trapezoid

import matplotlib.pyplot as plt

# ---------- Variables ----------

r_earth = 20902896.96  # radius of earth at UNCC, ft
smoothing = 500 # Spline smoothing strength; increase if output is longer than expected or looks rough
spacing = 0.5 # Spacing between points in output, ft

# ---------- Coordinate conversion ----------

def gps_to_xy(lat, long, lat0, long0):

    # Converts lat and long to x and y coordinates in feet, centered around first gps point

    x = r_earth * np.radians(np.asarray(long) - long0) * math.cos(math.radians(lat0)) # East-West distance from reference, ft
    y = r_earth * np.radians(np.asarray(lat) - lat0) # North-South distance from reference, ft
    return x, y

# ---------- Read GPS values from MoTeC export ----------

def read_gps_data(text, lat_column, long_column):

    # Parses MoTeC csv export

    lats = [] # List containing all latitude values
    longs = [] # List containing all longitude values

    reader = csv.reader(text.splitlines())

    for rows in reader:
        try:
            lat = float(rows[lat_column])
            long = float(rows[long_column])
            lats.append(lat)
            longs.append(long)
        except(ValueError, TypeError, IndexError):    # Skips over invalid rows (headers, blank rows, etc.)
            continue
    return lats, longs

# ---------- Build track model ----------

def build_track(lats, longs, smoothing, spacing):


    lat0 = lats[0]    # Sets reference latitude as first latitude value
    long0 = longs[0]  # Sets reference longitude as first longitude value

    x, y = gps_to_xy(lats, longs, lat0, long0)

    # Last data point is set equal to close loop. This jump should be smoothed out in the created spline
    x[-1] = x[0]
    y[-1] = y[0]

    # Create spline through points; bc_type='periodic' forces spline to be a closed loop
    spl, u = make_splprep([x, y], s=smoothing, bc_type='periodic')

    # Create array of evenly spaced values from 0-1 (domain of u)
    u_fine = np.linspace(0, 1, 10000)

    # Create array containing rate of change of position (ft) per unit of u along spline
    d1_fine = spl(u_fine, nu=1)

    dx = d1_fine[0] # Contains dx/du values across all u_fine points
    dy = d1_fine[1] # Contains dy/du values across all u_fine points

    # Compute magnitude of each rate of change vector (ds/du) across all u_fine points
    ds = np.sqrt(dx ** 2 + dy ** 2)

    # Integrate ds/du over u to get actual distance in ft
    s_fine = cumulative_trapezoid(ds, u_fine, initial=0)

    total_length = s_fine[-1]

    # Create uniformly spaced distance points based on 'spacing' value
    s_uniform = np.arange(0, total_length, spacing)

    # Find corresponding u values for each point in s_uniform
    u_uniform = np.interp(s_uniform, s_fine, u_fine)

    d1 = spl(u_uniform, nu=1) # Evaluates first derivative of spline at each uniformly spaced point
    d2 = spl(u_uniform, nu=2) # Evaluates second derivative of spline at each uniformly spaced point

    dx = d1[0]
    dy = d1[1]

    d2x = d2[0]
    d2y = d2[1]

    # Calculate curvature and radius at each point along track
    curvature = (dx * d2y - dy * d2x) / ((dx ** 2 + dy ** 2) ** (3/2))
    radius = 1.0 / curvature


    track_points = list(zip(range(len(s_uniform)), s_uniform, radius))
    return track_points, total_length, spl, u_fine

# ---------- Generates plot of track ----------

def plot_track(spl, u_fine, title):

    xy = spl(u_fine)
    x_plot = xy[0]
    y_plot = xy[1]

    plt.figure(figsize=(8, 8))
    plt.plot(x_plot, y_plot, '-', linewidth=1.5)
    plt.xlabel('X (ft)')
    plt.ylabel('Y (ft)')
    plt.title(title)
    plt.grid(True)
    plt.show()


# ---------- File Selection Interface ----------
class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("GPS Track Creator")

        self.file_track = tk.StringVar()
        self.file_out = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self.master, text="Track File", command=self.track_file).grid(column=100, row=10)
        ttk.Label(self.master, textvariable=self.file_track, font=('Calibri 12')).grid(column=100, row=20)

        ttk.Button(self.master, text="Output Folder", command=self.output_folder).grid(column=100, row=30)
        ttk.Label(self.master, textvariable=self.file_out, font=('Calibri 12')).grid(column=100, row=40)

        ttk.Label(self.master, text="Latitude column (first column is column 0)", font=('Calibri 12')).grid(column=100, row=50)
        self.lat_column = tk.Entry(self.master, width=15)
        self.lat_column.grid(column=100, row=60)

        ttk.Label(self.master, text="Longitude column (first column is column 0)", font=('Calibri 12')).grid(column=100, row=70)
        self.long_column = tk.Entry(self.master, width=15)
        self.long_column.grid(column=100, row=80)

        ttk.Label(self.master, text="Output File Name", font=('Calibri 12')).grid(column=100, row=110)
        self.out_name_entry = tk.Entry(self.master, width=15)
        self.out_name_entry.grid(column=100, row=120)

        ttk.Button(self.master, text="Set Choices", command=self.set_choices).grid(column=100, row=130)

    def track_file(self):
        self.file_track.set(filedialog.askopenfilename())

    def output_folder(self):
        self.file_out.set(filedialog.askdirectory())

    # Get column index for latitude and longitude data
    def set_choices(self):
        self.lat_col = int(self.lat_column.get())
        self.long_col = int(self.long_column.get())
        self.out_name = self.out_name_entry.get()

        self.track_path = self.file_track.get()
        self.out_path = self.file_out.get()

        self.master.destroy()


if __name__ == "__main__":
    interface = tk.Tk()
    app = Interface(interface)
    interface.mainloop()

    # File info from user inputs
    data_path = app.track_path
    output = app.out_path
    out_name = app.out_name
    track_path = os.path.join(output, out_name + '.csv')

    with open(data_path, 'r') as f:
        text = f.read()

    lats, longs = read_gps_data(text, app.lat_col, app.long_col)

    track_points, total_length, spl, u_fine = build_track(lats, longs, smoothing, spacing)

    print(f"Generated lap length: {total_length:.1f} ft")
    print(f"Track file contains {len(track_points)} points at {spacing} ft spacing.")

    with open(track_path, "w", newline='') as out_f:
        writer = csv.writer(out_f, dialect='excel')
        for row in track_points:
            writer.writerow(row)

    print('Track file created and saved to ' + track_path + '\n')

    plot_track(spl, u_fine, title=out_name)
