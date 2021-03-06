#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J simu3_arch2_0
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -o simu3_arch2_0_output.stdout
#SBATCH -e simu3_arch2_0_output.stderr

module purge
module load python gcc/4.9 numpy/py27/1.8.1-gcc49-atlas
module load untested gurobi

pdcp arch2_pod150_0.py simu3_matrix_0.csv $TMPDIR

cd $TMPDIR

python arch2_pod150_0.py

cp * $SLURM_SUBMIT_DIR

# End script
