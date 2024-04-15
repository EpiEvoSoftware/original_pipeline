#!/bin/bash
#SBATCH --job-name=seed_host_mat
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

# Match the seed sequences w/ hosts
python -u $SCRIPT_DIR/seed_host_matcher.py \
    -wkdir ${WORK_DIR} \
    -method randomly_generate \
    -n_seed 1 \
    -match_scheme  '{"0": "ranking"}' \
    -match_scheme_param '{"0": 5000}'

conda deactivate