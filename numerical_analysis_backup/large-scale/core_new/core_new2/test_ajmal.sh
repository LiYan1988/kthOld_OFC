#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p hebbe
#SBATCH -J core1
#SBATCH -N 1 -n 10
#SBATCH -t 20:00:00
#SBATCH -o core1.stdout
#SBATCH -e core1.stderr

module purge
module load GCC/6.1.0

pdcp * $TMPDIR

cd $TMPDIR

g++ -std=c++11 -O3 -pthread test_ajmal.cpp -o main
./main

cp *.csv $SLURM_SUBMIT_DIR
cp *.txt $SLURM_SUBMIT_DIR

# End script