#!/usr/bin/env bash
#SBATCH -A C3SE407-15-3
#SBATCH -p hebbe
#SBATCH -J core_arch4_8
#SBATCH -N 1
#SBATCH -n 2
#SBATCH -t 24:00:00
#SBATCH -o core_arch4_8.stdout
#SBATCH -e core_arch4_8.stderr

module purge
module load Python/2.7.10-intel-2015b untested gurobi

pdcp arch4_decomposition_new.py $TMPDIR
pdcp traffic_matrix_* $TMPDIR
pdcp pareto8.py $TMPDIR

cd $TMPDIR

python pareto8.py

cp *.csv $SLURM_SUBMIT_DIR

# End script
