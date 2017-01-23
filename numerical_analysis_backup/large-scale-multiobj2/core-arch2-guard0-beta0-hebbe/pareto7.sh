#!/usr/bin/env bash
#SBATCH -A C3SE407-15-3
#SBATCH -p hebbe
#SBATCH -J core_arch2_7
#SBATCH -N 1
#SBATCH -n 2
#SBATCH -t 24:00:00
#SBATCH -o core_arch2_7.stdout
#SBATCH -e core_arch2_7.stderr

module purge
module load Python/2.7.10-intel-2015b untested gurobi

pdcp arch2_decomposition_new.py $TMPDIR
pdcp traffic_matrix_* $TMPDIR
pdcp pareto7.py $TMPDIR

cd $TMPDIR

python pareto7.py

cp *.csv $SLURM_SUBMIT_DIR

# End script
