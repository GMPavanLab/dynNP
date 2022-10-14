#!/bin/bash

source ~/envs/NPenv/bin/activate
source ~/telemessage.sh

python TDcomplete.py
myecho "#hdf5: TDComplete  exited with code $?"