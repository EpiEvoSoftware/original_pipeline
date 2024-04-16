#!/bin/bash
#SBATCH --job-name=tb_seed
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
WORK_DIR=/workdir/sl984/epievosoftware/original_pipeline/demo/data_TB_seed_gen

mkdir -p ${WORK_DIR}

REF_PATH=/workdir/sl984/epievosoftware/original_pipeline/demo/data_TB_seed_gen/GCF_000195955.2_ASM19595v2_genomic.fna
# Match the seed sequences w/ hosts
python -u $SCRIPT_DIR/seed_generator.py \
    -wkdir $WORK_DIR \
    -seed_size 5 \
    -method SLiM_burnin_WF \
    -Ne 1000 \
    -ref_path $REF_PATH \
    -mu 1.1e-7 \
    -n_gen 6000

conda deactivate