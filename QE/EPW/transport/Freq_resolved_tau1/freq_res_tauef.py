import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Conversion factor from Rydberg to electronvolt
ry_to_ev = 13.605693

nk = pow(120,3)

freq_step = 35.0/2000 # meV

# Updated Gaussian broadening in eV
#sigma = 0.0258
sigma = 0.005

ryd2ps1 = 20670.6944033

# Input files with associated Ef (in eV) and output labels
files = [
    ("inv_tau_freq.fmt", 16.2317, "NbAs"),
#    ("inv_tau_freq25.fmt", 17.0883, "freq25"),
#    ("inv_tau_freq-25.fmt", 17.0383, "freq-25")
]

plt.figure()

for filename, ef, label in files:
    a = defaultdict(float)
    DOS = defaultdict(float)

    previous_energy = 1E20
    with open(filename, 'r') as f:
        for line in f:
            if line.strip().startswith('#') or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5:
                energy_ry = float(parts[2])
                energy_ev = energy_ry * ry_to_ev - ef
                freq = float(parts[3])
                tau_inv = float(parts[4]) * ryd2ps1 / freq_step # ps1/meV

                # Gaussian delta function
                gaussian = (1 / (np.sqrt(np.pi) * sigma)) * np.exp(-((energy_ev) / sigma) ** 2)
                a[freq] += 1./nk * tau_inv * gaussian # ps1/meV/eV
                current_energy = energy_ev
                energy_changed = abs(current_energy - previous_energy) > 1e-20
                # print (energy, energy_changed)
                #if energy_changed:
                DOS[freq] += 1./nk * gaussian # 1/eV
                #previous_energy = energy_ev

    a_divided = {}
    for freq in a:
        if DOS[freq] > 0:
            a_divided[freq] = a[freq] / DOS[freq]
        else:
            a_divided[freq] = 0.0  # or handle zero-DOS cases appropriately

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

#    # Sort and prepare output
    sorted_freqs2 = sorted(DOS.keys())
    summed_values2 = [DOS[f] for f in sorted_freqs]

    output_filename = f"DOS_{label}.dat"
    with open(output_filename, 'w') as out:
        out.write("# Frequency(meV)    Summed_delta(e-ef)\n")
        for freq, val in zip(sorted_freqs2, summed_values2):
            out.write(f"{freq:12.4f}    {val:14.6e}\n")


# Final plot adjustments
plt.xlabel('Frequency (meV)')
plt.ylabel('Summed ($\\tau^{-1} \\cdot \\delta(e - E_F)$)')
plt.title('Frequency-dependent Relaxation Analysis (σ = 0.01 eV)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

