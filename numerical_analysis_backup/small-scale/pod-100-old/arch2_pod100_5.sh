#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J simu1_arch2_5:
#SBATCH -N 1
#SBATCH -t 50:00:00
#SBATCH -o simu1_arch2_5_output.stdout
#SBATCH -e simu1_arch2_5_output.stderr

module purge
module load python gcc/4.9 numpy/py27/1.8.1-gcc49-atlas
module load untested gurobi

pdcp arch2_pod100_5.py simu1_matrix_5.csv $TMPDIR

cd $TMPDIR

python arch2_pod100_5.py

cp * $SLURM_SUBMIT_DIR

# End script
