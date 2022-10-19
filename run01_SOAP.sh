#!/bin/bash

source ./NPenv/bin/activate

python createHDF5Args.py ../simulations/*.lammpsdump
echo "#hdf5e5:  exited with code $?"
for h5 in *.hdf5; do
    if [[ "$h5"  == *fitted* || "$h5"  == *soap* || "$h5"  ==  *classifications* || "$h5"  ==  *pca*  || "$h5"  == *TopBottom* ]]; then
        continue
    fi
    python SoapifyArgs.py "$h5"
    echo "#SOAP: ${h5} exited with code $?"
done