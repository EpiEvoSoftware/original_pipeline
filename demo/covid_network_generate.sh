#!/bin/bash
#SBATCH --job-name=contact_net
#SBATCH --mail-type=ALL
#SBATCH --mail-user=sl984@cornell.edu
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=100G
#SBATCH --time=4-00:30:0

eval "$(conda shell.bash hook)"

conda activate trans_slim

SCRIPT_DIR=../enivol_packaging/enivol
WORK_DIR=/workdir/sl984/epievosoftware/original_pipeline/demo/data

mkdir -p $WORK_DIR # Create the working directory for this specific simulation

# Scale free graph host population structure for COVID
python $SCRIPT_DIR/network_generator.py \
    -popsize 10000 \
    -wkdir ${WORK_DIR} \
    -method randomly_generate \
    -model BA \
    -m 2

conda deactivate
