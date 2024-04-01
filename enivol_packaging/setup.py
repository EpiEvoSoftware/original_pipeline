import os
from setuptools import setup, find_packages

with open("README_PYPI.md", "r") as f:
    long_description = f.read()

setup(
    name = "enivol", # cannot repeat w/ other names on PyPI
    version = "0.0.1", # need to look into this
    description = "An epi-evo simulator for infectious disease outbreak", # description for the software 
    packages = find_packages(), # "flat-layout (a.k.a. adhoc structure, python automatically detects the package)"
    long_description = long_description, # readme
    long_description_content_type = "text/markdown", # confused
    include_package_data = True, # I think this will be for the template and stuff
    package_data = {"enivol": [os.path.join("burn_in_slim_scripts", "*.slim"),
                               os.path.join("config_template", "*.json"),
                               os.path.join("slim_scripts", "*.slim")]},
    url = "github",
    author = "Perry Xu, Shenni Liang",
    author_email = "shenni.liang@gmail.com",
    maintainer = "",
    maintainer_email = "",
    license = "MIT",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console', #CL tools
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: R'

    ],
    install_requires = ['matplotlib>=matplotlib=3.8.2', 'pandas>=2.2.0', 'ete3>=3.1.3', 'numpy>=1.26',
                        'tskit>=0.5.6', 'pyslim>=1.0.4'],
    python_requires = ">=3.12",
    keywords = ['phylodynamics', 'epidemiology', ''],
    entry_points = {
        'console_scripts': [
            'enivol = enivol.enivol:main',
            'network_generator = enivol.network_generator:main'
            'init_seq_generator = enivol.init_seq_generator:main',
            'genetic_effect_generator = enivol.genetic_effect_generator:main',
            'seed_host_matcher = enviol.seed_host_matcher:main'
            'outbreak_simulator = enivol.outbreak_simulator:main'
        ]
    }
)