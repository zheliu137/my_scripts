import numpy as np
import matplotlib.pyplot as plt

files = [
    ("dtauef_dw_int_25meV.dat", "25meV", "red"),
    ("dtauef_dw_int_0meV.dat", "0meV", "black"),
    ("dtauef_dw_int_-25meV.dat", "-25meV", "blue")
]

plt.rcParams.update({'font.size': 18})
fig, ax1 = plt.subplots()

# Second y-axis (right side)
ax2 = ax1.twinx()

ax1.set_ylim([0, 1.0])
ax2.set_ylim([0, 5.0])

for input_file, label, lc in files:
    # Load frequency (meV) and value
    data     = np.loadtxt(input_file, comments="#")
    x        = data[:, 0]   # meV
    vals   = data[:, 1]  # ps1/meV   scattering rates/phonon freq
    integral = data[:, 2]  # ps1/meV   scattering rates/phonon freq

    # Uniform x-grid: 1000 points from 0 to max(freq)
    xmax   = np.max(x)

    ax1.plot(x, vals, linestyle='-', label=f"{label}", color=lc)

    ax2.plot(x, integral, linestyle='--', color=lc)


# Axis labels and titles
ax1.set_xlabel('$\\omega$ (meV)')
ax1.set_ylabel('$\\partial \\tau^{-1}_{\\epsilon_{\\rm F}} / \\partial \\omega$ (THz/meV)', color='black')
ax2.set_ylabel('Integral (THz)', color='black')

# Legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=14)

# Layout and grid
#ax1.grid(True)

ax1.set_xlim([0, 35])

fig.tight_layout()
plt.show()

