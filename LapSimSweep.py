import csv
import tkinter as tk
from tkinter import filedialog

import numpy as np

from LapSim import (Car,
    FilePicker,
    read_track,
    weight as w0, # Base car weight, lbs (from LapSim.py)
    track_width,
    frontal_area,
    torque,
    gear_ratio,
    wheel_radius,
    skidpad_radius,
    skidpad_angle,)

weight_per_cl = 30.0666174   # Weight added per unit of C_l, lbs

cl_0 = 0.0 # Starting lift coefficient
cl_f = -3.0 # Final lift coefficient
cl_step = -0.01 # Lift coefficient step size


def param_sweep(track):


    # Creating array of cl values
    cl_vals = np.arange(cl_0, cl_f + cl_step, cl_step)

    results = []

    for cl in cl_vals:
        cd = -1 * cl # 1:-1 Cd to Cl ratio
        w = w0 + weight_per_cl * (-1 * cl) # Weight increases with cl

        car = Car(w, cl, cd, frontal_area, track_width, wheel_radius, torque, gear_ratio)

        endurance_lap, _ = car.lap_time(track) # Returns lap time. Uses '_' to discard total endurance time
        skidpad = car.cornering_time(skidpad_radius, skidpad_angle)

        results.append([cl, cd, w, endurance_lap, skidpad])
        print(f"CL = {cl:.2f} | CD = {cd:.2f} | Weight = {w:.3f} lbs | Lap Time = {endurance_lap:.3f} s | Skidpad Time = {skidpad:.3f} s")

    return results


def write_csv(results, output_path):
    with open(output_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["CL", "CD", "Weight", "Lap Time (s)", "Skidpad Time (s)"])
        writer.writerows(results)
    print("Sweep complete.")


if __name__ == "__main__":
    picker_root = tk.Tk()
    picker = FilePicker(picker_root)
    picker_root.mainloop()

    test_track = read_track(open(picker.track_path).read())

    save_root = tk.Tk()
    output_path = filedialog.asksaveasfilename(
        title="Save  results as",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile="sweep_results.csv",
    )
    save_root.destroy()

    sweep_results = param_sweep(test_track)
    write_csv(sweep_results, output_path)