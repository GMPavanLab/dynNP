#!/bin/bash

source ../envs/NPenv/bin/activate
source ../telemessage.sh

python createHDF5Args.py ../Gold/*.lammpsdump
myecho "#hdf5e5:  exited with code $?"
for h5 in *hdf5; do
    python SoapifyArgs.py "$h5"
    myecho "#SOAP: ${h5} exited with code $?"
done