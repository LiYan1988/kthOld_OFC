#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J simu1_arch2_3:
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -o simu1_arch2_3_output.stdout
#SBATCH -e simu1_arch2_3_output.stderr

module purge
module load python gcc/4.9 numpy/py27/1.8.1-gcc49-atlas
module load untested gurobi

pdcp arch2_3.py simu1_matrix_3.csv $TMPDIR

cd $TMPDIR

python arch2_3.py

cp * $SLURM_SUBMIT_DIR

# End script
