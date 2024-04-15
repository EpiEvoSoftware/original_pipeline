#!/bin/bash
#SBATCH --job-name=genetic_eff
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
EFFSIZE_PATH=/workdir/sl984/epievosoftware/original_pipeline/test/test_drugresist/causal_gene_info.csv

# Generate the genetic effects of genomic elements
python -u $SCRIPT_DIR/genetic_effect_generator.py \
    -wkdir $WORK_DIR \
    -method user_input \
    -effsize_path  $EFFSIZE_PATH \
    -trait_n '{"transmissibility": 1, "drug_resistance": 2}' \
    -n_seed 1

conda deactivate