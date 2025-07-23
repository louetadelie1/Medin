import MDAnalysis as mda
import numpy as np
import os
import glob
import shutil

path_files=('/Users/adelielouet/Documents/science/medin/cm10/cm10')

for x in range(0,47):
    stp_pockets = glob.glob(path_files+f'/rep_{x}/pair*_out/pair*_out.pdb')[0]
    original_pdb=glob.glob(path_files+f'/rep_{x}/pair*.pdb')[0]
    apo_pock = mda.Universe(stp_pockets)
    STP=apo_pock.select_atoms('resid 1'+' and resname STP')
    stp_pos=STP.atoms.positions
    #print(STP.center_of_geometry())

    os.makedirs(path_files+f'/rep_{x}/docked',exist_ok=True)

    new_dir=(path_files+f'/rep_{x}/docked')
    shutil.copy2(original_pdb,new_dir)
    try:
        with open(new_dir+f'/pair{x}_box.txt', "a") as file:
            print(file)
            file.write(f"center_x = {STP.center_of_geometry()[0]}\n")
            file.write(f"center_y = {STP.center_of_geometry()[1]}\n")
            file.write(f"center_z = {STP.center_of_geometry()[2]}\n")
            file.write("size_x = 20.0\n")
            file.write("size_y = 20.0\n")
            file.write("size_z = 20.0\n")
    except Exception as e:
        print(f"rep_{x} didn't work with fpocket")

subprocess.call(['for x in rep_*; do (cd $x && /Users/adelielouet/Documents/science/dd_proj/docking_other_systems/ADFRsuite_x86_64Darwin_1.0/bin/prepare_receptor -r *.pdb -A "hydrogens" -o medin.pdbqt);done'], shell=True, cwd=new_path)

rep_{2,20,23,31,47}

for x in rep_{2,20,23,31,47}; do (cd $x && vina --receptor medin.pdbqt --ligand ../ZINC000265540661.pdbqt --config docked/*box.txt --exhaustiveness=32 --out medin_docked.pdbqt);done'
