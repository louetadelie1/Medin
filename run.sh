#!/bin/bash -l
# Standard output and error:
##SBATCH -o ./bench.out.%j
##SBATCH -e ./bench.err.%j
# Initial working directory:
#SBATCH -D ./
#
#SBATCH -J cm8
#
#SBATCH --partition=p.chem
#
# Request 10 nodes
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=48        # 48 MPI ranks per node
#SBATCH --cpus-per-task=2           # 1 thread per MPI rank
#SBATCH --gres=gpu:l40s:4           # 1 GPU per node
#SBATCH --time=24:00:00
##SBATCH --array=1-20:1%1

module purge
module load cmake/3.30
module load git/2.48
module load autoconf/2.71 automake/1.15 libtool/2.5.3
module load gcc/13
module load openmpi/5.0
module load anaconda/3/2023.03

export PATH=/u/adlouet/software/gromacs-2022.5_gpu_support/bin:$PATH
export PATH=/u/adlouet/software/plumed2/src/lib/plumed/bin:$PATH
export PATH="/u/adlouet/software/plumed2/src/lib/:$PATH"
export LIBRARY_PATH="/u/adlouet/software/plumed2/src/lib/:$LIBRARY_PATH"
export LD_LIBRARY_PATH="/u/adlouet/software/plumed2/src/lib/:$LD_LIBRARY_PATH"

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PLACES=cores

mpirun gmx_mpi mdrun -v -ntomp $OMP_NUM_THREADS -s prod_final.tpr -multidir rep_{0..15}/prod/ -plumed ../../plumed_files/plumed.dat -maxh 23.30 -pme gpu -pmefft gpu -bonded gpu -nb gpu -npme 1 -noappend -cpi state

