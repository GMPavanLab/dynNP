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
def addPseudoFes(tempData, bins=300, rangeHisto=None):
    hist, xedges, yedges = numpy.histogram2d(
        tempData["pca"][:, 0],
        tempData["pca"][:, 1],
        bins=bins,
        range=rangeHisto,
        density=True,
    )
    tempData["pFES"] = -numpy.log(hist.T)
    tempData["pFESLimitsX"] = (xedges[:-1] + xedges[1:]) / 2
    tempData["pFESLimitsY"] = (yedges[:-1] + yedges[1:]) / 2


addPseudoFes(data[300], 150, rangeHisto=[data["xlims"], data["ylims"]])


##%%
# for fig 1
fig = plt.figure(figsize=(10, 5))

grid = fig.add_gridspec(2, 4)

pcaFESGrid = grid[1, 1:3].subgridspec(1, 3, width_ratios=[1, 1, 0.1])
axes = dict(
    soapAx=fig.add_subplot(grid[0, 0]),
    idealAx=fig.add_subplot(grid[0, 1]),
    idealSlicedAx=fig.add_subplot(grid[0, 2]),
    legendAx=fig.add_subplot(grid[0, 3]),
    imgAx=fig.add_subplot(grid[1, 0]),
    pcaAx=fig.add_subplot(pcaFESGrid[0], axes_class=AxesZero),
    pFESAx=fig.add_subplot(pcaFESGrid[1], axes_class=AxesZero),
    cbarFesAx=fig.add_subplot(pcaFESGrid[2]),
    tmatAx=fig.add_subplot(grid[1, 3]),
)

axes["pcaAx"].scatter(data[300]["pca"][:, 0], data[300]["pca"][:, 1], s=0.1)
pfesPlot = axes["pFESAx"].contourf(
    data[300]["pFESLimitsX"],
    data[300]["pFESLimitsY"],
    data[300]["pFES"],
    levels=10,
    color="k",
)
axes["pFESAx"].contour(
    data[300]["pFESLimitsX"],
    data[300]["pFESLimitsY"],
    data[300]["pFES"],
    levels=10,
)
cbar = plt.colorbar(
    pfesPlot, shrink=0.5, aspect=10, orientation="vertical", cax=axes["cbarFesAx"]
)
for ax in [axes["pcaAx"], axes["pFESAx"]]:
    ax.set_xlim(data["xlims"])
    ax.set_ylim(data["ylims"])
    ax.set_xticks([])
    ax.set_yticks([])
    for direction in ["left", "bottom"]:
        ax.axis[direction].set_axisline_style("-|>")

    for direction in ["right", "top"]:
        ax.axis[direction].set_visible(False)
#%%
