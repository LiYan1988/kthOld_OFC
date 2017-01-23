#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p hebbe
#SBATCH -J sa_pod150_core3_slot80
#SBATCH -N 1 -n 20
#SBATCH -t 80:00:00
#SBATCH -o sa_pod150_core3_slot80_output.stdout
#SBATCH -e sa_pod150_core3_slot80_output.stderr

module purge
module load GCC/6.1.0


pdcp * $TMPDIR

cd $TMPDIR

g++ -std=c++11 -O3 -pthread runsa.cpp -o main
./main

cp *.csv $SLURM_SUBMIT_DIR
cp *.txt $SLURM_SUBMIT_DIR

# End script