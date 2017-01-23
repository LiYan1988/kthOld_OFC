#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J pareto_arch5_pod100_nf_4
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -o pareto_arch5_pod100_nf_4.stdout
#SBATCH -e pareto_arch5_pod100_nf_4.stderr

module purge
module load python gcc/4.8/4.8.1 
module load acml/gfortran64_fma4_mp/5.3.0
module load numpy/py27/1.8.1-gcc48-acml_mp scipy/py27/0.14.0-gcc48-acml
module load untested gurobi


pdcp arch5_decomposition_new.py sdm1.py traffic_matrix_* $TMPDIR
pdcp pareto4.py $TMPDIR

cd $TMPDIR

python pareto4.py

cp *.csv $SLURM_SUBMIT_DIR

# End script
