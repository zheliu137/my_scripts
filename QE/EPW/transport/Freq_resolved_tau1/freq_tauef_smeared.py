import numpy as np
import matplotlib.pyplot as plt

# Gaussian smearing width in meV
sigma_freq = 0.1
#sigma_freq = 0.001

freq_step = 35.0/2000 # meV

nk = pow(120,3)

ry2ps1 = 20670.6944033

# Input/output files and labels
files = [
    ("dtauef_dw_NbAs.dat", "NbAs", "red")
#    ("dtauef_dw_freq0.dat", "0meV", "black"),
#    ("dtauef_dw_freq-25.dat", "-25meV", "blue")
]

# Set up main figure and axes
plt.rcParams.update({
    'font.size': 18,
    'legend.fontsize': 14  
})

fig, ax1 = plt.subplots()


# Second y-axis (right side)
ax2 = ax1.twinx()

#x_grid = np.linspace(0, 10, 1000)
#dx = 10.0/(1000-1)
#kernel = (1 / (np.sqrt(2 * np.pi) * sigma_freq)) * np.exp(-((x_grid - 5.0)**2) / (2 * sigma_freq**2))
#area = np.sum(kernel) * dx

ax1.set_ylim([0, 1.0])
ax2.set_ylim([0, 5.0])
for input_file, label, lc in files:
    # Load frequency (meV) and value
    data = np.loadtxt(input_file, comments="#")
    freqs = data[:, 0]   # meV
    values = data[:, 1]  # ps1/meV   scattering rates/phonon freq

    # Uniform x-grid: 1000 points from 0 to max(freq)
    fmax = np.max(freqs)
    x_grid = np.linspace(0, fmax, 1000)
    dx = x_grid[1] - x_grid[0]

    # Smearing
    smeared_vals = []
    dos_vals = []
    for x in x_grid:
        kernel = (1 / (np.sqrt( np.pi) * sigma_freq)) * np.exp(-((x - freqs)**2) / ( sigma_freq**2))
        smeared_vals.append(np.sum(kernel * values ) * freq_step)
    smeared_vals = np.array(smeared_vals) # ps1/meV

    # Integral of y
    y2 = np.cumsum(smeared_vals) * dx

    # Plot original smeared values on left y-axis
    #ax1.plot(x_grid, smeared_vals, linestyle='-', label=f"{label} (\partial tau^-1/\partial \omega)")
    ax1.plot(x_grid, smeared_vals, linestyle='-', label=f"{label}", color=lc)

    # Plot integral on right y-axis
    #ax2.plot(x_grid, y2, linestyle='--', label=f"{label} (tau^-1)")
    ax2.plot(x_grid, y2, linestyle='--', color=lc)

    # Save to output file
    output_file = f"dtauef_dw_int_{label}.dat"
    with open(output_file, 'w') as out:
        #out.write("# omega(meV)  \\partial \\tau^{-1}_{\\epsilon_F}( / \\partial \\omega(THz/meV)  Integral(THz)\n")
        out.write("# omega(meV)  dt1_{ef}/dw(THz/meV)  Integral(THz)\n")
        for x, y, yint in zip(x_grid, smeared_vals, y2):
            out.write(f"{x:12.4f}    {y:14.6e}    {yint:14.6e}\n")

# Axis labels and titles
ax1.set_xlabel('$\\omega$ (meV)')
ax1.set_ylabel('$\\partial \\tau^{-1}_{\\epsilon_{\\rm F}} / \\partial \\omega$ (THz/meV)', color='black')
ax2.set_ylabel('Integral (THz)', color='black')

# Legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
#ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=14)
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# Layout and grid
#ax1.grid(True)

ax1.set_xlim([0, 35])

fig.tight_layout()

plt.savefig("output.pdf", format='pdf', bbox_inches='tight')

plt.show()

