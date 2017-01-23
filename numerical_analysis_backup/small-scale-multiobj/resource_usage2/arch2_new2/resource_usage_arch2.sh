#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J RU_arch2_pod100_new2
#SBATCH -N 1
#SBATCH -t 50:00:00
#SBATCH -o RU_arch2_pod100.stdout
#SBATCH -e RU_arch2_pod100.stderr

module purge
module load python gcc/4.8/4.8.1 
module load acml/gfortran64_fma4_mp/5.3.0
module load numpy/py27/1.8.1-gcc48-acml_mp scipy/py27/0.14.0-gcc48-acml
module load untested gurobi

pdcp arch2_decomposition_new.py $TMPDIR
pdcp traffic_matrix.csv $TMPDIR
pdcp resource_usage_arch2.py  $TMPDIR

cd $TMPDIR

python resource_usage_arch2.py

cp * $SLURM_SUBMIT_DIR

# End script
