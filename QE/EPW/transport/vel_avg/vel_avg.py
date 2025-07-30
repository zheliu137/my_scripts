#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
import os

# Constants
ry_to_ev = 13.605693009

def compute_velocity_averages(input_file, sigma=0.026, num_points=2001, e_range=0.2):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Extract Fermi energy (Ef0)
    for line in lines:
        if line.strip().startswith("# itemp"):
            ef_line = lines[lines.index(line)+1]
            ef_ry = float(ef_line.split()[1])  # in Ry
            break
    else:
        raise ValueError("Fermi energy not found in input file.")

    ef_ev = ef_ry * ry_to_ev

    # Extract data
    data = []
    in_band_section = False
    for line in lines:
        if line.strip().startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) == 7:
            in_band_section = True
            try:
                vx, vy, vz = map(float, parts[2:5])
                eig_ry = float(parts[5])
                weight = float(parts[6])
                data.append([vx, vy, vz, eig_ry, weight])
            except ValueError:
                continue
        elif in_band_section and len(parts) == 2:
            break

    data = np.array(data, dtype=float).reshape(-1, 5)
    eig_ev = data[:, 3] * ry_to_ev - ef_ev  # shift relative to Ef
    weights = data[:, 4]

    # Energy grid from -e_range to +e_range
    e0_vals = np.linspace(-e_range, e_range, num_points)
    v_avg_x = np.zeros_like(e0_vals)
    v_avg_y = np.zeros_like(e0_vals)
    v_avg_z = np.zeros_like(e0_vals)
    norm = np.zeros_like(e0_vals)

    for i, e0 in enumerate(e0_vals):
        delta = np.exp(-((eig_ev - e0)**2) / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))
        v_avg_x[i] = np.sum(np.abs(data[:, 0])**2 * delta * weights)
        v_avg_y[i] = np.sum(np.abs(data[:, 1])**2 * delta * weights)
        v_avg_z[i] = np.sum(np.abs(data[:, 2])**2 * delta * weights)
        norm[i] = np.sum(delta * weights)

    with np.errstate(divide='ignore', invalid='ignore'):
        v_avg_x = np.where(norm > 0, v_avg_x / norm, 0)
        v_avg_y = np.where(norm > 0, v_avg_y / norm, 0)
        v_avg_z = np.where(norm > 0, v_avg_z / norm, 0)

    output = np.column_stack((e0_vals, v_avg_x, v_avg_y, v_avg_z))
    np.savetxt("average_velocity_vs_energy.dat", output,
               header="Energy(eV)  |Vx|  |Vy|  |Vz|", fmt="%.6f")
    print("Saved: average_velocity_vs_energy.dat")
    return output

def plot_velocity_data(datafile):
    data = np.loadtxt(datafile, comments="#")
    e, vx, vy, vz = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    plt.plot(e, vx, label='|Vx|')
    plt.plot(e, vy, label='|Vy|')
    plt.plot(e, vz, label='|Vz|')
    plt.xlabel("Energy (eV)")
    plt.ylabel("Average Absolute Velocity (Ry)")
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Compute and/or plot average velocity vs energy.")
    parser.add_argument("input_file", nargs="?", default="IBTEvel_sup.fmt",
                        help="Input velocity file or existing average file (default: IBTEvel_sup.fmt)")
    parser.add_argument("--sigma", type=float, default=0.01,
                        help="Gaussian broadening in eV (default: 0.01)")
    parser.add_argument("--plot-only", action="store_true",
                        help="Only plot from existing average data file")

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)

    if args.plot_only or "average_velocity_vs_energy" in args.input_file:
        plot_velocity_data(args.input_file)
    else:
        result = compute_velocity_averages(args.input_file, sigma=args.sigma)
        plot_velocity_data("average_velocity_vs_energy.dat")

if __name__ == "__main__":
    main()

