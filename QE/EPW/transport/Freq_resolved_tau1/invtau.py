import matplotlib.pyplot as plt
from collections import defaultdict

# List of input files with optional labels
files = [
    ("inv_tau_freq0.fmt", "freq 0"),
    ("inv_tau_freq25.fmt", "freq +25"),
    ("inv_tau_freq-25.fmt", "freq -25")
]

plt.figure()

for filename, label in files:
    a = defaultdict(float)
    with open(filename, 'r') as file:
        for line in file:
            if line.strip().startswith('#') or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 5:
                energy = float(parts[2])   # Now group by the 3rd column (energy)
                relaxation_time = float(parts[4])
                a[energy] += relaxation_time
    
    sorted_energy = sorted(a.keys())
    summed_relax_times = [a[e] for e in sorted_energy]
    
    plt.plot(sorted_energy, summed_relax_times, marker='o', linestyle='None', label=label)

# Final plot formatting
plt.xlabel('Energy (Ry)')
plt.ylabel('Summed Relaxation Time (Ry)')
plt.title('Relaxation Time vs Energy for Multiple Files')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

