#!/bin/bash
(
    source ./NPenv/bin/activate
    cd figures || exit
    echo creating the cmaps and the legends
    python createCMAPS.py
    deactivate
)


(
    #this is neccessary to workaround a problem between matplolib and PySide
    cd figures || exit
    if [[ ! -d NPfiguresEnv ]]; then
        python3 -m venv NPfiguresEnv
        source ./NPfiguresEnv/bin/activate
	    pip install -U pip
	    pip install -r requirements.txt
    else 
        source ./NPfiguresEnv/bin/activate
    fi
    echo creating the .xyz for visualization
    python createXYZs.py
    python createXYZForFig4.py
    echo creating the images with ovito
    python legendAtomsCreation.py
    python createDefaultImgs-ico.py
    python createDefaultImgs-idealForFig1.py
    python createDefaultImgs.py
    python createico309SOAPexample.py
    python createImgsForFig4.py
    python createImgsForFig3.py
    deactivate

)


(
    source ./NPenv/bin/activate
    cd figures || exit
    echo generating the figures:
    echo -e "\tfigures 1 and 2"
    python figure1and2.py
    for i in 3 4 5; do
        echo -e "\tfigure $i"
        python "figure${i}.py"
    done
    echo -e "\tfigures 6 and 7"
    python figure6and7.py
    echo -e "\tSI figures"
    python figuresSI.py

)
