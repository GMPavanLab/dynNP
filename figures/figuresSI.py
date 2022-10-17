#%%
import figureSupportModule as fsm
import numpy
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import seaborn

#%%
Temps = [300, 400, 500]


def getFullData(np):
    data = fsm.pcaLoaderBottomUp(f"../bottomUp/{np}soap.hdf5")
    fsm.loadClassificationBottomUp(f"../bottomUp/{np}classifications.hdf5", data, np)
    fsm.loadClassificationTopDown(f"../topDown/{np}TopBottom.hdf5", data, np)

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


#%%
ico309_1ns = getFullData("ico309")
ico309_100ps = getFullDataStrided("ico309", slice(10000, None, None))
ico309_200ps = getFullDataStrided("ico309", slice(10000, None, 2))
#%%
ico309_100psFull = getFullDataStrided("ico309", slice(None))
ico309_1nsFull = getFullDataStrided("ico309", slice(None, None, 10))
#%%
figsize = numpy.array([3, 1]) * 10
zoom = 0.02

for i, (mytmat, legendNames, reordering) in enumerate(
    [
        ("tmatBUNN", "bottomUp", fsm.bottomReordering_r),
        ("tmatTDNN", "topDown", range(10)),
    ]
):
    fig = plt.figure(figsize=figsize, dpi=300)
    mainGrid = fig.add_gridspec(1, 3)
    for i, T in enumerate(Temps):
        ax = fig.add_subplot(mainGrid[i])
        tmat = ico309_1ns[T][mytmat]
        mask = tmat == 0
        annots = True  # fsm.getCompactedAnnotationsForTmat_percent(tmat)
        seaborn.heatmap(
            tmat,
            linewidths=1,
            ax=ax,
            # fmt="s",
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
        ax.set_title(f"{T} K")
        fsm.decorateTmatWithLegend(legendNames, reordering, ax, zoom=zoom)
    fig.savefig(f"SIfigure{i}.png", bbox_inches="tight", pad_inches=0, dpi=300)
# %%
figsize = numpy.array([3, 1]) * 10
zoom = 0.02
fig = plt.figure(figsize=figsize, dpi=300)
mainGrid = fig.add_gridspec(3, 2)
for i, T in enumerate(Temps):
    ax = fig.add_subplot(mainGrid[i, 0])
    tmat = ico309_1ns[T]["tmatBU"]
    mask = tmat == 0
    annots = fsm.getCompactedAnnotationsForTmat_percent(tmat)
    seaborn.heatmap(
        tmat,
        linewidths=0.1,
        ax=ax,
        fmt="s",
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
        vmax=1,
        vmin=0,
    )
    fsm.decorateTmatWithLegend("bottomUp", fsm.bottomReordering_r, ax, zoom=zoom)
    ax = fig.add_subplot(mainGrid[i, 1])
    tmat = ico309_100ps[T]["tmatBU"]
    mask = tmat == 0
    annots = fsm.getCompactedAnnotationsForTmat_percent(tmat)
    seaborn.heatmap(
        tmat,
        linewidths=0.1,
        ax=ax,
        fmt="s",
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
        vmax=1,
        vmin=0,
    )
    fsm.decorateTmatWithLegend("bottomUp", fsm.bottomReordering_r, ax, zoom=zoom)
# %%
def calculateTransitions(tmat, time):
    n = tmat.shape[0]
    rates = numpy.zeros_like(tmat)
    for i in range(n):
        for j in range(n):
            if i != j and tmat[i, j] != 0:
                rates[i, j] = 1.0 / (tmat[i, j] / time)
    return rates


figsize = numpy.array([2, 3]) * 10
zoom = 0.02
fig = plt.figure(figsize=figsize, dpi=300)
mainGrid = fig.add_gridspec(3, 2)
for i, T in enumerate(Temps):
    ax = fig.add_subplot(mainGrid[i, 0])
    tmat = calculateTransitions(ico309_1ns[T]["tmatBU"], 1)
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
    fsm.decorateTmatWithLegend("bottomUp", fsm.bottomReordering_r, ax, zoom=zoom)
    ax = fig.add_subplot(mainGrid[i, 1])
    tmat = calculateTransitions(ico309_100ps[T]["tmatBU"], 0.1)
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
    fsm.decorateTmatWithLegend("bottomUp", fsm.bottomReordering_r, ax, zoom=zoom)

# %%
figsize = numpy.array([2, 3]) * 10
zoom = 0.02
fig = plt.figure(figsize=figsize, dpi=300)
mainGrid = fig.add_gridspec(3, 2)
for i, T in enumerate(Temps):
    ax = fig.add_subplot(mainGrid[i, 0])
    tmat = calculateTransitions(ico309_1ns[T]["tmatTD"], 1)
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
    fsm.decorateTmatWithLegend("topDown", range(10), ax, zoom=zoom)
    ax = fig.add_subplot(mainGrid[i, 1])
    tmat = calculateTransitions(ico309_100ps[T]["tmatTD"], 0.1)
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
    fsm.decorateTmatWithLegend("topDown", range(10), ax, zoom=zoom)
# %%
figsize = numpy.array([2, 3]) * 10
zoom = 0.02
fig = plt.figure(figsize=figsize, dpi=300)
mainGrid = fig.add_gridspec(3, 2)
for i, T in enumerate(Temps):
    ax = fig.add_subplot(mainGrid[i, 0])
    tmat = calculateTransitions(ico309_200ps[T]["tmatTD"], 0.2)
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
    fsm.decorateTmatWithLegend("topDown", range(10), ax, zoom=zoom)
    ax = fig.add_subplot(mainGrid[i, 1])
    tmat = calculateTransitions(ico309_100ps[T]["tmatTD"], 0.1)
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
    fsm.decorateTmatWithLegend("topDown", range(10), ax, zoom=zoom)
# %%
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


# %%
figsize = numpy.array([2, 3]) * 10


def plotEquilibriumSingle(
    dataDict: dict, T: int, classNum: int, Class: str, color: list, ax=None
):
    axis = plt if ax is None else ax
    t = numpy.count_nonzero(dataDict[T][Class].references == classNum, axis=-1)
    axis.plot(range(t.shape[0]), t, color=color)


def figureEquilibrium(
    dataDict: dict, Class: str, cmap: list, figkwargs: dict, reorder=None
):

    fig = plt.figure(**figkwargs)
    tdNum = len(cmap)

    reordering = reorder if reorder else range(tdNum)
    mainGrid = fig.add_gridspec(tdNum, 3)
    axes = numpy.empty((tdNum, 3), dtype=numpy.object_)
    for i, T in enumerate(Temps):
        for j in range(tdNum):
            jj = reordering[j]
            axes[j, i] = fig.add_subplot(
                mainGrid[jj, i],
                sharex=axes[j - 1, i] if j != 0 else None,
                sharey=axes[j, i - 1] if i != 0 else None,
            )
            plotEquilibriumSingle(dataDict, T, j, Class, cmap[j], axes[j, i])


figureEquilibrium(
    ico309_1nsFull, "ClassTD", fsm.topDownColorMap, dict(figsize=figsize, dpi=300)
)
figureEquilibrium(
    ico309_1nsFull, "ClassBU", fsm.bottomUpColorMap, dict(figsize=figsize, dpi=300)
    , fsm.bottomReordering_r
)

# %%
figsize = numpy.array([2, 3]) * 10
fig = plt.figure(figsize=figsize, dpi=300)
mainGrid = fig.add_gridspec(3, 2)
for i, T in enumerate(Temps):
    stackEquilibrium(
        ico309_1nsFull,
        T,
        "ClassTD",
        fsm.topDownColorMap,
        fig.add_subplot(mainGrid[i, 1]),
    )
    stackEquilibrium(
        ico309_1nsFull,
        T,
        "ClassBU",
        fsm.bottomUpColorMap,
        fig.add_subplot(mainGrid[i, 0]),
        fsm.bottomReordering_r,
    )
#%%
ico309_1nsFF = getFullDataStrided("ico309", slice(None, 1000, 10))

figsize = numpy.array([2, 3]) * 10
fig = plt.figure(figsize=figsize, dpi=300)
mainGrid = fig.add_gridspec(3, 2)
for i, T in enumerate(Temps):
    plotEquilibrium(
        ico309_1nsFF,
        T,
        "ClassTD",
        fsm.topDownColorMap,
        fig.add_subplot(mainGrid[i, 1]),
    )
    plotEquilibrium(
        ico309_1nsFF,
        T,
        "ClassBU",
        fsm.bottomUpColorMap,
        fig.add_subplot(mainGrid[i, 0]),
    )
