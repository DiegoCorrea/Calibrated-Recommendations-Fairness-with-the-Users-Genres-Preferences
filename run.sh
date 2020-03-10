#!/bin/sh

source "/home_nfs/diegocorrea/.bashrc"
conda activate calibrated_recommendation

ulimit -s unlimited

salloc -c 2 -p gpu
srun python main.py

