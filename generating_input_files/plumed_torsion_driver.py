## Using plumed driver

"""""
#gmx trjconv -s ../prod.tpr -f ../traj_comp.xtc -o lig.nojump.xtc -pbc nojump
#plumed driver --plumed plumed_torsion.dat --mf_xtc prod/lig.nojump.xtc --pdb cm10.pdb

MOLINFO STRUCTURE=cm10.pdb
WHOLEMOLECULES ENTITY0=1-82

t1:  TORSION ATOMS=9,24,23,21
t2:  TORSION ATOMS=23,24,9,8
t3:  TORSION ATOMS=23,24,18,17
t4:  TORSION ATOMS=17,10,11,12
t5:  TORSION ATOMS=11,10,9,8
t6:  TORSION ATOMS=16,11,10,9
t7:  TORSION ATOMS=6,8,9,24
t8:  TORSION ATOMS=7,6,8,9
t9:  TORSION ATOMS=10,9,8,6
t10: TORSION ATOMS=9,8,6,5
t11: TORSION ATOMS=4,5,6,7
t12: TORSION ATOMS=8,6,5,4
t13: TORSION ATOMS=25,5,6,8
t14: TORSION ATOMS=25,5,6,7
t15: TORSION ATOMS=26,25,5,6
t16: TORSION ATOMS=26,25,5,4
t17: TORSION ATOMS=4,3,2,1
t18: TORSION ATOMS=5,4,3,2
t19: TORSION ATOMS=49,3,2,1
t20: TORSION ATOMS=48,49,3,2
t21: TORSION ATOMS=32,31,48,49
t22: TORSION ATOMS=32,31,29,30
t23: TORSION ATOMS=32,31,29,28
t24: TORSION ATOMS=47,32,31,29
t25: TORSION ATOMS=47,32,31,48
t26: TORSION ATOMS=29,31,32,33
t27: TORSION ATOMS=34,33,32,31
t28: TORSION ATOMS=34,33,32,47
t29: TORSION ATOMS=35,34,33,32
t30: TORSION ATOMS=31,32,47,46
t31: TORSION ATOMS=32,47,46,35
t32: TORSION ATOMS=46,47,35,34
t33: TORSION ATOMS=47,46,35,36
t34: TORSION ATOMS=34,35,36,37
t35: TORSION ATOMS=46,35,36,37
t36: TORSION ATOMS=46,35,36,38
t37: TORSION ATOMS=34,35,36,38
t38: TORSION ATOMS=39,38,36,37
t39: TORSION ATOMS=39,38,36,35
t40: TORSION ATOMS=40,39,38,36
t41: TORSION ATOMS=45,40,39,38
t42: TORSION ATOMS=41,40,39,38

PRINT ARG=t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30,t31,t32,t33,t34,t35,t36,t37,t38,t39,t40,t41,t42 FILE=colvar STRIDE=10

"""""

import pandas as pd
import matplotlib.pyplot as plt



import pandas as pd
import matplotlib.pyplot as plt
import math

# Read header line from colvar file
with open("/Users/adelielouet/Documents/science/medin/cm8/cm8/free_ligand_simulation/parameter_files_openff_cm8/colvar") as f:
    for line in f:
        if line.startswith("#! FIELDS"):
            header_line = line.strip()
            break

# Extract column names
cols = header_line.replace("#! FIELDS ", "").split()

# Load data
colvar = pd.read_csv("/Users/adelielouet/Documents/science/medin/cm8/cm8/free_ligand_simulation/parameter_files_openff_cm8/colvar", delim_whitespace=True, comment="#", names=cols, header=None)

time_col = "time"

torsions = [c for c in cols if c != time_col]

plots_per_fig = 10
n_figs = math.ceil(len(torsions) / plots_per_fig)

for fig_idx in range(n_figs):
    start = fig_idx * plots_per_fig
    end = start + plots_per_fig
    torsion_subset = torsions[start:end]

    # Create figure with subplots (adjust rows/cols as needed)
    n = len(torsion_subset)
    cols_subplot = 2
    rows_subplot = math.ceil(n / cols_subplot)

    fig, axs = plt.subplots(rows_subplot, cols_subplot, figsize=(12, 3 * rows_subplot), sharex=True)
    axs = axs.flatten()

    for i, torsion in enumerate(torsion_subset):
        axs[i].plot(colvar[time_col], colvar[torsion], label=torsion)
        axs[i].set_title(f"{torsion} over time")
        axs[i].set_ylabel("Angle (rad)")
        axs[i].grid(True)
        axs[i].legend(fontsize='small')

    # Remove empty subplots if any
    for j in range(i+1, len(axs)):
        fig.delaxes(axs[j])

    plt.xlabel("Time (steps or frames)")
    plt.tight_layout()
    plt.show()
    plt.close(fig)
