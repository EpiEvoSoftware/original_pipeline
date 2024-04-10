## About The Project

EnivolCrossing is an outbreak simulator that features the coupling of pathogen evolution and various epidemiological scenarios. It is designed to be easily used by users with few or no coding experience by launching a GUI that sets up all the simulation configurations, but can also be tuned by module on command line for users with coding experience. It's supported in MacOS system and Linux system.

See our manuscript at (manuscript url).

See the manual at (https://github.com/EpiEvoSoftware/original_pipeline/blob/main/Manual_software.pdf)

## Getting Started

### Installation

* Using docker
  Run the following command:
  ```sh
  docker ...
  ```
  
* Using conda & git clone
  1. Clone the repository
  ```sh
  git clone https://github.com/EpiEvoSoftware/original_pipeline
  ```
  
  2. Create a conda enviornment by our configuration file. For MacOS users, change `YOUR_YML` to `mac_env_w_builds.yml`. For Linux users, change `YOUR_YML` to `linux_env_w_builds.yml`.
  ```sh
  cd original_pipeline
  conda env create --name enivol --file YOUR_YML
  ```
  If environment solving failed or you encounter any error message about importing packages in testing (step 4). Please do `conda deactivate` to leave the environment and delete it by `conda remove --name enivol --all`, then restart from step 3 by using the no-builds options of the yml file (`mac_env_wo_builds.yml` for MacOS or `linux_env_w_builds.yml` for Linux).
  
  3. Activate the conda environment
  ```sh
  conda activate enivol
  ```
  
  4. Test whether the software is installed correctly by running a minimal model
  ```sh
  cd enivol_packaging/enivol
  CODESDIR=${PWD}
  cd ..
  cd ../test/test_minimal_model
  python -u ${CODESDIR}/outbreak_simulator.py -config test_config.json
  ```
  You should see standard output printing in your terminal that shows the processing of the simulator and you should be able to see output files in your current directory after it finished if the installation is successful.


### Usage

1. Find a working directory (in most circumstances, create a new empty directory not in the github repo you cloned). This directory will be your "working directory", any files generated throughout usage will be stored there along with the simulation results. Thus you want to use separate working directories for different simulation configurations. Since this working directory will need to be provided in all the modules, store the path to `WORKDIR`.
```sh
WORKDIR=YOUR_WORKING_DIRECTORY
```

2. Generate a configuration file and all prerequisites for the current simulation.
   * By GUI
     
   We provide an interative option for the pre-simulation settings.
  ```sh
  python gui
  ```
  A GUI will pop up and you will be asked to navigate to your working directory in the first tab. By going through all the tabs, all the simulation presettings will be finished, and a configuation file called `simulation_config.json` will be generated in the working directory as well. For further information on how to use the GUI, please refer to the manual Chapter X.
  
   * By command line
     
  Command line options for the pre-simulatuion programs includes NetworkGenerator, SeedGenerator and SeedHostMatcher. Please refer to the manual chapter Y-Z as for how to run them sequentially and consistently. Note that `${WORKDIR}` should be provided for each program in option `-wkdir` to ensure that they are consistent. After these programs, you need to create a configuration file by changing the options listed in the config file template. For explanations of the config file, please refer to Manual chapter T.
```sh
cp ${CODESDIR}/config_template/slim_only_template.json ${WORKDIR}/simulation.config
## Then manually change the configuration in ${WORKDIR}/simulation.config.
```

3. Run the simulation
```sh
python -u ${CODESDIR}/outbreak_simulator.py -config ${WORKDIR}/simulation.config
```

4. (Alternative to 2 & 3) Run the pre-simulation programs and the simulator in one command. You need to fill out a bigger configuration file.
```sh
cp ${CODESDIR}/config_template/base_params.json ${WORKDIR}/simulation.config
## Then manually change the configuration in ${WORKDIR}/simulation.config.
## After which, do
python -u ${CODESDIR}/enivol.py -config ${WORKDIR}/simulation.config
```

## Liscence











================================

Run ```conda env update --name myenvname --file environment.yml --prune`` to be updated w/ dependencies for backend
or
Run ```conda env create -f environment.yml``` to initialize conda env

https://akrabat.com/creating-virtual-environments-with-pyenv/
https://stackoverflow.com/questions/42352841/how-to-update-an-existing-conda-environment-with-a-yml-file


deployment: https://github.com/TomSchimansky/CustomTkinter/issues/2322


distributing for macos:
pip install pyinstaller
pyinstaller --onefile --windowed --icon=__icon__.ico __script__.py

https://www.pythonguis.com/tutorials/packaging-tkinter-applications-windows-pyinstaller/
