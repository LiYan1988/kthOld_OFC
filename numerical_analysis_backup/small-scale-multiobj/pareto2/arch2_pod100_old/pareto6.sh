#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J arch2_old_6
#SBATCH -N 1
#SBATCH -t 12:00:00
#SBATCH -o arch2_old_6.stdout
#SBATCH -e arch2_old_6.stderr

module purge
module load python gcc/4.8/4.8.1 
module load acml/gfortran64_fma4_mp/5.3.0
module load numpy/py27/1.8.1-gcc48-acml_mp scipy/py27/0.14.0-gcc48-acml
module load untested gurobi

pdcp arch2_decomposition_new.py $TMPDIR
pdcp traffic_matrix_* $TMPDIR
pdcp pareto6.py $TMPDIR

cd $TMPDIR

python pareto6.py

cp *.csv $SLURM_SUBMIT_DIR

# End script
