#!/usr/bin/env bash
#SBATCH -A C3SE407-15-3
#SBATCH -p hebbe
#SBATCH -J arch5_old1_1
#SBATCH -N 1
#SBATCH -n 20
#SBATCH -t 24:00:00
#SBATCH -o arch5_old1_1.stdout
#SBATCH -e arch5_old1_1.stderr

module purge
module load Python/2.7.10-intel-2015b untested gurobi

pdcp arch5_decomposition_new.py $TMPDIR
pdcp traffic_matrix_* $TMPDIR
pdcp template1.py  $TMPDIR

cd $TMPDIR

python template1.py

cp * $SLURM_SUBMIT_DIR

# End script
