#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J sensitivity-load
#SBATCH -N 1
#SBATCH -t 100:00:00
#SBATCH -o sensitivity-load.stdout
#SBATCH -e sensitivity-load.stderr

module purge
module load gcc/4.9/4.9.2


pdcp * $TMPDIR

cd $TMPDIR

g++ -std=c++11 -O3 -pthread runsa.cpp -o main
./main

cp *.csv $SLURM_SUBMIT_DIR
cp *.txt $SLURM_SUBMIT_DIR

# End script