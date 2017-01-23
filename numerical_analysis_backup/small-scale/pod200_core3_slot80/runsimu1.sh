#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J pod200_1
#SBATCH -N 1
#SBATCH -t 50:00:00
#SBATCH -o pod200_1.stdout
#SBATCH -e pod200_1.stderr

module purge
module load python gcc/4.8/4.8.1 
module load acml/gfortran64_fma4_mp/5.3.0
module load numpy/py27/1.8.1-gcc48-acml_mp scipy/py27/0.14.0-gcc48-acml
module load untested gurobi

pdcp arch1.py arch2_decomposition.py arch4_decomposition.py $TMPDIR
pdcp arch5_decomposition.py $TMPDIR
pdcp runsimu1.py traffic_matrix_* $TMPDIR

cd $TMPDIR

python runsimu1.py

cp result1.csv $SLURM_SUBMIT_DIR

# End script
