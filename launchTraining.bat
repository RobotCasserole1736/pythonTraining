:: Make sure the latest kernel from the repo is installed
python .\TrainingKernel\install.py
:: Launch notebook server, but don't launch the home page
start "" jupyter notebook --no-browser
:: Launch the training itself in the user's chosen browser
:: start http://localhost:8888/notebooks/Training.ipynb