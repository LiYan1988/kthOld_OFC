#!/usr/bin/env bash
#SBATCH -A C3SE407-15-3
#SBATCH -p hebbe
#SBATCH -J core_arch5_2_9
#SBATCH -N 1
#SBATCH -n 20
#SBATCH -t 24:00:00
#SBATCH -o core_arch5_2_9.stdout
#SBATCH -e core_arch5_2_9.stderr

module purge
module load Python/2.7.10-intel-2015b untested gurobi

pdcp arch5_decomposition_new.py $TMPDIR
pdcp traffic_matrix_* $TMPDIR
pdcp pareto29.py $TMPDIR

cd $TMPDIR

python pareto29.py

cp *.csv $SLURM_SUBMIT_DIR

# End script
