**This repository contains all the necessary information to prepare and run three systems of Medin** — with two small molecule ligands (**ZINC265540661** and **ZINC2325837608**) and **urea** as a control. These were run using **16 replicas each**, with **multiple walker metadynamics**.

---

### **Ligand Preparation**

The ligands came from the **ZINC20** library and were parametrized using **OpenFF SAGE** software (details included in the `generating_input_files` directory).

---

### **Starting Configuration of Medin**

A **free single-replica simulation** of Medin (lactadherin human **Q08431**, AlphaFold web server, **residues 268–317 extracted**) was run at high temperature.  
**FASTA sequence**:  
`RLDKQGNFNAWVAGSYGNDQWLQVDLGSSKEVTGIITQGARNFGSVQFVA`

From this trajectory, **16 random frames** were selected to generate the **16 starting structures** for each replica.  
We then used **fpocket** to identify the best pocket per frame, and docked the ligands onto these pockets to determine the **best starting configuration** for the protein-ligand simulations.  
*Simulations therefore begin in the bound state.*

---

### **Preparing Protein–Ligand Complex for Metadynamics**

The `prep_file` is used to set up the systems (in **a99SBdisp.ff**), and the **PLUMED** files are included to run the metadynamics.  
A `plumed_reweight` file is also included for **unbiasing the simulations** during post-processing.  
The **16 replicas combined were run for just under 10 μs per system**.

---

### **Post-processing**

Post-processing is carried out in the analysis notebooks using the following code:

```python
import numpy as np

KBT = 2.49  # kJ/mol

def process_weights(w_file):
    data = np.loadtxt(w_file, comments="#")
    bias = data[:, -1]
    weights = np.exp(bias / KBT)
    weights /= weights.sum()
    return weights


def trim(file,n_reps,trim_fraction):
    w_split = np.array_split(file, n_reps)
    trimmed_chunks = [chunk[int(trim_fraction * len(chunk)):] for chunk in w_split]
    w_trimmed = np.concatenate(trimmed_chunks)
    return(w_trimmed)
