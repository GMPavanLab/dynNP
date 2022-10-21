#%%
import figureSupportModule as fsm
import numpy
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import seaborn

#%%
Temps = [300, 400, 500]


def getFiguresData(np):
    data = fsm.pcaLoaderBottomUp(f"../{np}pca.hdf5", fsm.trajectorySlice)
    fsm.loadClassificationBottomUp(
        f"../{np}classifications.hdf5", data, np, fsm.trajectorySlice
    )
    fsm.loadClassificationTopDown(
        f"../{np}TopBottom.hdf5", data, np, fsm.trajectorySlice
    )

    for T in Temps:
        fsm.addPseudoFes(data[T], 150, rangeHisto=[data["xlims"], data["ylims"]])
        fsm.addTmatBU(data[T])
        fsm.addTmatBUNN(data[T])
        fsm.addTmatTD(data[T])
        fsm.addTmatTDNN(data[T])
    fsm.loadClassificationTopDown
    return data


def getFullDataStrided(np, window):
    data = fsm.pcaLoaderBottomUp(f"../{np}pca.hdf5", TimeWindow=window)
    fsm.loadClassificationBottomUp(
        f"../{np}classifications.hdf5", data, np, TimeWindow=window
    )
    fsm.loadClassificationTopDown(f"../{np}TopBottom.hdf5", data, np, TimeWindow=window)

    for T in Temps:
        fsm.addPseudoFes(data[T], 150, rangeHisto=[data["xlims"], data["ylims"]])
        fsm.addTmatBU(data[T])
        fsm.addTmatBUNN(data[T])
        fsm.addTmatTD(data[T])
        fsm.addTmatTDNN(data[T])
    fsm.loadClassificationTopDown
    return data


def makeTmats(
    dataDict,
    tmatAddr,
    legendNames,
    reordering,
    figsize=numpy.array([3, 1]) * 10,
    zoom=0.02,
):
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=figsize, dpi=300)
    for i, T in enumerate(Temps):
        # axes[i].set_aspect(1)
        axes[i].set_title(f"{T} K")
        # continue
        tmat = dataDict[T][tmatAddr]
        mask = tmat == 0
        annots = True
        seaborn.heatmap(
            tmat,
            linewidths=1,
            ax=axes[i],
            annot=annots,
            mask=mask,
            square=True,
            cmap="rocket_r",
            cbar=False,
            xticklabels=False,
            yticklabels=False,
            annot_kws=dict(
                weight="bold",
            ),
        )

        fsm.decorateTmatWithLegend(legendNames, reordering, axes[i], zoom=zoom)
    return fig


def calculateTransitions(tmat, time):
    n = tmat.shape[0]
    rates = numpy.zeros_like(tmat)
    for i in range(n):
        for j in range(n):
            if i != j and tmat[i, j] != 0:
                rates[i, j] = 1.0 / (tmat[i, j] / time)
    return rates


def transitionsFigures(
    dataDict1,
    dataDict2,
    tmatAddr,
    legendNames,
    reordering,
    figsize=numpy.array([2, 3]) * 10,
    zoom=0.02,
):
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=figsize, dpi=300)
    for j, myDict in enumerate([dataDict1, dataDict2]):
        for i, T in enumerate(Temps):
            ax = axes[i, j]
            tmat = calculateTransitions(myDict[T][tmatAddr], 0.2)
            mask = tmat == 0
            annots = True  # fsm.getCompactedAnnotationsForTmat_percent(tmat)
            seaborn.heatmap(
                tmat,
                linewidths=0.1,
                ax=ax,
                annot=annots,
                mask=mask,
                square=True,
                cmap="rocket_r",
                cbar=False,
                xticklabels=False,
                yticklabels=False,
                annot_kws=dict(
                    weight="bold",
                ),
            )
            fsm.decorateTmatWithLegend(legendNames, reordering, ax, zoom=zoom)
    return fig


def plotEquilibrium(dataDict: dict, T: int, Class: str, colorMap: list, ax=None):
    axis = plt if ax is None else ax
    for i in range(len(colorMap)):
        t = numpy.count_nonzero(dataDict[T][Class].references == i, axis=-1)
        axis.plot(range(t.shape[0]), t, color=colorMap[i])


def plotEquilibriumWithMean(
    dataDict: dict, T: int, Class: str, colorMap: list, ax=None
):
    from pandas import DataFrame

    axis = plt if ax is None else ax
    for i in range(len(colorMap)):
        t = numpy.count_nonzero(dataDict[T][Class].references == i, axis=-1)
        df = DataFrame(t)
        axis.plot(range(t.shape[0]), t, color=colorMap[i], alpha=0.5)
        axis.plot(range(t.shape[0]), df.rolling(10).mean(), color=colorMap[i])


def stackEquilibrium(
    dataDict: dict, T: int, Class: str, colorMap: list, ax=None, reorder=None
):
    axis = plt if ax is None else ax
    t = numpy.zeros((len(colorMap), dataDict[T][Class].references.shape[0]), dtype=int)
    for i in range(len(colorMap)):
        t[i] = numpy.count_nonzero(dataDict[T][Class].references == i, axis=-1)
    colors = colorMap
    if reorder:
        t[:] = t[reorder]
        colors = colorMap[reorder]
    axis.stackplot(range(t.shape[1]), t, colors=colors)


def plotEquilibriumSingle(
    dataDict: dict,
    T: int,
    classNum: int,
    Class: str,
    color: list,
    label: str = None,
    ax=None,
):
    axis = plt if ax is None else ax
    t = numpy.count_nonzero(dataDict[T][Class].references == classNum, axis=-1)
    axis.plot(range(t.shape[0]), t, color=color, label=label)


def figureEquilibrium(
    dataDict: dict,
    Class: str,
    cmap: list,
    figkwargs: dict,
    labels: list,
    reorder: list = None,
    vline: float = None,
):
    tdNum = len(cmap)
    fig, axes = plt.subplots(
        nrows=tdNum, ncols=3, sharex="col", sharey="row", **figkwargs
    )
    reordering = reorder if reorder else range(tdNum)

    for i, T in enumerate(Temps):
        for j in range(tdNum):
            jj = reordering[j]
            plotEquilibriumSingle(
                dataDict, T, j, Class, cmap[j], labels[jj], axes[jj, i]
            )
            axes[jj, i].legend(bbox_to_anchor=(1, 1), loc="right", framealpha=1)
            if i == 0:
                axes[jj, i].yaxis.set_major_locator(MaxNLocator(nbins=5, integer=True))
                axes[jj, i].set_ylabel("Number of atoms")
            if jj == (tdNum - 1):
                t = [i for i in range(0, 2001, 500)]
                axes[jj, i].set_xticks(t, [i / 1000 for i in t])
                axes[jj, i].set_xlabel("md time [$\mu$s]")
            if jj == 0:
                axes[jj, i].set_title(f"{T} K")
            if vline:
                axes[jj, i].axvline(vline, color="k", linestyle="--")
    fig.align_ylabels(axes[:, 0])
    return fig


#%%
if __name__ == "__main__":

    ico309_1ns = getFiguresData("ico309")
    to309_9_4_1nsFull = getFullDataStrided("to309_9_4", slice(None, None, 10))
    dh348_3_2_3_1nsFull = getFullDataStrided("dh348_3_2_3", slice(None, None, 10))
    ico309_1nsFull = getFullDataStrided("ico309", slice(None, None, 10))
    figsize = numpy.array([99, 297]) * 0.1
    for i, (tmatAddr, legendNames, npTitle, reordering) in enumerate(
        [
            ("tmatBUNN", "bottomUp", "Bottom-Up", fsm.bottomReordering_r),
            ("tmatTDNN", "topDown", "Top-Down", range(10)),
        ]
    ):
        fig = makeTmats(
            ico309_1ns, tmatAddr, legendNames, reordering, figsize=figsize, zoom=0.04
        )

        fig.suptitle("$Ih_{309}$ " + npTitle, fontsize=16, y=1)
        fig.set_layout_engine("tight")
        fig.savefig(f"SIfigure{i+1}.png", bbox_inches="tight", pad_inches=0, dpi=300)

    figsize = numpy.array([210, 297]) * 0.05
    ico309_1nsFull = getFullDataStrided("ico309", slice(None, None, 10))
    fig = figureEquilibrium(
        ico309_1nsFull,
        "ClassBU",
        fsm.bottomUpColorMap,
        dict(figsize=figsize, dpi=300, tight_layout=True),
        fsm.bottomUpLabels_ordered,
        [
            fsm.bottomReordering_r.index(i)
            for i in range(len(fsm.bottomUpLabels_ordered))
        ],
        vline=1000,
    )

    fig.suptitle("$Ih_{309}$ Bottom-Up", fontsize=16)

    fig.savefig(f"SIfigure{3}.png", bbox_inches="tight", pad_inches=0, dpi=300)

    for figID, (dataDict, np) in enumerate(
        [
            (ico309_1nsFull, "$Ih_{309}$"),
            (to309_9_4_1nsFull, "$To_{309}$"),
            (dh348_3_2_3_1nsFull, "$Dh_{309}$"),
        ],
        4,
    ):
        fig = figureEquilibrium(
            dataDict,
            "ClassTD",
            fsm.topDownColorMap,
            dict(figsize=figsize, dpi=300, tight_layout=True),
            fsm.topDownLabels,
            vline=1000,
        )
        fig.suptitle(f"{np} Top-Down", fontsize=16)
        fig.savefig(f"SIfigure{figID}.png", bbox_inches="tight", pad_inches=0, dpi=300)

    # %%

    to309_9_4_1ns = getFiguresData("to309_9_4")
    dh348_3_2_3_1ns = getFiguresData("dh348_3_2_3")
    #%%
    figsize = numpy.array([99, 297]) * 0.1
    for i, data, tmatAddr, legendNames, npTitle, reordering in [
        ("To", to309_9_4_1ns, "tmatTDNN", "topDown", "Top-Down", range(10)),
        ("Dh", dh348_3_2_3_1ns, "tmatTDNN", "topDown", "Top-Down", range(10)),
    ]:
        fig = makeTmats(
            data, tmatAddr, legendNames, reordering, figsize=figsize, zoom=0.04
        )

        fig.suptitle(f"${i}_{{309}}$ " + npTitle, fontsize=16, y=1)
        fig.set_layout_engine("tight")
        fig.savefig(f"SIfigure2{i}.png", bbox_inches="tight", pad_inches=0, dpi=300)

# %%
