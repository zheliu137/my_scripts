import numpy as np
import matplotlib.pyplot as plt

# Constants
ry_to_ev = 13.605693009  # Ry to eV conversion
sigma = 0.005  # Gaussian broadening in eV
num_points = 1000
e_range = 0.2  # +/- range from Ef in eV

# Read the file
filename = "IBTEvel_sup.fmt"
with open(filename, 'r') as f:
    lines = f.readlines()

# Extract Fermi energy (Ef0)
for line in lines:
    if line.strip().startswith("# itemp"):
        ef_line = lines[lines.index(line)+1]
        ef = float(ef_line.split()[1])  # in Ry
        break

ef_ev = ef * ry_to_ev

# Extract data lines until the line with only 2 columns is found
data = []
for line in lines:
    if line.strip().startswith("#") or not line.strip():
        continue
    parts = line.split()
    if len(parts) == 2:
        # Stop reading when reaching the final useless line
        break
    if len(parts) == 7:
        ik = int(parts[0])
        ibnd = int(parts[1])
        vx, vy, vz = map(float, parts[2:5])
        eig_ry = float(parts[5])
        weight = float(parts[6])
        data.append([vx, vy, vz, eig_ry, weight])

data = np.array(data)
eig_ev = data[:, 3] * ry_to_ev  # convert to eV

# ε grid
e0_vals = np.linspace(ef_ev - e_range, ef_ev + e_range, num_points)

# Prepare arrays for velocity averages
v_avg_x = np.zeros_like(e0_vals)
v_avg_y = np.zeros_like(e0_vals)
v_avg_z = np.zeros_like(e0_vals)
norm = np.zeros_like(e0_vals)

# Gaussian smearing and summation
for i, e0 in enumerate(e0_vals):
    delta = np.exp(-((eig_ev - e0)**2) / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))
    weights = data[:, 4]
    v_avg_x[i] = np.sum(data[:, 0] * delta * weights)
    v_avg_y[i] = np.sum(data[:, 1] * delta * weights)
    v_avg_z[i] = np.sum(data[:, 2] * delta * weights)
    norm[i] = np.sum(delta * weights)

# Normalize
with np.errstate(divide='ignore', invalid='ignore'):
    v_avg_x = np.where(norm > 0, v_avg_x / norm, 0)
    v_avg_y = np.where(norm > 0, v_avg_y / norm, 0)
    v_avg_z = np.where(norm > 0, v_avg_z / norm, 0)

# Save result
output = np.column_stack((e0_vals, v_avg_x, v_avg_y, v_avg_z))
np.savetxt("average_velocity_vs_energy.dat", output,
           header="Energy(eV)  Vx  Vy  Vz", fmt="%.6f")

# Optional plot
plt.plot(e0_vals, v_avg_x, label='Vx')
plt.plot(e0_vals, v_avg_y, label='Vy')
plt.plot(e0_vals, v_avg_z, label='Vz')
plt.xlabel("Energy (eV)")
plt.ylabel("Average Velocity")
plt.legend()
plt.tight_layout()
plt.show()
