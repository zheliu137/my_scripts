import numpy as np
import matplotlib.pyplot as plt

# Constants
inv_cell = 1.0 / 472.3420819
bohr2ang_ang2cm = 5.29177E-09
hbarJ = 1.05E-34
electron_si = 1.60E-19
nktot = 80**3

# Smearing parameter (in Ry)
eta = 5e-3  # ~small broadening width, adjust if needed

# Input file
filename = "Distribution_nk.fmt"

# Load data
velocities = []
contributions = []

with open(filename, 'r') as f:
    for line in f:
        if line.strip().startswith("#") or not line.strip():
            continue
        parts = line.split()
        try:
            dfde_x = float(parts[4])
            vnk_x = float(parts[7])
            sigma_point = -vnk_x * dfde_x / nktot
            velocities.append(abs(vnk_x))
            contributions.append(sigma_point)
        except (IndexError, ValueError):
            continue

velocities = np.array(velocities)
contributions = np.array(contributions)

# Compute total sigma_x
sigma_x = np.sum(contributions)
sigma_SI = sigma_x * (electron_si**2 * inv_cell) / (hbarJ * bohr2ang_ang2cm)

# Output total
print(f"Total sigma_x (Ry·Bohr units): {sigma_x:.6e}")
print(f"Total sigma_x (SI units):     {sigma_SI:.6e} S/cm")

# Smearing: define v grid and evaluate smeared distribution
v_max = velocities.max()
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
cumulative_sum_SI = np.cumsum(sigma_smeared_SI) * (v_grid[1] - v_grid[0])  # integrate over velocity

# Plot
fig, ax1 = plt.subplots(figsize=(8, 5))

color1 = 'tab:blue'
ax1.set_xlabel(r'$|v_{nk}^x|$ (Ry)')
ax1.set_ylabel(r'Smeared $\sigma_{point}$ (S/cm)', color=color1)
ax1.plot(v_grid, sigma_smeared_SI, '-', color=color1, label="Smeared σ")
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel(r'Cumulative $\sigma$ (S/cm)', color=color2)
ax2.plot(v_grid, cumulative_sum_SI, '-', color=color2, label="Cumulative σ")
ax2.tick_params(axis='y', labelcolor=color2)

fig.tight_layout()
plt.title(r'Smeared $\sigma_x$ vs $|v_{nk}^x|$')
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()

