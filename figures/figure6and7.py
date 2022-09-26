#%%
import matplotlib.pyplot as plt
import numpy
from string import ascii_lowercase as labels

#%%
def makeLayout5(figsize, **figkwargs):
    axes = dict()
    fig = plt.figure(figsize=figsize, **figkwargs)
    mainGrid = fig.add_gridspec(
        nrows=4, ncols=2, width_ratios=[1, 3], height_ratios=[1, 2, 2, 2]
    )
    legendGrid = mainGrid[0, :].subgridspec(1, 2)
    axes["dendro"] = fig.add_subplot(legendGrid[0])
    axes["legend"] = fig.add_subplot(legendGrid[1])
    npGrid = mainGrid[1:, 0].subgridspec(4, 1)
    tmatGrid = mainGrid[3, 1].subgridspec(1, 3)
    chordGrid = mainGrid[2, 1].subgridspec(1, 3)
    axes[f"npIdeal"] = fig.add_subplot(npGrid[0])
    for i, T in enumerate([300, 400, 500]):
        axes[f"np{T}"] = fig.add_subplot(npGrid[i + 1])
        axes[f"tmat{T}"] = fig.add_subplot(tmatGrid[i])
        axes[f"chord{T}"] = fig.add_subplot(chordGrid[i])

    axes["Histo"] = fig.add_subplot(mainGrid[1, 1])
    for i, ax in enumerate(
        [
            axes["dendro"],
            axes["npIdeal"],
            axes["Histo"],
            axes["chord300"],
            axes["tmat300"],
        ]
    ):
        ax.set_title(labels[i])
    return fig, axes


def makeLayout6and7(figsize, **figkwargs):
    axes = dict()
    fig = plt.figure(figsize=figsize, **figkwargs)
    mainGrid = fig.add_gridspec(nrows=3, ncols=2, width_ratios=[3, 1])
    npGrid = mainGrid[0, 0].subgridspec(1, 4)
    tmatGrid = mainGrid[2, 0].subgridspec(1, 3)
    chordGrid = mainGrid[:, 1].subgridspec(3, 1)
    axes[f"npIdeal"] = fig.add_subplot(npGrid[0])
    for i, T in enumerate([300, 400, 500]):
        axes[f"np{T}"] = fig.add_subplot(npGrid[i + 1])
        axes[f"tmat{T}"] = fig.add_subplot(tmatGrid[i])
        axes[f"chord{T}"] = fig.add_subplot(chordGrid[i])

    axes["Histo"] = fig.add_subplot(mainGrid[1, 0])
    for i, ax in enumerate(
        [
            axes["npIdeal"],
            axes["Histo"],
            axes["tmat300"],
            axes["chord300"],
        ]
    ):
        ax.set_title(labels[i])
    return fig, axes


#%%
figsize = numpy.array([4, 3]) * 3
fig, axes = makeLayout6and7(figsize, dpi=300)
