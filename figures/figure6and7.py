#%%
from calendar import c
from turtle import position, width
import matplotlib.pyplot as plt
import numpy
import figureSupportModule as fsm
from figureSupportModule import (
    topDownLabels,
    topDownClusters,
    topDownColorMap,
    getCompactedAnnotationsForTmat_percent,
    decorateTmatWithLegend,
)
import seaborn
from matplotlib.image import imread
import h5py, re
from SOAPify import SOAPclassification
from chorddiagram import ChordDiagram

reT = re.compile("T_([0-9]*)")


def getT(s):
    match = reT.search(s)
    if match:
        return int(match.group(1))
    else:
        return "Ideal"


def dataGetter(classificationFile: str, data: dict):
    with h5py.File(classificationFile, "r") as distFile:
        ClassG = distFile["Classifications/icotodh"]
        for k in ClassG:
            if NPname in k:
                T = getT(k)
                data[T] = dict()
                classification = ClassG[k][:]
                clusterized = topDownClusters[classification]
                data[T]["Class"] = SOAPclassification([], clusterized, topDownLabels)


#%% Loading Data

data = {}
for NPname in ["dh348_3_2_3", "to309_9_4"]:
    data[NPname] = dict()
    classificationFile = f"../topDown/{NPname}TopBottom.hdf5"
    dataGetter(classificationFile, data[NPname])
    dataGetter("../minimized.hdf5", data[NPname])


for NP in data:
    for T in data[NP]:
        if T == "Ideal":
            continue
        fsm.addTmatTD(data[NP][T])
        fsm.addTmatNNTD(data[NP][T])


#%%
def AddTmatsAndChord(axesdict, data, T, zoom=0.01):
    reorder = list(range(10))  # [0, 1, 2, 5, 3, 4, 6, 7, 9, 8]
    mask = data["tmat"] == 0
    seaborn.heatmap(
        data["tmat"],
        linewidths=0.1,
        ax=axesdict[f"tmat{T}"],
        fmt="s",
        annot=None,
        mask=mask,
        square=True,
        cmap="rocket_r",
        vmax=1,
        vmin=0,
        cbar=False,
        xticklabels=False,
        yticklabels=False,
    )
    decorateTmatWithLegend("topDown", reorder, axesdict[f"tmat{T}"], zoom=zoom)
    ChordDiagram(
        data["tmatNN"], colors=topDownColorMap, ax=axesdict[f"chord{T}"], onlyFlux=True
    )


def HistoMaker(ax, data, reshuffler=None):
    nHisto = len(topDownLabels)
    t = data["Ideal"]["Class"]
    order = ["Ideal", 300, 400, 500]
    countMean = {T: numpy.zeros((nHisto), dtype=float) for T in data}
    countDev = {T: numpy.zeros((nHisto), dtype=float) for T in data}
    pos = {T: numpy.zeros((nHisto), dtype=float) for T in order}

    positions = range(nHisto)
    width = 0.1
    space = 0.1
    D = 4 * width + 3 * space
    for c in range(nHisto):
        countMean["Ideal"][c] = numpy.count_nonzero(t.references[0] == c)
        countDev["Ideal"] = None
        dev = -D / 2
        for T in order:
            pos[T][c] = positions[c] + dev
            dev += width + space
            if T == "Ideal":
                continue
            countC = numpy.count_nonzero(data[T]["Class"].references == c, axis=-1)
            countMean[T][c] = numpy.mean(countC)
            countDev[T][c] = numpy.std(countC)
    ax.set_xticks(range(nHisto), topDownLabels)

    for T in data:
        ax.bar(pos[T], countMean[T], yerr=countDev[T], width=width, align="edge")


figsize = numpy.array([4, 3]) * 3
fig, axes = fsm.makeLayout6and7(figsize, dpi=300)


for T in [300, 400, 500]:

    AddTmatsAndChord(axes, data["dh348_3_2_3"][T], T)
    # AddTmats(axes, data["dh348_3_2_3"][T], T)

HistoMaker(axes["Histo"], data["dh348_3_2_3"])
# todo: histo
# %%


#%%
