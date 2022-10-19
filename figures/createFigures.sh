#!/bin/bash

source ./NPenv/bin/activate
#CMAPS and legend are pregenerated

python createXYZForFig4.py
python createXYZ.py
#fell free to use ovitos for these
python createDefaultImgs-ico.py
python createDefaultImgs-idealForFig1.py
python createDefaultImgs.py
python imgsNPforFig3.py
python imgsNPforFig4.py
python createico309SOAPexample.py
#go back to plain python 
python figure1and2.py
python figure3.py
python figure4.py
python figure5.py
python figure6and7.py
python figuresSI.py

