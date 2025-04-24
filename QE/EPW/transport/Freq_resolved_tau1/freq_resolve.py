import matplotlib.pyplot as plt
from collections import defaultdict

# List of input files with optional labels
files = [
    ("inv_tau_freq0.fmt", "freq 0"),
    ("inv_tau_freq25.fmt", "freq +25"),
    ("inv_tau_freq-25.fmt", "freq -25")
]

# Plot setup
plt.figure()

for filename, label in files:
    a = defaultdict(float)
    with open(filename, 'r') as file:
        for line in file:
            if line.strip().startswith('#') or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5:
                freq = float(parts[3])
                relaxation_time = float(parts[4])
                a[freq] += relaxation_time

    sorted_freqs = sorted(a.keys())
    summed_relax_times = [a[freq] for freq in sorted_freqs]

    plt.plot(sorted_freqs, summed_relax_times, marker='o', linestyle='-', label=label)

# Final plot formatting
plt.xlabel('Frequency (meV)')
plt.ylabel('Summed Relaxation Time (Ry)')
plt.title('Relaxation Time vs Frequency for Multiple Files')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

