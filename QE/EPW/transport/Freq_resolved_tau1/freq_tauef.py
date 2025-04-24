import numpy as np
import matplotlib.pyplot as plt

# Gaussian smearing width in meV
sigma_freq = 0.01

freq_step = 35.0/2000 # meV

nk = pow(100,3)

ry2ps1 = 20670.6944033

# Input/output files and labels
files = [
    ("dtauef_dw_freq0.dat", "0meV"),
    ("dtauef_dw_freq25.dat", "25meV"),
    ("dtauef_dw_freq-25.dat", "-25meV")
]


# Set up plot
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # right y-axis

for filename, label in files:
    # Load data, skip header
    data = np.loadtxt(filename, comments="#")
    x = data[:, 0]  # Frequency in meV
    y1 = data[:, 1]/DOS[label] # d(tau^-1)/dw (e.g. in ps^-1/meV)

    # Cumulative integral y2 using trapezoidal rule
    y2 = np.cumsum(np.concatenate([[0], 0.5 * (y1[1:] + y1[:-1]) * np.diff(x)]))

    # Plot original function and integral
    ax1.plot(x, y1, label=f"{label} (dtau/dw)", linestyle='-')
    ax2.plot(x, y2, label=f"{label} (integral)", linestyle='--')

    # Save output
    output_file = f"integrated_{filename}"
    with open(output_file, 'w') as f:
        f.write("# Frequency(meV)    y1                 Integral_y2\n")
        for xi, yi, yint in zip(x, y1, y2):
            f.write(f"{xi:12.4f}    {yi:14.6e}    {yint:14.6e}\n")

# Axis labels
ax1.set_xlabel('$\\omega$ (meV)')
ax1.set_ylabel('$\\partial \\tau^{-1} / \\partial \\omega$ (ps$^{-1}$/meV)', color='C0')
ax2.set_ylabel('$\\tau^{-1}(E_F)$ (ps$^{-1}$)', color='C1')

# Combine legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# Layout
ax1.set_xlim([0, 35])
ax1.grid(True)
fig.tight_layout()
plt.show()

