#!/usr/bin/env bash
#SBATCH -A C3SE407-15-3
#SBATCH -p hebbe
#SBATCH -J core_arch2_0
#SBATCH -N 1
#SBATCH -n 2
#SBATCH -t 24:00:00
#SBATCH -o core_arch2_0.stdout
#SBATCH -e core_arch2_0.stderr

module purge
module load Python/2.7.10-intel-2015b untested gurobi

pdcp arch2_decomposition_new.py $TMPDIR
pdcp traffic_matrix_* $TMPDIR
pdcp pareto0.py $TMPDIR

cd $TMPDIR

python pareto0.py

cp *.csv $SLURM_SUBMIT_DIR

# End script
