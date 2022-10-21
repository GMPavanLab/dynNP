# Data and analysis setup for -title here-

All of the required package will be installed with:

``` bash
python3 -m venv NPenv
source ./NPenv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install --upgrade joblib==1.1.0
```

the last line, with the downgrade of joblib, is due to a bug in the requirements of hdbscan 0.8.28

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

## Visualization

Prepare and run the visualizations with with `bash ./run03_visualization.sh`

This script is more set up to be used on the dataset of the article, whereas the others are more general and can be used with other datasets.
With this, we mean that the object in the 'figure' folder needs more work to be adapted for analyzing new data.

And includes a workaround to a problem that arises when working with ovito

### Remarks

The Bottom-up and the Top-Down can be executed in any order on in parallel
