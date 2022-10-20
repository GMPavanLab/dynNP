#!/bin/bash

(
    source ./NPenv/bin/activate
    cd topDown || exit
    if [[ ! -f "References.hdf5" ]]; then
        python TD00_referenceMaker.py
    fi
    
    python TDcomplete.py
)