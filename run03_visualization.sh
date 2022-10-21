#!/bin/bash

(
    source ./NPenv/bin/activate
    cd figures || exit
    echo creating the .xyz for visualization
    #python createXYZs.py
    python createXYZForFig4.py
    echo creating the cmaps and the legends
    #python createCMAPS.py
    #python legendAtomsCreation.py
    echo creating the images
    #python createDefaultImgs-ico.py
    #python createDefaultImgs-idealForFig1.py
    #python createDefaultImgs.py
    #python createico309SOAPexample.py
    python createImgsForFig4.py
    python createImgsForFig3.py
    echo generating the figures

)
