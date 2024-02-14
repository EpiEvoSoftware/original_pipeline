#!/bin/bash

while IFS=":" read -r key value; do
    declare "$key=$value"
done < "../params.config"

if [ -e "main_generated.slim" ]; then
	rm main_generated.slim
fi
touch main_generated.slim
cat trait_calc_function.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
cat initialization.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
cat mutation_effsize.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
cat block_control.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
cat seeds_read_in.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
cat contact_network_read_in.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
cat self_reproduce.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
if [ ${trans_type}="additive" ]; then
	cat transmission_additive.slim >> main_generated.slim
else
	cat transmission_bialleleic.slim >> main_generated.slim
fi
echo -e "\n" >> main_generated.slim
if [ -z ${within_host_evolution} ]; then
	true
else
	cat within_host_reproduce.slim >> main_generated.slim
	echo -e "\n" >> main_generated.slim
fi
cat kill_old_pathogens.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
if [ "${model}" == "SEIR" ]; then
	cat Exposed_process.slim >> main_generated.slim
	echo -e "\n" >> main_generated.slim
fi
if [ -z ${multiple_epochs} ]; then
	true
else
	cat change_epoch.slim >> main_generated.slim
	echo -e "\n" >> main_generated.slim
fi
cat Infected_process.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
if [ -z ${treatment} ]; then
	true
else
	if [ "${dr_type}" == "additive" ]; then
		cat Infected_process_treatment_additive.slim >> main_generated.slim
	else
		cat Infected_process_treatment_bialleleic.slim >> main_generated.slim
	fi
	echo -e "\n" >> main_generated.slim
fi
if [ -z ${massive_sampling} ]; then
	True
else
	cat massive_sampling.slim >> main_generated.slim
	echo -e "\n" >> main_generated.slim
fi
if [ -z ${super_infection} ]; then
	cat New_infection_process.slim >> main_generated.slim
else
	cat New_infection_process_superinfection.slim >> main_generated.slim
fi
echo -e "\n" >> main_generated.slim
if [[ $(echo "${RS_rate} > 0" | bc -l ) ]]; then
	cat Recovered_process.slim >> main_generated.slim
	echo -e "\n" >> main_generated.slim
fi
cat log.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim
cat finish_simulation.slim >> main_generated.slim
echo -e "\n" >> main_generated.slim

