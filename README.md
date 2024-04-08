# original_pipeline

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
