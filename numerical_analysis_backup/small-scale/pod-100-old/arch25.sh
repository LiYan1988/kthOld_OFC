
#!/usr/bin/env bash
#SBATCH -A C3SE2016-1-11
#SBATCH -p glenn
#SBATCH -J arch2_main_0_pod100
#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -o arch2_main_0_pod100_output.stdout
#SBATCH -e arch2_main_0_pod100_output.stderr

module purge
module load gcc/4.8/4.8.1

pdcp arch2_main_0_pod100.cpp arch2.h $TMPDIR

cd $TMPDIR

g++ -std=c++11 -pthread -O3 arch2_main_0_pod100.cpp -o main
./main

cp * $SLURM_SUBMIT_DIR

# End script
