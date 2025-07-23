This contains all the necessary information to prep and run 3 systems of medin - with 2 small molecule ligands (ZINC265540661 and ZINC2325837608) and urea as a control. These were run using 16 replicas each, with multiple walker metadynamics. 

Ligand Prep - The ligands came from the ZINC20 library, and parametrized using openff SAGE software (details included in generating_input_files). 

Starting Configuration of Medin - A free single replica simulation of the medin (lactadherin human Q08431 - AlphaFold web server - Residues 268:317 extracted - FASTA RLDKQGNFNAWVAGSYGNDQWLQVDLGSSKEVTGIITQGARNFGSVQFVA) was run at high temperature, and 16 random frames were selected throughout the simualtion to generate the 16 starting strucutres for each replica. We then used fpocket to identify the best pocket per frame, and proceeded to dock the following ligands on each pocket to find the best starting configuration for the protein-ligand simulations (simu will therefore begin in bound state).

Preparing Protein Ligand Complex for Metadynamics - The prep_file is used to prep the systems (in a99SBdisp.ff) and the plumed files are included to run the metadynamics. I have also included a plumed_reweight file that is used to unbias the simulations for post-processing. The 16 replicas combined were run for a bit under 10us per system. 

Post processing is then carried out in analysis notebooks using the following code-

w_eq = np.loadtxt(w_file)
def process_weights(w_file):
    KBT = 2.49  # kJ/mol
    colvar_file = w_file
    data = np.loadtxt(colvar_file, comments="#")
    bias = data[:, -1]
    weights = np.exp(bias / KBT)
    weights /= weights.sum() 

To account for equilirbartion artifacts, the first 10% of each replica was discarded (and the same done in the COVAR REWEIGHT file).

def trim(file,n_reps,trim_fraction):
    w_split = np.array_split(file, n_reps)
    trimmed_chunks = [chunk[int(trim_fraction * len(chunk)):] for chunk in w_split]
    w_trimmed = np.concatenate(trimmed_chunks)
    return(w_trimmed)
