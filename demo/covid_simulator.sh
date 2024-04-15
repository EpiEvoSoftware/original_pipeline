#!/bin/bash
#SBATCH --job-name=simu_out
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
WORK_DIR=/workdir/sl984/epievosoftware/original_pipeline/demo/data_COVID_step_by_step
CONFIG_PATH=/workdir/sl984/epievosoftware/original_pipeline/demo/data_COVID_step_by_step/test_config.json

# Match the seed sequences w/ hosts
python -u $SCRIPT_DIR/outbreak_simulator.py -config $CONFIG_PATH

conda deactivate