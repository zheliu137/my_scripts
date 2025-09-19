import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.image as mpimg
from matplotlib.ticker import FixedLocator, MultipleLocator, AutoMinorLocator
from matplotlib import rcParams
import argparse

# --------------------
# Style
# --------------------
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica', 'Bitstream Vera Sans', 'sans-serif'],
    'font.size': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'axes.linewidth': 1.0,
    'xtick.major.width': 1.0,
    'ytick.major.width': 1.0,
    'legend.fontsize': 10,
    'legend.columnspacing': 0.5,
    'legend.handletextpad': 0.25,
    'legend.borderaxespad': 0.25,
})

def load_data(filename):
    data = np.loadtxt(filename, comments="#")
    energy = data[:, 0]
    # Offsets for each material: [start_col, start_col+1, start_col+2]
    offsets = {
        "TaAs": 1,
        "TaP":  4,
        "NbAs": 7,
        "NbP": 10,
    }
    return energy, data, offsets

def plot_velocity(energy, data, offsets, component):
    # Component index: vx = 0, vz = 2
    comp_idx = {"x": 0, "y": 1, "z": 2}[component.lower()]

    plt.figure(figsize=(6, 4))
    plt.xlim([-0.1,0.1])
    ax = plt.gca()
    plt.xticks(np.arange(-0.2, 0.21, 0.1))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    plt.axvline(x=-0.025, color='blue', linestyle='dashed', linewidth=1.5, alpha = 0.5, zorder=0)
    plt.axvline(x=0, color='black', linestyle='dashed', linewidth=1.5, alpha = 0.5, zorder=0)
    plt.axvline(x=0.025, color='red', linestyle='dashed', linewidth=1.5, alpha = 0.5, zorder=0)

    for material, start_col in offsets.items():
        v = data[:, start_col + comp_idx]
        plt.plot(energy, v, label=material)

    plt.xlabel(r'$\varepsilon_F - \varepsilon_F^0$ (eV)')
    if comp_idx == 0 :
      plt.ylabel(r"$\langle v_{x}^2 \rangle$ (Ry)")
      plt.yticks(np.arange(0, 0.251, 0.05))
      plt.ylim([0.0,0.25])
    if comp_idx == 1 :
      plt.ylabel(r"$\langle v_{y}^2 \rangle$ (Ry)")
    if comp_idx == 2 :
      plt.ylabel(r"$\langle v_{z}^2 \rangle$ (Ry)")
      plt.yticks(np.arange(0, 0.201, 0.05))
      plt.ylim([0.0,0.20])
    # plt.title(f"Average |v_{component}|^2 vs Energy")
    plt.legend()
    plt.tight_layout()
    if comp_idx == 0 :
      plt.savefig('TaAs_family_vx2.pdf', bbox_inches='tight')
      plt.savefig('TaAs_family_vx2.png', dpi=300, bbox_inches='tight')
    if comp_idx == 1 :
      plt.savefig('TaAs_family_vy2.pdf', bbox_inches='tight')
      plt.savefig('TaAs_family_vy2.png', dpi=300, bbox_inches='tight')
    if comp_idx == 2 :
      plt.savefig('TaAs_family_vz2.pdf', bbox_inches='tight')
      plt.savefig('TaAs_family_vz2.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Plot v_x or v_z for 4 materials from combined data.")
    parser.add_argument("--file", default="avg_tot.dat", help="Input file name")
    args = parser.parse_args()

    energy, data, offsets = load_data('avg_tot.dat')
    plot_velocity(energy, data, offsets, 'x')
    plot_velocity(energy, data, offsets, 'z')

if __name__ == "__main__":
    main()