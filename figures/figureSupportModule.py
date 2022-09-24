#%%
# from matplotlib.gridspec import
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.axisartist.axislines import AxesZero
import h5py
import re, numpy
import colorsys
from SOAPify import (
    transitionMatrixFromSOAPClassificationNormalized as tmatMaker,
    SOAPclassification,
)
import seaborn

getT = re.compile("T_([0-9]*)")


#%%
# ../bottomUp/ico309soap.hdf5
#
bottomUpcolorMap = numpy.array(
    [
        to_rgb("#00b127"),  # Faces
        to_rgb("#e00081"),  # Concave
        to_rgb("#0086ba"),  # 5foldedSS
        to_rgb("#003ac6"),  # Ico
        to_rgb("#450055"),  # Bulk
        to_rgb("#3800a8"),  # SubSurf
        to_rgb("#bdff0e"),  # Edges
        to_rgb("#ffe823"),  # Vertexes
    ]
)
bottomUpLabels = [
    "Faces",
    "Concave",
    "5foldedSS",
    "Ico",
    "Bulk",
    "SubSurf",
    "Edges",
    "Vertexes",
]
bottomReordering = [7, 6, 0, 1, 2, 5, 4, 3]
bottomReordering_r = bottomReordering[::-1]


def getF(proposed: float, concurrentArray, F):
    avversary = F(concurrentArray)
    return F([proposed, avversary])


def getMin(proposed: float, concurrentArray):
    return getF(proposed, concurrentArray, numpy.min)


def getMax(proposed: float, concurrentArray):
    return getF(proposed, concurrentArray, numpy.max)


def dataLoaderBottomUp(filename):
    dataContainer = dict()
    dataContainer["xlims"] = [numpy.finfo(float).max, numpy.finfo(float).min]
    dataContainer["ylims"] = [numpy.finfo(float).max, numpy.finfo(float).min]
    with h5py.File(filename, "r") as f:
        pcas = f["/PCAs/ico309-SV_18631-SL_31922-T_300"]
        for k in pcas:
            T = int(getT.search(k).group(1))
            dataContainer[T] = dict(pca=pcas[k][:, :, :2].reshape(-1, 2))
            dataContainer["xlims"][0] = getMin(
                dataContainer["xlims"][0], dataContainer[T]["pca"][:, 0]
            )
            dataContainer["xlims"][1] = getMax(
                dataContainer["xlims"][1], dataContainer[T]["pca"][:, 0]
            )
            dataContainer["ylims"][0] = getMin(
                dataContainer["ylims"][0], dataContainer[T]["pca"][:, 1]
            )
            dataContainer["ylims"][1] = getMax(
                dataContainer["ylims"][1], dataContainer[T]["pca"][:, 1]
            )

    return dataContainer


#%%

data = dataLoaderBottomUp("../bottomUp/ico309soap.hdf5")

#%%
def loadClassification(
    dataContainer, filename="../bottomUp/ico309classifications.hdf5"
):
    with h5py.File(filename, "r") as f:
        classes = f["/Classifications/ico309-SV_18631-SL_31922-T_300"]
        for k in classes:
            T = int(getT.search(k).group(1))
            dataContainer[T]["labelsNN"] = classes[k]["labelsNN"][:].reshape(-1)


loadClassification(data)
#%%
def addPseudoFes(tempData, bins=300, rangeHisto=None):
    hist, xedges, yedges = numpy.histogram2d(
        tempData["pca"][:, 0],
        tempData["pca"][:, 1],
        bins=bins,
        range=rangeHisto,
        density=True,
    )
    tempData["pFES"] = -numpy.log(hist.T)
    tempData["pFES"] -= numpy.min(tempData["pFES"])
    tempData["pFESLimitsX"] = (xedges[:-1] + xedges[1:]) / 2
    tempData["pFESLimitsY"] = (yedges[:-1] + yedges[1:]) / 2


addPseudoFes(data[300], 150, rangeHisto=[data["xlims"], data["ylims"]])
addPseudoFes(data[400], 150, rangeHisto=[data["xlims"], data["ylims"]])
addPseudoFes(data[500], 150, rangeHisto=[data["xlims"], data["ylims"]])


def createSimulationFigs(grid, fig, name=""):
    toret = dict()
    pcaFESGrid = grid[1:3].subgridspec(1, 3, width_ratios=[1, 1, 0.1])
    toret[f"img{name}Ax"] = fig.add_subplot(grid[0])
    toret[f"pca{name}Ax"] = fig.add_subplot(pcaFESGrid[0], axes_class=AxesZero)
    toret[f"pFES{name}Ax"] = fig.add_subplot(pcaFESGrid[1], axes_class=AxesZero)
    toret[f"cbarFes{name}Ax"] = fig.add_subplot(pcaFESGrid[2])
    toret[f"tmat{name}Ax"] = fig.add_subplot(grid[3])
    return toret


#%%


def getCompactedAnnotationsForTmat_percent(tmat) -> list:
    """
    Returns a list of compacted annotations for a given tmat.
    """
    annot = list(numpy.empty(tmat.shape, dtype=str))
    # annot=numpy.chararray(tmat.shape, itemsize=5)
    for row in range(tmat.shape[0]):
        annot[row] = list(annot[row])
        for col in range(tmat.shape[1]):
            if tmat[row, col] < 0.01:
                annot[row][col] = f"<1"
            elif tmat[row, col] > 0.99:
                annot[row][col] = f">99"
            else:
                annot[row][col] = f"{100*tmat[row,col]:.0f}"
    return annot


def addTmat(tempData):
    tempData["tmat"] = tmatMaker(
        SOAPclassification([], tempData["labelsNN"].reshape(-1, 309), bottomUpLabels)
    )[bottomReordering_r][:, bottomReordering_r]


addTmat(data[300])
addTmat(data[400])
addTmat(data[500])

#%%
def plotTemperatureData(axesdict, T, data, xlims, ylims):
    # option for the countour lines
    countourOptions = dict(
        levels=10,
        colors="k",
        linewidths=0.1,
        zorder=2,
    )
    # the pca points
    axesdict[f"pca{T}Ax"].scatter(
        data["pca"][:, 0],
        data["pca"][:, 1],
        s=0.1,
        c=bottomUpcolorMap[data["labelsNN"]],
        alpha=0.5,
    )
    axesdict[f"pca{T}Ax"].contour(
        data["pFESLimitsX"],
        data["pFESLimitsY"],
        data["pFES"],
        **countourOptions,
    )

    # pseudoFES representation
    pfesPlot = axesdict[f"pFES{T}Ax"].contourf(
        data["pFESLimitsX"],
        data["pFESLimitsY"],
        data["pFES"],
        levels=10,
        cmap="coolwarm_r",
        zorder=1,
    )

    axesdict[f"pFES{T}Ax"].contour(
        data["pFESLimitsX"],
        data["pFESLimitsY"],
        data["pFES"],
        **countourOptions,
    )

    cbar = plt.colorbar(
        pfesPlot,
        shrink=0.5,
        aspect=10,
        orientation="vertical",
        cax=axesdict[f"cbarFes{T}Ax"],
    )
    mask = data["tmat"] == 0
    annots = getCompactedAnnotationsForTmat_percent(data["tmat"])
    seaborn.heatmap(
        data["tmat"],
        linewidths=0.1,
        ax=axesdict[f"tmat{T}Ax"],
        fmt="s",
        annot=annots,
        mask=mask,
        square=True,
        cmap="rocket_r",
        vmax=1,
        vmin=0,
        cbar=False,
    )
    for ax in [axesdict[f"pca{T}Ax"], axesdict[f"pFES{T}Ax"]]:
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)
        ax.set_xticks([])
        ax.set_yticks([])
        for direction in ["left", "bottom"]:
            ax.axis[direction].set_axisline_style("-|>")

        for direction in ["right", "top"]:
            ax.axis[direction].set_visible(False)


##%%
# for fig 1
fig1 = plt.figure(figsize=(10, 5), dpi=300)
fig2 = plt.figure(figsize=(10, 5), dpi=300)


grid1 = fig1.add_gridspec(2, 4)
grid2 = fig2.add_gridspec(2, 4)

axesFig1 = dict(
    soapAx=fig1.add_subplot(grid1[0, 0]),
    idealAx=fig1.add_subplot(grid1[0, 1]),
    idealSlicedAx=fig1.add_subplot(grid1[0, 2]),
    legendAx=fig1.add_subplot(grid1[0, 3]),
)
axesFig2 = dict()
axesFig1.update(createSimulationFigs(grid1[1, :].subgridspec(1, 4), fig1, name="300"))
axesFig2.update(createSimulationFigs(grid2[0, :].subgridspec(1, 4), fig2, name="400"))
axesFig2.update(createSimulationFigs(grid2[1, :].subgridspec(1, 4), fig2, name="500"))

plotTemperatureData(axesFig1, 300, data[300], data["xlims"], data["ylims"])
for T in [400, 500]:
    plotTemperatureData(axesFig2, T, data[T], data["xlims"], data["ylims"])

#%%
bottomUpcolorMap = numpy.array(
    [
        to_rgb("#00b127"),  # plain
        to_rgb("#e00081"),  # concave
        to_rgb("#0086ba"),  # 5foldedSS
        to_rgb("#003ac6"),  # ico
        to_rgb("#450055"),  # bulk
        to_rgb("#3800a8"),  # SS
        to_rgb("#bdff0e"),  # edge
        to_rgb("#ffe823"),  # vertex
    ]
)
fig, ax = plt.subplots(2, 4)
ax = ax.flatten()

for i in range(8):
    address = data[T]["labelsNN"] == i
    ax[i].scatter(
        data[T]["pca"][address, 0],
        data[T]["pca"][address, 1],
        s=0.1,
        color=bottomUpcolorMap[i],
    )
    notaddress = data[T]["labelsNN"] != i
    ax[i].scatter(
        data[T]["pca"][notaddress, 0],
        data[T]["pca"][notaddress, 1],
        s=0.1,
        c="gray",
    )
    ax[i].set_title(i)
    ax[i].axis("off")
    ax[i].set_xlim(data["xlims"])
    ax[i].set_ylim(data["ylims"])
