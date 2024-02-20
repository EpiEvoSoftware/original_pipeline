#!/bin/bash

#SBATCH --job-name=simulation
#SBATCH -o simulation_%j.out                  # output file (%j expands to jobID)
#SBATCH -e simulation_%j.err                  # error log file (%j expands to jobID)
#SBATCH --mail-type=ALL
#SBATCH --mail-user=px54@cornell.edu
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=2
#SBATCH --mem-per-cpu=80G
#SBATCH --time=4-00:30:00

####################################################
## This is a pipeline for an individually contact network-based pathogen outbreak simulation in one host population.
## The main purpose is to conduct a transmissibility inference study.



####################################################
## Environmental variables for preparation (Reading in a config file):
config_file="/Users/px54/Documents/TB_software/covid_test/params.config"
codes_dir="/Users/px54/Documents/TB_software/V1_codes"

while IFS=":" read -r key value; do
    declare "$key=$value"
done < ${config_file}





####################################################


####################################################
## STEP 0: PREPARING INPUTS FOR SLIM SIMULATION
## 0.0  Generate or process seeds' .vcf file, depending on whether seed's files are provided
if [ -f "${seeds_vcf}" ]; then
    echo "Using user's file as input"
    python ${codes_dir}/convert_external_vcf.py  ## A script to check and convert user_input file to standard format Ask user to provide fasta
else
    ## Now we copy config file to the codes' directory to run burn-in, however we would want to generate SLiM scripts later by hard code.
    cp ${config_file} ${codes_dir}
    slim ${codes_dir}/burn-in.slim # this will generate a "seeds.vcf"
    ######## Check before the SLiM
    echo "Burn-in Finished"
    ## This will also generate a .trees file for the seeds, however, this tree doesn't necessarily coalesce.
    ## Choice 1: Rerun untill we get something that coalesce (might be running forever)
    ## Choice 2: Using other tree reconstruction algorithm to reconstruct the tree (ensuring the tree is dated, so that the seeds are introduced at the same date)
    ## ********** SUBJECT TO DISCUSSION ************************
    python ${codes_dir}/tree_process.py  -wk_dir ${cwdir}/  -scale_time 12
fi





## 0.1 Split the seeds' vcf files
cd ${cwdir}
python ${codes_dir}/seeds_vcf_split.py -wk_dir ${cwdir}/  \
    -seed_size ${seed_size}     # This will generate seed.x.vcf, x in [0:seed_size-1]
mkdir ${cwdir}/originalvcfs                  # Create a new subdirectory to store these new vcf files.
mv ${cwdir}/seed.*.vcf ./originalvcfs/
rm ${cwdir}/seeds.vcf




## 0.2 Choose causal genes and effect size for transmissibility (normalized to expected maximum # of mutations at the end of the simulation)
if [ -f "${causal_gene_path}" ]; then
    echo "Using user's effect size file as input"
    cat ${causal_gene_path} > causal_gene_info.csv
    ## A script to check and convert user_input file to standard format, for now just store it in the standard file name  *********NOT FINISHED YET***************
else
    python ${codes_dir}/effsize.py \
        -gff ${gff} \
        -causal_1 ${n_causal_genes_1} -es_low_1 ${efsize_min_1} -es_high_1 ${efsize_max_1} \
        -causal_2 ${n_causal_genes_2} -es_low_2 ${efsize_min_2} -es_high_2 ${efsize_max_2} \
        -wk_dir ${cwdir}/ -sim_generation ${n_generation} -mut_rate ${mut_rate}
    # Effect size now is randomly generated uniformly between efsize_min and efsize_max, then normalize to the expected number of mutations at the end of the simulation
    # i.e. Average for the sum of effect size per genome is expected to be 1 at the end of the simulation
    # This definitely needs further refinement
fi
echo "Effect sizes generated!"




## 0.3 Generate a contact network for the host population
if [ -f "${contact_network_path}" ]; then
    echo "Using user's effect size file as input"
    cat ${contact_network_path} > contact_network.adjlist.modified
    ## A script to check and convert user_input file to standard format, for now just store it in the standard file name  *********NOT FINISHED YET***************
else
    python ${codes_dir}/network_generate.py \
        -popsize ${host_size} \
        -wkdir ${cwdir}/ \
        -method ${network_model} -p_ER ${p_ER} -rp_size ${rp_size} -p_within ${p_within} -p_between ${p_between} -m ${ba_m}
    ## This will generate an adjacent list file called "contact_network.adjlist.modified"
    ## To use different random network model, will have to change the method in config file and the parameter
fi
echo "Network generated!"

## 0.4 Match seeds with hosts
python ${codes_dir}/seed_host_match.py -wk_dir ${cwdir}/ \
    -seed_size ${seed_size} -host_size ${host_size} \
    -match_method random



####################################################
## STEP 1: SLIM SIMULATION

## 1.1 Generate SLiM script
cd ${codes_dir}/slim_code/
bash generate_slim.sh
cd ..
cp ${codes_dir}/slim_code/main_generated.slim .
## 1.2 Run the SLiM simulation
# Now, the seeded individuals are randomly chosen in SLiM and SLiM will store the ids of the seeded hosts.
#mkdir ${cwdir}/sample_vcfs
#slim ${codes_dir}/main_generated.slim
#echo "SLiM finished!"

# bash run_slim.sh
sim_count=0
while [ ${sim_size} -gt ${sim_count} ]
do
    echo ${sim_count}
    mkdir ${cwdir}/${sim_count}
    mkdir ${cwdir}/sample_vcfs
    slim ${codes_dir}/main_generated.slim > ${cwdir}/${sim_count}/slim.log
    mv ${cwdir}/sample_vcfs ${cwdir}/${sim_count}
    mv ${cwdir}/sampled_genomes.trees ${cwdir}/${sim_count}
    mv ${cwdir}/*.txt.gz ${cwdir}/${sim_count}
    gunzip ${cwdir}/${sim_count}/*.gz
    # MacOS: gunzip ${cwdir}/*.gz
    # Linux: bgzip -d ${cwdir}/*.gz
    mkdir ${cwdir}/${sim_count}/transmission_tree
    python ${codes_dir}/treeseq_post_processing.py -wk_dir ${cwdir}/${sim_count}
    sim_count=$((sim_count+1))
done





####################################################
## STEP 2: Tidying (and converting) SLiM output

## 2.1 Producing transmission trees and metadata files for the tree, and vcf files
mkdir ${cwdir}/transmission_tree
python ${codes_dir}/treeseq_post_processing.py -wk_dir ${cwdir}/

## 2.2 Generating a plot for the transmission tree (separately or jointly if seeds' genealogy is provided)
Rscript 




: << 'END_COMMENT'
## 2.5 Convert the sampled.vcf files of SLiM output to fastas
cd ${cwdir}/sample_vcfs/
# Compress all sampled vcf, and index them
for i in *.named.vcf; do
bgzip $i
bcftools index $i.gz
done
# Merge all vcf.gz
bcftools merge *.vcf.gz -O v -o ${cwdir}/samples.merged.vcf
## Needs to convert the .s entry to 0s
python ${codes_dir}/vcf.20.py \
    -wk_dir ${cwdir}/
echo "Samples vcf merged!"




## 2.6.1 Generate whole genome fasta files for samples
cd ${cwdir}
Rscript ${codes_dir}/vcf2fasta.R -wk_dir ${cwdir}/
sed -i 's/X/p/' ${cwdir}/sample.fasta
echo "Samples fasta generated!"
## 2.6.2 Generate SNPs-only fasta files for samples
Rscript ${codes_dir}/vcf2snpfasta.R -wk_dir ${cwdir}/
sed -i 's/X/p/' ${cwdir}/sample.SNPs_only.fasta
echo "Samples fasta generated!"




## 2.7.1 Time the whole genome fasta files for samples
python ${codes_dir}/timefasta.py \
    -wk_dir ${cwdir}/ -year sim_start_y -month sim_start_m \
    -fa sample.fasta
## 2.7.2 Time the SNPs-only fasta files for samples
python ${codes_dir}/timefasta.py \
    -wk_dir ${cwdir}/ -year sim_start_y -month sim_start_m \
    -fa sample.SNPs_only.fasta
## Time the out group / reference genome
sed -i "s/>/>H37Rv|${sim_start_y}-${sim_start_m}-01/" ${cwdir}/reference.snpsonly.fasta
# Now the time file can only time by monthly grid, changing for different time grid in the future.




## 2.8 Concatenate SNPs sampled fasta and SNP reference fasta (This is for our use to build a tree, idk whether we want to implement this for the user)
cat ${cwdir}/reference.snpsonly.fasta sample.SNPs_only.timed.fasta > ${cwdir}/sample.SNPs_only.timed.withref.fasta




## 2.9 Arrange and tidy up intermediate files and output
# Move all files related to seeds to the seeds_info subdirectory
mkdir ${cwdir}/seeds_info
mv ${cwdir}/seeds.* ${cwdir}/seeds_info
# Move all epidemiological log files to the epidemiology_log subdirectory
mkdir ${cwdir}/epidemiology_log
mv ${cwdir}/*.txt ${cwdir}/epidemiology_log




####################################################
## STEP 3: Visualization of results
## 3.1 Plot the SEIR trajectory
Rscript SEIR_trajectory.R ${cwdir}/SIR_trajectory.txt ${cwdir}/

## 3.2 Plot the strain distribution (color the drug treatment time in the background)

## 3.3 Plot the transmission tree




