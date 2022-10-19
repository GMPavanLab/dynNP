# Data and analysis setup for -title here-

All of the required package will be installed with:

``` bash
python3 -m venv NPenv
source ./NPenv/bin/activate
pip install -U pip wheel
pip install -r requirements.txt
```

## NB

The file donw here are set up to reproduce exaclty the results obtained in our simulations, so if you want to apply the anlyiss to your data, you will need to modify the scripts.

## Simulations

If you have a recent version of lammps (with the [smatb/single](https://docs.lammps.org/pair_smatb.html) pair active) simply launch the script in `simulations`

## SOAP calculations

Prepare the SOAP trajectories with `bash ./run01_SOAP.sh`

## Bottom-up analysis

Prepare and run the BU analysis with `bash ./run02_BU.sh`

## Top-Down analysis

Prepare and run the TD analysis with `bash ./run02_TD.sh`
