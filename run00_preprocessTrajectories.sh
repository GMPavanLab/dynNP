#!/bin/bash

source ./NPenv/bin/activate

echo preprocessing trajectories

python createHDF5Args.py ../simulations/*.lammpsdump
python createHDF5Minimized.py ../simulations/*.minimization.data
