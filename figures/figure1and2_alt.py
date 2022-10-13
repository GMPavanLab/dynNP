#%%
import figureSupportModule as fsm
import matplotlib.pyplot as plt
import numpy
from mpl_toolkits.axisartist.axislines import AxesZero
from matplotlib.image import imread

#%%
def getData(np):
    data = fsm.dataLoaderBottomUp(f"../bottomUp/{np}soap.hdf5")
    fsm.loadClassificationBottomUp(data, f"../bottomUp/{np}classifications.hdf5")
    nat = data["nat"]
    fsm.addPseudoFes(data[300], 150, rangeHisto=[data["xlims"], data["ylims"]])
    fsm.addPseudoFes(data[400], 150, rangeHisto=[data["xlims"], data["ylims"]])
    fsm.addPseudoFes(data[500], 150, rangeHisto=[data["xlims"], data["ylims"]])
    fsm.addTmatBU(data[300], nat)
    fsm.addTmatBU(data[400], nat)
    fsm.addTmatBU(data[500], nat)
    return data


def createSimulationFigsNoIMG(grid, fig, name=""):
    toret = dict()
    pcaFESGrid = grid[0:2].subgridspec(1, 3, width_ratios=[1, 1, 0.1])
    toret[f"pca{name}Ax"] = fig.add_subplot(pcaFESGrid[0], axes_class=AxesZero)
    toret[f"pFES{name}Ax"] = fig.add_subplot(pcaFESGrid[1], axes_class=AxesZero)
    toret[f"cbarFes{name}Ax"] = fig.add_subplot(pcaFESGrid[2])
    toret[f"tmat{name}Ax"] = fig.add_subplot(grid[2])
    return toret


def alternativeLayout(figsize, **figkwargs):
    fig = plt.figure(figsize=figsize, **figkwargs)
    mainGrid = fig.add_gridspec(3, 4)

    axes = dict()
    axes.update(fsm.createS(mainGrid[0, :].subgridspec(1, 4), fig, name="300"))
    axes.update(
        fsm.createSimulationFigs(mainGrid[1, :].subgridspec(1, 4), fig, name="400")
    )
    axes.update(
        fsm.createSimulationFigs(mainGrid[2, :].subgridspec(1, 4), fig, name="500")
    )
    return fig, axes


#%%
data = dict()
for np in ["ico309", "dh348_3_2_3", "to309_9_4"]:
    data[np] = getData(np)
#%%

figsize = numpy.array([2, 1]) * 8
for np in ["ico309", "dh348_3_2_3", "to309_9_4"]:
    fig1, axesFig1 = alternativeLayout(figsize=figsize, dpi=300)
    for T in [300, 400, 500]:
        fsm.plotTemperatureData(
            axesFig1, T, data[np][T], data[np]["xlims"], data[np]["ylims"], zoom=0.02
        )
        axesFig1[f"img{T}Ax"].imshow(imread(f"{np}_{T}-bottomUP.png"))
        axesFig1[f"img{T}Ax"].axis("off")
    fig1.savefig(f"{np}_analysisBottomUp.png")

#%%
figsize = (5, 3)
fig = plt.figure(figsize=figsize)
mainGrid = fig.add_gridspec(1, 1)
ax = fig.add_subplot(mainGrid[:])
for i in range(8):
    d = numpy.count_nonzero(
        data["ico309"][300]["labelsNN"].reshape(1000, -1) == i, axis=-1, keepdims=True
    )
    ax.plot(range(1000), d, c=fsm.bottomUpColorMap[i])
ax.set_ylabel("NAT per cluster")
ax.set_xticks(list(range(0, 1001, 100)), [i / 10 for i in range(11)])
ax.set_xlabel("MD time [$\mu$s]")
fig.savefig(f"ico309_500Equilibrium.png", bbox_inches="tight", pad_inches=0, dpi=300)
# %%
