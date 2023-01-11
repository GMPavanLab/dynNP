# Data and analysis setup for "Machine Learning of Atomic Dynamics and Statistical Surface Identities in Gold Nanoparticles"

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

The file in this repository are tailored to reproduce precisely the results obtained in our simulations (starting from the data that are present in the zenodo link and/or in the [release on github](https://github.com/GMPavanLab/dynNP/releases/tag/V1.0-trajectories)), so if you want to apply the analysis to your data, you will need to modify the scripts.

## Simulations

If you have a recent version of lammps (with the [smatb/single](https://docs.lammps.org/pair_smatb.html) pair active) simply launch the script in `simulations`
And then preprocess the trajectories with `bash ./run00_preprocessTrajectories.sh`

OR

You may download the precompressed trajectory from the [release page on github](https://github.com/GMPavanLab/dynNP/releases/tag/V1.0-trajectories) or run the following commands:

```bash
wget https://github.com/GMPavanLab/dynNP/releases/download/V1.0-trajectories/dh348_3_2_3.hdf5
wget https://github.com/GMPavanLab/dynNP/releases/download/V1.0-trajectories/dh348_3_2_3_fitted.hdf5
wget https://github.com/GMPavanLab/dynNP/releases/download/V1.0-trajectories/ico309.hdf5
wget https://github.com/GMPavanLab/dynNP/releases/download/V1.0-trajectories/ico309_fitted.hdf5
wget https://github.com/GMPavanLab/dynNP/releases/download/V1.0-trajectories/to309_9_4.hdf5
wget https://github.com/GMPavanLab/dynNP/releases/download/V1.0-trajectories/to309_9_4_fitted.hdf5

```

## SOAP calculations

- Prepare the SOAP trajectories with `bash ./run01_SOAP.sh`

## Bottom-up analysis

- Prepare and run the BU analysis with `bash ./run02_BU.sh`

## Top-Down analysis

- Prepare and run the TD analysis with `bash ./run02_TD.sh`

## Visualization

- Prepare the visualizations and create the figures with with `bash ./run03_prepareFigs.sh`

This scripts contains a small workaround that we encountered in working in an virtual environment with both ovito and matplotlib.

### Remarks

The Bottom-up and the Top-Down can be executed in any order or in parallel
