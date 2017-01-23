#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J simu4_arch2_11
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -o simu4_arch2_11_output.stdout
#SBATCH -e simu4_arch2_11_output.stderr

module purge
module load python gcc/4.9 numpy/py27/1.8.1-gcc49-atlas
module load untested gurobi

pdcp arch2_pod175_11.py simu4_matrix_11.csv $TMPDIR

cd $TMPDIR

python arch2_pod175_11.py

cp * $SLURM_SUBMIT_DIR

# End script
