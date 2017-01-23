#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J load
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -o load.stdout
#SBATCH -e load.stderr

module purge
module load gcc/4.9/4.9.2

pdcp sa_sdm.h test_ajmal.cpp $TMPDIR

cd $TMPDIR

while sleep 600; do
    # This will be executed once per every 10 seconds
    cp $TMPDIR/*.csv $SLURM_SUBMIT_DIR/result
done &     # The &-sign after the done-keyword places 
           # the while-loop in a sub-shell in the background
LOOPPID=$! # Save the PID of the subshell running the loop

g++ -std=c++11 -O3 -pthread test_ajmal.cpp -o main
./main

cp *.csv $SLURM_SUBMIT_DIR
cp *.txt $SLURM_SUBMIT_DIR

# End script
kill $LOOPPID
