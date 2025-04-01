#!/bin/bash
#SBATCH --account mutationalscanning
#SBATCH --time 10:00:00
#SBATCH -c 32
#SBATCH --mem 256g

source $(conda info --base)/etc/profile.d/conda.sh
conda activate kinetics_modelling
python fetch_null_kinetics.py