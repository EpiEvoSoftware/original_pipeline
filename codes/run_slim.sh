#!/bin/bash


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
	mkdir ${cwdir}/${sim_count}/transmission_tree
	python ${codes_dir}/treeseq_post_processing.py -wk_dir ${cwdir}/${sim_count}
	sim_count=$((sim_count+1))
done