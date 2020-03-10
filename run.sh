#!/bin/sh

#source "/home_nfs/diegocorrea/.bashrc"
#conda activate calibrated_recommendation
#
#sbatch --partition=gpu --qos=gpu
#sbatch --nodes=2
#sbatch --mem=10000
#sbatch --job-name="calibrated"
#sbatch --output=log/
#
#echo "SLURM_JOBID="$SLURM_JOBID
#echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
#echo "SLURM_NNODES"=$SLURM_NNODES
#echo "SLURMTMPDIR="$SLURMTMPDIR  # Comando não esta adicionando nada
#
#echo "/home_nfs/diegocorrea/Calibrated-Recommendations-Fairness-with-the-Users-Genres-Preferences/ = "$SLURM_SUBMIT_DIR
#
#ulimit -s unlimited
#
#NPROCS="srun --nodes=${SLURM_NNODES} bash -c "hostname" |wc -l"
#echo NPROCS=$NPROCS

salloc -c 2 -p gpu
srun python main.py

