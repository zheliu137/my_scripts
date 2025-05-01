import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Conversion factor from Rydberg to electronvolt
ry_to_ev = 13.605693
ryd2ps1 = 20670.6944033

nk = pow(120, 3)
freq_step = 35.0 / 2000  # meV

# Gaussian broadening in eV
sigma = 0.005  # for Gaussian

# Temperature in Kelvin for Fermi-Dirac derivative
temperature = 300.0  # K
k_B = 8.617333262e-5  # Boltzmann constant in eV/K

# Choose whether to use Gaussian or Fermi derivative
use_fermi_derivative = True

# Input files with associated Ef (in eV) and output labels
files = [
    ("inv_tau_freq.fmt", 17.0633, "0meV"),
    ("inv_tau_freq25.fmt", 17.0883, "25meV"),
    ("inv_tau_freq-25.fmt", 17.0383, "-25meV")
]

plt.figure()

for filename, ef, label in files:
    a = defaultdict(float)
    DOS = defaultdict(float)

    with open(filename, 'r') as f:
        for line in f:
            if line.strip().startswith('#') or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5:
                energy_ry = float(parts[2])
                energy_ev = energy_ry * ry_to_ev - ef
                freq = float(parts[3])
                tau_inv = float(parts[4]) * ryd2ps1 / freq_step  # ps^-1/meV

                if use_fermi_derivative:
                    # Derivative of Fermi-Dirac distribution: -df/dE
                    beta = 1.0 / (k_B * temperature)  # 1/eV
                    fermi_deriv = (beta / 4.0) / (np.cosh(beta * energy_ev / 2.0) ** 2)
                    weight = fermi_deriv
                else:
                    # Gaussian delta function
                    weight = (1 / (np.sqrt(np.pi) * sigma)) * np.exp(-((energy_ev) / sigma) ** 2)

                a[freq] += 1.0 / nk * tau_inv * weight  # ps^-1/meV/eV
                DOS[freq] += 1.0 / nk * weight  # 1/eV

    # Normalize: a[freq] divided by DOS[freq]
    a_divided = {}
    for freq in a:
        if DOS[freq] > 0:
            a_divided[freq] = a[freq] / DOS[freq]
        else:
            a_divided[freq] = 0.0

    a = a_divided

    # Sort and prepare output
    sorted_freqs = sorted(a.keys())
    summed_values = [a[f] for f in sorted_freqs]

    # Plot
    plt.plot(sorted_freqs, summed_values, marker='o', linestyle='-', label=label)

    # Output to file
    output_filename = f"dtauef_dw_{label}.dat"
    with open(output_filename, 'w') as out:
        out.write("# # Omega(meV)     dTau_ef^-1dw(ps^-1/meV)\n")
        for freq, val in zip(sorted_freqs, summed_values):
            out.write(f"{freq:12.4f}    {val:14.6e}\n")

    # Also output DOS
    sorted_freqs2 = sorted(DOS.keys())
    summed_values2 = [DOS[f] for f in sorted_freqs2]

    output_filename = f"DOS_{label}.dat"
    with open(output_filename, 'w') as out:
        out.write("# Frequency(meV)    Summed_delta_or_dfdE(e-ef)\n")
        for freq, val in zip(sorted_freqs2, summed_values2):
            out.write(f"{freq:12.4f}    {val:14.6e}\n")

# Final plot adjustments
plt.xlabel('Frequency (meV)', fontsize=16)
plt.ylabel('Summed ($\\tau^{-1} \\cdot \\partial f/\\partial E$)', fontsize=16)
plt.title('Frequency-dependent Relaxation Analysis', fontsize=18)
plt.legend(fontsize=14)
plt.grid(True)
plt.tight_layout()

# Save as PDF
plt.savefig("plot_result.pdf", format='pdf', bbox_inches='tight')

# Display
plt.show()

