#%%
import matplotlib.pyplot as plt
import numpy
import figureSupportModule as fsm
from string import ascii_lowercase as labels
from matplotlib.image import imread
import sys

sys.path.insert(0, "../topDown")
from referenceMaker import (
    getDefaultReferencesSubdict,
    getDefaultReferences,
    referenceDendroMaker,
    renamer,
)

#%%
__titleDict = dict(
    fontdict=dict(weight="bold"),
    loc="left",
)
def makeLayout4(figsize, **figkwargs):
    fig = plt.figure(figsize=figsize, **figkwargs)
    mainGrid = fig.add_gridspec(4, 2, width_ratios=[1, 3])

    axes = dict(
        NPAx=fig.add_subplot(mainGrid[:3, 0]),
        icoAx=fig.add_subplot(mainGrid[0, 1]),
        dhAx=fig.add_subplot(mainGrid[1, 1]),
        toAx=fig.add_subplot(mainGrid[2, 1]),
        fullAx=fig.add_subplot(mainGrid[3, :]),
    )
    axes["NPAx"].axis("off")
    axes["ico309Im"] = axes["NPAx"].inset_axes([0.0, 0.7, 0.5, 0.15])
    axes["dh348Im"] = axes["NPAx"].inset_axes([0.0, 0.4, 0.5, 0.15])
    axes["to309Im"] = axes["NPAx"].inset_axes([0.0, 0.1, 0.5, 0.15])
    axes["ico923Im"] = axes["NPAx"].inset_axes([0.5, 0.75, 0.5, 0.15])
    axes["dh1734Im"] = axes["NPAx"].inset_axes([0.5, 0.5, 0.5, 0.15])
    axes["dh1086Im"] = axes["NPAx"].inset_axes([0.5, 0.25, 0.5, 0.15])
    axes["to976Im"] = axes["NPAx"].inset_axes([0.5, 0.0, 0.5, 0.15])
    for k in axes:
        if "Im" in k:
            axes[k].set_title(k)

    for i, ax in enumerate(
        [
            axes["NPAx"],
            axes["icoAx"],
            axes["dhAx"],
            axes["toAx"],
            axes["fullAx"],
        ]
    ):
        ax.set_title(labels[i],**__titleDict)
    return fig, axes


figsize = numpy.array([4, 3]) * 3
NPS = ["ico", "dh", "to"]
refs = {k: getDefaultReferencesSubdict(k, "../topDown/References.hdf5") for k in NPS}
refs["all"] = getDefaultReferences("../topDown/References.hdf5")

#%%


fig, axes = makeLayout4(figsize, dpi=300)
print(axes.keys())
for k in NPS:
    labels = [renamer[k]() for k in refs[k].names]
    referenceDendroMaker(refs[k], ax=axes[f"{k}Ax"], labels=labels)
    # axes[f"{k}Ax"].axis("off")

# %%
