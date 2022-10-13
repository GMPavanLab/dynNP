#%%
from matplotlib import offsetbox
import matplotlib.pyplot as plt
import numpy
import figureSupportModule as fsm
from string import ascii_lowercase as alph
from matplotlib.image import imread
import scipy.cluster.hierarchy as sch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import sys

sys.path.insert(0, "../topDown")
from referenceMaker import (
    getDefaultReferencesSubdict,
    getDefaultReferences,
    referenceDendroMaker,
    renamer,
)


#%%

figsize = numpy.array([5, 1.25]) * 3
NPS = ["ico", "dh", "to"]
refs = {k: getDefaultReferencesSubdict(k, "../topDown/References.hdf5") for k in NPS}
refs["icodhto"] = getDefaultReferences("../topDown/References.hdf5")
cut_at = 0.08
bias = dict(dh=12 + 13, to=12, ico=0)
zoom = 0.015
zoomScissors = zoom * 2
labelPad = 18


def makeLayout(figsize, **figkwargs):
    fig = plt.figure(figsize=figsize, **figkwargs)
    mainGrid = fig.add_gridspec(1, 1)
    axes = dict(
        icodhtoAx=fig.add_subplot(mainGrid[:]),
    )

    for k in axes:
        if "Im" in k:
            # continue
            # axes[k].set_title(k)
            axes[k].axis("off")

    return fig, axes


fig, axes = makeLayout(figsize, dpi=300)

k = "icodhto"
labels = [renamer[k]() for k in refs[k].names]
reorderedColors = [fsm.topDownColorMapHex[i] for i in [0, 1, 2, 4, 5, 3, 6, 7, 9, 8]]
sch.set_link_color_palette(reorderedColors)

dendro = referenceDendroMaker(
    refs[k],
    ax=axes[f"{k}Ax"],
    labels=labels,
    color_threshold=cut_at,
    above_threshold_color="#999",
)

axes[f"{k}Ax"].spines["bottom"].set_position("zero")
axes[f"{k}Ax"].tick_params(axis="x", which="major", pad=labelPad, rotation=90)
for i, l in enumerate(dendro["leaves"]):
    img = OffsetImage(imread(f"topDownFull{l:04}.png"), zoom=zoom)
    n = 0
    offset = -0.035
    ab = AnnotationBbox(
        img,
        (i * 10 + 5, 0),
        xybox=(i * 10 + 5, n + offset),
        frameon=False,
        xycoords="data",
        # box_alignment=(0.5, 0.5),
    )
    axes[f"{k}Ax"].add_artist(ab)
axes[f"{k}Ax"].hlines(cut_at, 0, 47 * 10, color="k", linestyles="--")
axes[f"{k}Ax"].add_artist(
    AnnotationBbox(
        OffsetImage(imread(f"Scissors.png"), zoom=zoomScissors),
        (47 * 10, cut_at),
        # xybox=(i * 10 + 5, n + offset),
        frameon=False,
        xycoords="data",
        # box_alignment=(0.5, 0.5),
    )
)

topDownLabels = [
    ("b", 8),  # 0
    ("ss", 7),  # 1
    ("ss'", 3),  # 2
    ("c'", 3),  # 3
    ("s", 8),  # 4
    ("c", 2),  # 5
    ("e", 3),  # 6
    ("e'", 7),  # 7
    ("v", 3),  # 8
    ("v'", 3),  # 9
]
pos = 0
myheight = -0.15
scaledict = {8: 1.75, 7: 1.75, 3: 1.7, 2: 1.6}
for i, (label, width) in enumerate(topDownLabels):
    place = (pos + width / 2) * 10
    pos += width
    axes[f"{k}Ax"].annotate(
        label,
        (place, myheight),
        (place, -0.25),
        xycoords="data",
        textcoords="data",
        # size="large", color="tab:blue",
        horizontalalignment="center",
        verticalalignment="center",
        arrowprops=dict(
            arrowstyle=f"-[,widthB={scaledict[width]*width/2}, lengthB=1.5, angleB=0",  # ="-[",
            #    connectionstyle="arc3,rad=-0.05",
            color=reorderedColors[i],
            lw=2
            #    shrinkA=5,
            #    shrinkB=5,
            #    patchB=l,
        ),
        # bbox=dict(boxstyle="square", fc="w"),
    )
axes[f"{k}Ax"].set_ylim(bottom=myheight)
for spine in ["top", "right", "bottom", "left"]:
    axes[f"{k}Ax"].spines[spine].set_visible(False)
axes[f"{k}Ax"].set_yticks([])
#%%
fig.savefig(f"figureOnlyDendro.png", bbox_inches="tight", pad_inches=0, dpi=300)
# %%
