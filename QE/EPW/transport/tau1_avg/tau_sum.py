# This code is for the sum of \tau-1 over states near the electronic energies.
import numpy as np
import matplotlib.pyplot as plt

# Define the sigma, e0 range, and Ef
sigma = 0.005
n=401
ub = 0.10
lb = -0.10
leng = ub - lb
e0_values = np.linspace(lb, ub, n)
E_f = [17.0633-0.025,17.0633,17.0633+0.025]  # Fermi energy in eV
ry_to_ev = 13.6057  # Conversion factor from Rydberg to eV
ry_to_ps1 = 20670.6944033 # Conversion factor from Rydberg to 1/ps

# Function to load data and compute results
def compute_results(filename, nk, E_f):
    # Load data from file
    data = np.loadtxt(filename, skiprows=1)
    e = data[:, 0] * ry_to_ev - E_f  # Convert from Rydberg to eV and subtract Ef
    # f = data[:, 6]

    inv_tau = data[:, 6] * ry_to_ps1
    f = np.where(inv_tau < 1E-50, 0.0, 1.0 / inv_tau)
    
    # Prepare to store the results
    results = np.zeros_like(e0_values)
    
    # Calculate the sum for each e0
    for index, e0 in enumerate(e0_values):
        delta_approx = 1/nk* (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(e - e0)**2 / (2 * sigma**2))
        tau = np.sum(f * delta_approx)
        dos = np.sum( delta_approx)
        results[index] = tau
    return results

# Compute results for each file
results1 = compute_results('data1.txt', pow(120,3), E_f[1])
results2 = compute_results('data2.txt', pow(140,3), E_f[0])
results3 = compute_results('data3.txt', pow(140,3), E_f[2])

total_sum = np.array([e0_values, results1, results2, results3])

#np.savetxt(file_path, array, fmt='%.4e', newline='\n')

np.savetxt('tau_sum.dat', total_sum.T, fmt='%.4e', newline='\n')

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(e0_values, results1, label='0meV', color = "black")
plt.plot(e0_values, results2, label='-25meV', color = "blue")
plt.plot(e0_values, results3, label='25meV', color = "red")
plt.xlim(-0.1, 0.1)
#plt.ylim(1e-4, 1e-3)
plt.yscale('log')  # Set the y-axis to logarithmic scale
plt.xlabel('E-E_f(eV)')
plt.ylabel('Tau_sum(ps/eV) ')
#plt.title('Log-Scale Sum of f_i * delta_sigma(e_i - e0) for Three Energy Offsets')
plt.legend()
plt.grid(True, which="both", ls="--")  # Enhance grid visibility for log scale
plt.show()

