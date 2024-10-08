# HtautauRegression

MPHYS project on tau-pair mass regression for H->tautau and HH->bbtautau 

# Instructions

## Log on

```bash
# Logon to alpha machine
ssh alpha.ph.liv.ac.uk
```

## First time setup

```bash
# Download this package
git clone https://github.com/carlgwilliam/HtautauRegression
cd HtautauRegression

# Set up a virtual environment
source setup/setup_conda.sh
mamba create -n Mtautau python=3.10

# Acivate the virtual enviroment
conda activate Mtautau

# Install required packages
python -m pip install -e .
```

## Subsequent setup

```bash

# Resetup conda
source setup.sh

# Reacivate the virtual enviroment
conda activate Mtautau
```

## Running

```bash

# On alpha, un jupyter lab with no browser
jupyer lab --no-browser --port 8888

# On your laptop create an ssh tunnel to alpha
ssh -L 8888:localhost:8888 <userame>@alpha.ph.liv.ac.uk cat -

# Point your local web browser to localhost:8888 to access jupyter
# and paste in the token displayed in the terminal on alpha
```




