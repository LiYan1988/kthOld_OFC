#!/usr/bin/env bash
#SBATCH -A C3SE407-15-3
#SBATCH -p hebbe
#SBATCH -J core_arch5_9
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -t 12:00:00
#SBATCH -o core_arch5_9.stdout
#SBATCH -e core_arch5_9.stderr

module purge
module load Python/2.7.10-intel-2015b untested gurobi

pdcp arch5_decomposition_new.py $TMPDIR
pdcp traffic_matrix_* $TMPDIR
pdcp pareto9.py $TMPDIR

cd $TMPDIR

python pareto9.py

cp *.csv $SLURM_SUBMIT_DIR

# End script
