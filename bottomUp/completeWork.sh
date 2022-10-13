#!/bin/bash

source ~/envs/NPenv/bin/activate
source ~/telemessage.sh

python BUComplete.py
myecho "#hdf5: BUComplete  exited with code $?"
