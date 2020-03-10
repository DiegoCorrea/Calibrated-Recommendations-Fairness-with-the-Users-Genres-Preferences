#!/bin/sh

salloc -c 2 -p long

source "/home_nfs/diegocorrea/.bashrc"
conda activate calibrated_recommendation

SBATCH --partition=long --qos=long
SBATCH --nodes=2
SBATCH --mem=10000
SBATCH --job-name="calibrated"
SBATCH --output=log/output_terminal.log

echo "SLURM_JOBID="$SLURM_JOBID
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
echo "SLURM_NNODES"=$SLURM_NNODES
echo "SLURMTMPDIR="$SLURMTMPDIR

echo "/home_nfs/diegocorrea/Calibrated-Recommendations-Fairness-with-the-Users-Genres-Preferences = "$SLURM_SUBMIT_DIR

module load intel/13.1
module load intel-mpi/4.1.3
module list
ulimit -s unlimited

NPROCS="srun --nodes=${SLURM_NNODES} bash -c 'hostname' |wc -l"
echo NPROCS=$NPROCS

srun python main.py

