#!/bin/sh

source "/home_nfs/diegocorrea/.bashrc"
salloc -c 2 -p gpu
conda activate calibrated_recommendation

ulimit -s unlimited

srun python main.py

