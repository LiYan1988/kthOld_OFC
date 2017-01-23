#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J sa_pod100_core3_slot80
#SBATCH -N 1
#SBATCH -t 80:00:00
#SBATCH -o sa_pod100_core3_slot80_output.stdout
#SBATCH -e sa_pod100_core3_slot80_output.stderr

module purge
module load gcc/4.9/4.9.2


pdcp * $TMPDIR

cd $TMPDIR

g++ -std=c++11 -O3 -pthread runsa.cpp -o main
./main

cp *.csv *.txt $SLURM_SUBMIT_DIR

# End script