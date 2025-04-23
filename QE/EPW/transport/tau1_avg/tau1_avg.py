# This code is for the calculation of the average of \tau-1 near the different energies.
import numpy as np
import matplotlib.pyplot as plt

# Define the sigma, e0 range, and Ef
sigma = 0.005
n=401
nk=140^3
ub = 0.20
lb = -0.20
leng = ub - lb
e0_values = np.linspace(lb, ub, n)
E_f = [17.0633-0.025,17.0633,17.0633+0.025]  # Fermi energy in eV
ry_to_ev = 13.6057  # Conversion factor from Rydberg to eV

# Function to load data and compute results
def compute_results(filename, E_f):
    # Load data from file
    data = np.loadtxt(filename, skiprows=1)
    # e = data[:, 0] * ry_to_ev - E_f  # Convert from Rydberg to eV and subtract Ef
    e = data[:, 0]  # in the unit of eV and relative to Ef
    #f = data[:, 6]
    f = data[:, 1]
    
    # Prepare to store the results
    results = np.zeros_like(e0_values)
    
    # Calculate the sum for each e0
    for index, e0 in enumerate(e0_values):
        delta_approx =  (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(e - e0)**2 / (2 * sigma**2))
        tau = np.sum(f * delta_approx)
        dos = np.sum( delta_approx)
        results[index] = tau/dos
    return results

# Set the print options to use scientific notation with 4 decimal places
#np.set_printoptions(formatter={'float': '{:0.4e}'.format})

# Print the array
#np.savetxt(array)


# Compute results for each file
results1 = compute_results('data1.txt', E_f[1])
results2 = compute_results('data2.txt', E_f[0])
results3 = compute_results('data3.txt', E_f[2])

total_avg = np.array([e0_values, results1, results2, results3])

np.savetxt('energy.dat', e0_values , fmt='%.4e')
np.savetxt('avg1.dat', results1 , fmt='%.4e')
np.savetxt('avg2.dat', results2 , fmt='%.4e')
np.savetxt('avg3.dat', results3 , fmt='%.4e')

#np.savetxt(file_path, array, fmt='%.4e', newline='\n')

np.savetxt('avg_tot.dat', total_avg.T, fmt='%.4e', newline='\n')

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(e0_values, results1, label='0meV')
#plt.plot(e0_values-0.025, results2, label='-25meV')
#plt.plot(e0_values+0.025, results3, label='25meV')
plt.plot(e0_values, results2, label='-25meV')
plt.plot(e0_values, results3, label='25meV')
plt.xlim(-0.1, 0.1)
#plt.ylim(1e-4, 1e-3)
#plt.yscale('log')  # Set the y-axis to logarithmic scale
plt.xlabel('E-E_f(eV)')
plt.ylabel('Tau_avg ')
#plt.title('Log-Scale Sum of f_i * delta_sigma(e_i - e0) for Three Energy Offsets')
plt.legend()
plt.grid(True, which="both", ls="--")  # Enhance grid visibility for log scale
plt.show()

