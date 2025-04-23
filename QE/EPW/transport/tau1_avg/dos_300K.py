import numpy as np
import matplotlib.pyplot as plt

# Define the sigma, e0 range, and Ef
func = "Gaussian"
#func = "FD"
sigma = 0.01
n=401
nk1=pow(140,3)
nk2=pow(120,3)
ub = 0.1
lb = -0.1
leng = ub - lb
e0_values = np.linspace(lb, ub, n)

T = 300.0  # Temperature in Kelvin

E_f = [17.0633-0.025,17.0633,17.0633+0.025]  # Fermi energy in eV

# Constants
k_B = 8.617e-5  # Boltzmann constant in eV/K
ry_to_ev = 13.6057  # Conversion factor from Rydberg to eV

# Fermi-Dirac distribution function
def fermi_dirac(E, T):
    return 1 / (np.exp(( E ) / (k_B * T)) + 1)

# Function to load data and compute results
def compute_results(filename, E_f, nk, func="Delta"):
    # Load data from file
    data = np.loadtxt(filename, skiprows=1)
    e = data[:, 0] * ry_to_ev - E_f  # Convert from Rydberg to eV and subtract Ef
    f = data[:, 6]
    
    # Prepare to store the results
    results = np.zeros_like(e0_values)
    
    # Calculate the sum for each e0
    for index, e0 in enumerate(e0_values):
        if (func == "FD") :
          f_fd = fermi_dirac( e - e0 , T)
          delta_approx = 1./nk * f_fd * (1. - f_fd)/(k_B*T)
        else:
          delta_approx = 1./nk * (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(e - e0)**2 / (2 * sigma**2))

        dos = np.sum( delta_approx)
        results[index] = dos
    return results

# Compute results for each file
results1 = compute_results('data1.txt', E_f[1], nk2, func)
# results2 = compute_results('data2.txt', E_f[0], nk1, func)
# results3 = compute_results('data3.txt', E_f[2], nk1, func)

n = 0
for i in results1, results2, results3:
    n = n + 1
    results = np.array([e0_values, i])
    np.savetxt( str(n) + '.dat', results.T , fmt='%.4e')

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(e0_values, results1, label='0meV', color = "black")
# plt.plot(e0_values, results2, label='-25meV', color = "blue")
# plt.plot(e0_values, results3, label='25meV', color = "red")
#plt.yscale('log')  # Set the y-axis to logarithmic scale
plt.xlabel('E-E_f (eV)')
plt.ylabel('∂f/∂ε')
plt.ylabel('DOS(States/eV)')
plt.legend()
plt.grid(True, which="both", ls="--")  # Enhance grid visibility for log scale
plt.show()

