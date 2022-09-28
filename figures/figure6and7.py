#%%
from turtle import width
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.image import imread
import figureSupportModule as fsm

from figureSupportModule import (
    topDownLabels,
    topDownColorMap,
    decorateTmatWithLegend,
    __titleDict,
    alph,
)

import numpy, seaborn
from chorddiagram import ChordDiagram


#%% Loading Data

data = {}
for NPname in ["dh348_3_2_3", "to309_9_4"]:
    data[NPname] = dict()
    classificationFile = f"../topDown/{NPname}TopBottom.hdf5"
    fsm.dataLoaderTopDown(classificationFile, data[NPname], NPname)
    fsm.dataLoaderTopDown("../minimized.hdf5", data[NPname], NPname)


for NP in data:
    for T in data[NP]:
        if T == "Ideal":
            continue
        fsm.addTmatTD(data[NP][T])
        fsm.addTmatNNTD(data[NP][T])


#%%


def makeLayout6and7(figsize, **figkwargs):
    axes = dict()
    fig = plt.figure(figsize=figsize, **figkwargs)
    mainGrid = fig.add_gridspec(nrows=3, ncols=2, width_ratios=[3, 1], wspace=0.1)
    npGrid = mainGrid[0, 0].subgridspec(1, 4)
    tmatGrid = mainGrid[2, 0].subgridspec(1, 4, width_ratios=[1, 1, 1, 0.05])
    chordGrid = mainGrid[:, 1].subgridspec(3, 1)
    axes[f"npIdeal"] = fig.add_subplot(npGrid[0])
    for i, T in enumerate([300, 400, 500]):
        axes[f"np{T}"] = fig.add_subplot(npGrid[i + 1])
        axes[f"tmat{T}"] = fig.add_subplot(tmatGrid[i])
        axes[f"chord{T}"] = fig.add_subplot(chordGrid[i])
    axes[f"tmatCMAP"] = fig.add_subplot(tmatGrid[3])
    axes[f"nps"] = fig.add_subplot(npGrid[:])
    axes[f"tmats"] = fig.add_subplot(tmatGrid[:])
    axes[f"chords"] = fig.add_subplot(chordGrid[:])
    axes["Histo"] = fig.add_subplot(mainGrid[1, 0])
    for i, ax in enumerate(
        [
            axes["nps"],
            axes["Histo"],
            axes["tmats"],
            axes["chords"],
        ]
    ):
        ax.set_title(alph[i], **__titleDict)
    for ax in [axes["nps"], axes["tmats"], axes["chords"]]:
        ax.axis("off")
    return fig, axes


def AddTmatsAndChord5_6_7(axesdict, data, T, zoom=0.01, cbarAx=None, **tmatOptions):
    reorder = list(range(10))  # [0, 1, 2, 5, 3, 4, 6, 7, 9, 8]
    mask = data["tmat"] == 0
    seaborn.heatmap(
        data["tmat"],
        ax=axesdict[f"tmat{T}"],
        fmt="s",
        annot=None,
        mask=mask,
        square=True,
        cmap="rocket_r",
        vmax=1,
        vmin=0,
        cbar=cbarAx is not None,
        cbar_ax=cbarAx,
        xticklabels=False,
        yticklabels=False,
        **tmatOptions,
    )
    decorateTmatWithLegend("topDown", reorder, axesdict[f"tmat{T}"], zoom=zoom)
    ChordDiagram(
        data["tmatNN"], colors=topDownColorMap, ax=axesdict[f"chord{T}"], onlyFlux=True
    )
    for ax in [axesdict[f"chord{T}"], axesdict[f"tmat{T}"]]:
        ax.set_title(f"{T}\u2009K")


def HistoMaker(
    ax: plt.Axes,
    data: dict,
    width: float = 0.15,
    space: float = 0.05,
    arrowLenght: float = 0.25,
    positions=None,
):

    nHisto = len(topDownLabels)
    if positions is None:
        positions = range(nHisto)
    t = data["Ideal"]["Class"]
    order = ["Ideal", 300, 400, 500]
    countMean = {T: numpy.zeros((nHisto), dtype=float) for T in data}
    countDev = {T: numpy.zeros((nHisto), dtype=float) for T in data}
    pos = {T: numpy.zeros((nHisto), dtype=float) for T in order}

    barsSpace = 4 * width + 3 * space
    for c in range(nHisto):
        countMean["Ideal"][c] = numpy.count_nonzero(t.references[0] == c)
        countDev["Ideal"] = None
        dev = -barsSpace / 2
        for T in order:
            pos[T][c] = positions[c] + dev
            dev += width + space
            if T == "Ideal":
                continue
            countC = numpy.count_nonzero(data[T]["Class"].references == c, axis=-1)
            countMean[T][c] = numpy.mean(countC)
            countDev[T][c] = numpy.std(countC)
    ax.set_xticks(
        range(nHisto), [topDownLabels[positions.index(k)] for k in range(nHisto)]
    )
    styles = {
        "Ideal": dict(edgecolor="k", alpha=0.5),
        300: dict(edgecolor="w"),
        400: dict(hatch="///", edgecolor="w"),
        500: dict(hatch="\\\\\\", edgecolor="w"),
    }
    for T in data:
        ax.bar(
            pos[T],
            countMean[T],
            yerr=countDev[T],
            width=width,
            align="edge",
            color=topDownColorMap,
            **styles[T],
        )
    _, axylim = ax.get_ylim()
    ax.set_ylabel("Mean Number of Atoms")
    for c in range(nHisto):
        if countMean["Ideal"][c] == 0:
            arrowXPos = pos["Ideal"][c] + width / 2
            ax.annotate(
                "",
                xy=(arrowXPos, 0),
                xycoords="data",
                xytext=(arrowXPos, axylim * arrowLenght),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
            )
    legend_elements = []
    for k in styles:
        title = f"{k}\u2009K" if k != "Ideal" else "Ideal"
        legend_elements.append(Patch(label=title, facecolor="#aaa", **styles[k]))

    ax.legend(handles=legend_elements)


for NP in ["dh348_3_2_3", "to309_9_4"]:
    figsize = numpy.array([3.8, 3]) * 4
    # fig, axes = fsm.makeLayout6and7(figsize, dpi=300)
    fig, axes = makeLayout6and7(figsize, dpi=300)
    for T in [300, 400, 500]:
        AddTmatsAndChord5_6_7(
            axes,
            data[NP][T],
            T,
            cbarAx=None if T != 500 else axes["tmatCMAP"],
            linewidth=0.1,
            cbar_kws={} if T != 500 else {"label": "Probability"},
        )

    # todo: add the arrows
    HistoMaker(axes["Histo"], data[NP], positions=[0, 1, 2, 9, 8, 3, 7, 5, 6, 4])

# %%


#%%
