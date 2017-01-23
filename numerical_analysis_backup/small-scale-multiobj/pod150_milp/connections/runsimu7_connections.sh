#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J pod150_7_connections
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -o pod150_7_connections.stdout
#SBATCH -e pod150_7_connections.stderr

module purge
module load python gcc/4.8/4.8.1 
module load acml/gfortran64_fma4_mp/5.3.0
module load numpy/py27/1.8.1-gcc48-acml_mp scipy/py27/0.14.0-gcc48-acml
module load untested gurobi

pdcp arch1.py arch2_decomposition.py arch4_decomposition.py $TMPDIR
pdcp arch5_decomposition.py sdm1.py traffic_matrix_* $TMPDIR
pdcp runsimu7_connections.py $TMPDIR

cd $TMPDIR

python runsimu7_connections.py

cp *.csv $SLURM_SUBMIT_DIR

# End script
