#%%
# from matplotlib.gridspec import
from turtle import color
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import AxesZero
import h5py
import re, numpy


getT = re.compile("T_([0-9]*)")


#%%
# ../bottomUp/ico309soap.hdf5
#


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
# for fig 1
fig = plt.figure(figsize=(10, 10))

grid = fig.add_gridspec(4, 4)

axes = dict(
    soapAx=fig.add_subplot(grid[0, 0]),
    idealAx=fig.add_subplot(grid[0, 1]),
    idealSlicedAx=fig.add_subplot(grid[0, 2]),
    legendAx=fig.add_subplot(grid[0, 3]),
)

axes.update(createSimulationFigs(grid[1, :].subgridspec(1, 4), fig, name="300"))
axes.update(createSimulationFigs(grid[2, :].subgridspec(1, 4), fig, name="400"))
axes.update(createSimulationFigs(grid[3, :].subgridspec(1, 4), fig, name="500"))

for T in [300, 400, 500]:

    axes[f"pca{T}Ax"].scatter(
        data[T]["pca"][:, 0], data[T]["pca"][:, 1], s=0.1, c=data[T]["labelsNN"], vmax=7
    )
    print(T, set(data[T]["labelsNN"]))
    pfesPlot = axes[f"pFES{T}Ax"].contourf(
        data[T]["pFESLimitsX"],
        data[T]["pFESLimitsY"],
        data[T]["pFES"],
        levels=10,
        color="k",
        linewidths=1,
        zorder=2,
    )
    axes[f"pFES{T}Ax"].contour(
        data[T]["pFESLimitsX"],
        data[T]["pFESLimitsY"],
        data[T]["pFES"],
        levels=10,
        zorder=1,
    )
    cbar = plt.colorbar(
        pfesPlot,
        shrink=0.5,
        aspect=10,
        orientation="vertical",
        cax=axes[f"cbarFes{T}Ax"],
    )
    for ax in [axes[f"pca{T}Ax"], axes[f"pFES{T}Ax"]]:
        ax.set_xlim(data["xlims"])
        ax.set_ylim(data["ylims"])
        ax.set_xticks([])
        ax.set_yticks([])
        for direction in ["left", "bottom"]:
            ax.axis[direction].set_axisline_style("-|>")

        for direction in ["right", "top"]:
            ax.axis[direction].set_visible(False)
#%%
