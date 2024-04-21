#!/bin/bash
#SBATCH --job-name=TB
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
PATH_TO_COMPLETE_CONFIG=/workdir/sl984/epievosoftware/original_pipeline/demo/data_TB_complete/whole_config_minimal_seed.json

python -u ${SCRIPT_DIR}/enivol.py -path_config ${PATH_TO_COMPLETE_CONFIG}

conda deactivate