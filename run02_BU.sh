#!/bin/bash

(
    source ./NPenv/bin/activate
    cd bottomUp || exit
    echo applying the pca
    python BUComplete.py pca
    #this may be very heavy on your RAM
    echo classifying
    python BUComplete.py classify
)