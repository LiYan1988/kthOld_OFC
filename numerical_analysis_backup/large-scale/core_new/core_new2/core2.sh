#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p hebbe
#SBATCH -J core2
#SBATCH -N 1 -n 20
#SBATCH -t 20:00:00
#SBATCH -o core2.stdout
#SBATCH -e core2.stderr

module purge
module load GCC/6.1.0

pdcp * $TMPDIR

cd $TMPDIR

g++ -std=c++11 -O3 -pthread core2.cpp -o main
./main

cp *.csv $SLURM_SUBMIT_DIR
cp *.txt $SLURM_SUBMIT_DIR

# End script