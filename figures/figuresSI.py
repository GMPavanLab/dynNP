#%%
import figureSupportModule as fsm
import numpy
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt

#%%
def getFullData(np):
    data = fsm.pcaLoaderBottomUp(f"../bottomUp/{np}soap.hdf5")
    fsm.loadClassificationBottomUp(f"../bottomUp/{np}classifications.hdf5", data, np)
    fsm.loadClassificationTopDown(f"../bottomUp/{np}classifications.hdf5", data, np)

    for T in [300, 400, 500]:
        fsm.addPseudoFes(data[T], 150, rangeHisto=[data["xlims"], data["ylims"]])
        fsm.addTmatBU(data[T])
        fsm.addTmatBUNN(data[T])
        fsm.addTmatTD(data[T])
        fsm.addTmatTDNN(data[T])
    fsm.loadClassificationTopDown
    return data

ico309=getFullData("ico309")