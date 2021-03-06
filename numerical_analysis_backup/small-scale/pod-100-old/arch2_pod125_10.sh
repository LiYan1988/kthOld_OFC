#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J simu2_arch2_10:
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -o simu2_arch2_10_output.stdout
#SBATCH -e simu2_arch2_10_output.stderr

module purge
module load python gcc/4.9 numpy/py27/1.8.1-gcc49-atlas
module load untested gurobi

pdcp arch2_pod125_10.py simu2_matrix_10.csv $TMPDIR

cd $TMPDIR

python arch2_pod125_10.py

cp * $SLURM_SUBMIT_DIR

# End script
