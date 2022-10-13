#!/bin/bash

source ~/envs/NPenv/bin/activate
source ~/telemessage.sh

python TDComplete.py
myecho "#hdf5: TDComplete  exited with code $?"