import numpy as np
import matplotlib.pyplot as plt
import sys

# Constants
inv_cell_all = { 'TaAs' : 1.0 / 472.3420819, 'NbAs' : 1.0 / 478.626017138069, 'TaP' : 1.0 / 426.130539876746, 'NbP' :  1.0/432.406303470959} 

if len(sys.argv) > 1:
    system = sys.argv[1]
else:
    system = 'TaAs'


inv_cell = inv_cell_all[system]
bohr2ang_ang2cm = 5.29177E-09
hbarJ = 1.05E-34
electron_si = 1.60E-19
#nktot = 100**3
nktot = 120**3

# Smearing parameter (in Ry)
eta = 5e-3  # ~small broadening width, adjust if needed
xrange_max = 0.75

# Smearing parameter for energy delta
eta_e = eta  # Ry

# files
filename = "Distribution_nk.fmt"
output_file = "sigma_v_distribution.dat"

# Load data
energies = []
velocities = []
contributions = []

with open(filename, 'r') as f:
    for line in f:
        if line.strip().startswith("#") or not line.strip():
            continue
        parts = line.split()
        try:
            energy = float(parts[3])  # in Ry
            dfde_x = float(parts[4])
            vnk_x = float(parts[7])
            sigma_point = -vnk_x * dfde_x / nktot
            abs_vx = abs(vnk_x)
            if abs_vx > 0:
                energies.append(energy)
                velocities.append(abs_vx)
                contributions.append(sigma_point)
        except (IndexError, ValueError):
            continue

energies = np.array(energies)
velocities = np.array(velocities)
contributions = np.array(contributions)

# Compute total sigma_x
sigma_x = np.sum(contributions)
sigma_SI = sigma_x * (electron_si**2 * inv_cell) / (hbarJ * bohr2ang_ang2cm)

# Output total
print(f"Total sigma_xx :     {sigma_SI:.6e} S/cm")

# Smearing: define v grid and evaluate smeared distribution
#v_max = velocities.max()
v_max = xrange_max
v_grid = np.linspace(0, v_max, 500)
sigma_smeared = np.zeros_like(v_grid)

# Gaussian kernel sum
for i, v in enumerate(v_grid):
    weight = np.exp(-0.5 * ((v - velocities) / eta) ** 2)
    kernel = weight / (np.sqrt(2 * np.pi) * eta)
    sigma_smeared[i] = np.sum(contributions * kernel)

# Convert to SI
sigma_smeared_SI = sigma_smeared * (electron_si**2 * inv_cell) / (hbarJ * bohr2ang_ang2cm)

# Cumulative sum for second curve
cumulative_sigma_SI = np.cumsum(sigma_smeared_SI) * (v_grid[1] - v_grid[0])  # integrate over velocity

# --- Compute vDOS (no weighting) ---

# Compute dos at Fermi level
energy_weight = np.exp(-0.5 * (energies / eta_e) ** 2)
energy_kernel = energy_weight / (np.sqrt(2 * np.pi) * eta_e)
N_E = np.sum(energy_kernel) / nktot
print(f"Dos at Ef : {N_E}")

# Double delta vDOS at E=0
vDOS_Ef = np.zeros_like(v_grid)

for i, v in enumerate(v_grid):
    vel_weight = np.exp(-0.5 * ((v - velocities) / eta)**2)
    vel_kernel = vel_weight / (np.sqrt(2 * np.pi) * eta)
    combined = vel_kernel * energy_kernel / nktot
    vDOS_Ef[i] = np.sum(combined)


# Normalize vDOS(E=0)
# vDOS_Ef /= N_E

# Write to file
with open(output_file, 'w') as f_out:
    f_out.write("# v(Ry)   contribution(S/cm/Ry)   cumulative(S/cm)   density(states/cell/Ry)\n")
    for v, contrib, cum, dens in zip(v_grid, sigma_smeared_SI, cumulative_sigma_SI, vDOS_Ef):
        f_out.write(f"{v:.6e}  {contrib:.6e}  {cum:.6e}  {dens:.6e}\n")

print(f"Data written to: {output_file}")

# # Plot
# fig, ax1 = plt.subplots(figsize=(8, 5))

# color1 = 'tab:blue'
# plt.xlim(0, v_max)
# ax1.set_xlabel(r'$|v_x|$ (Ry)')
# ax1.set_ylabel(r'Contribution to $\sigma$ (S/cm)', color=color1)
# ax1.plot(v_grid, sigma_smeared_SI, '-', color=color1, label="Contribution to σ")
# ax1.tick_params(axis='y', labelcolor=color1)

# ax2 = ax1.twinx()
# color2 = 'tab:red'
# ax2.set_ylabel(r'Cumulative $\sigma$ (S/cm)', color=color2)
# ax2.plot(v_grid, cumulative_sigma_SI, '-', color=color2, label="Cumulative σ")
# ax2.tick_params(axis='y', labelcolor=color2)

# fig.tight_layout()
# plt.title(r'Smeared $\sigma_x$ vs $|v_{nk}^x|$')
# plt.grid(True, linestyle='--', alpha=0.3)
# plt.show()

# # 2. vDOS figure
# plt.figure(figsize=(8, 4.5))
# plt.plot(v_grid, vDOS_Ef, color='tab:green')
# plt.xlabel(r'$|v_{nk}^x|$ (Ry)')
# plt.ylabel(r'Density of states (arb. units)')
# plt.title(r'vDOS: Density of states vs $|v_{nk}^x|$')
# plt.grid(True, linestyle='--', alpha=0.3)
# plt.tight_layout()
# plt.show()

