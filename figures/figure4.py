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
__titleDict = dict(
    fontdict=dict(weight="bold", horizontalalignment="right"),
    loc="left",
)


figsize = numpy.array([5, 4]) * 3
NPS = ["ico", "dh", "to"]
refs = {k: getDefaultReferencesSubdict(k, "../topDown/References.hdf5") for k in NPS}
refs["icodhto"] = getDefaultReferences("../topDown/References.hdf5")
cut_at = 0.08
bias = dict(dh=12 + 13, to=12, ico=0)
zoom = 0.015
zoomScissors = zoom * 2
labelPad = 17
#%%


def makeLayout4(figsize, **figkwargs):
    fig = plt.figure(figsize=figsize, **figkwargs)
    mainGrid = fig.add_gridspec(4, 2, width_ratios=[1, 2.5], wspace=0.1)
    dendroGrid = mainGrid[:3, 1].subgridspec(6, 1, height_ratios=[1, 0.25] * 3)
    axes = dict(
        NPAx=fig.add_subplot(mainGrid[:3, 0]),
        icoAx=fig.add_subplot(dendroGrid[0]),
        dhAx=fig.add_subplot(dendroGrid[2]),
        toAx=fig.add_subplot(dendroGrid[4]),
        icodhtoAx=fig.add_subplot(mainGrid[3, :]),
    )

    axes["NPAx"].axis("off")
    basesDist = 0.0
    basesH = (1 - basesDist * 3) / 4
    basesW = 0.6
    analizedDist = 0.0
    analyzedH = (1 - analizedDist * 4) / 3
    analyzedW = 0.4
    axes["ico309Im"] = axes["NPAx"].inset_axes(
        [0.0, analizedDist + 2 * (analyzedH + analizedDist), analyzedW, analyzedH],
        box_aspect=1,
    )
    axes["dh348_3_2_3Im"] = axes["NPAx"].inset_axes(
        [0.0, analizedDist + analyzedH + analizedDist, analyzedW, analyzedH],
        box_aspect=1,
    )
    axes["to309_9_4Im"] = axes["NPAx"].inset_axes(
        [0.0, analizedDist, analyzedW, analyzedH], box_aspect=1
    )

    axes["ico923_6Im"] = axes["NPAx"].inset_axes(
        [analyzedW, (basesH + basesDist) * 3, basesW, basesH], box_aspect=1
    )
    axes["dh1734_5_4_4Im"] = axes["NPAx"].inset_axes(
        [analyzedW, (basesH + basesDist) * 2, basesW, basesH], box_aspect=1
    )
    axes["dh1086_7_1_3Im"] = axes["NPAx"].inset_axes(
        [analyzedW, basesH + basesDist, basesW, basesH], box_aspect=1
    )
    axes["to976_12_4Im"] = axes["NPAx"].inset_axes(
        [analyzedW, 0.0, basesW, basesH], box_aspect=1
    )
    for k in axes:
        if "Im" in k:
            # continue
            # axes[k].set_title(k)
            axes[k].axis("off")

    for i, ax in enumerate(
        [
            axes["NPAx"],
            axes["icoAx"],
            axes["dhAx"],
            axes["toAx"],
            axes["icodhtoAx"],
        ]
    ):
        ax.set_title(alph[i], **__titleDict)
    return fig, axes


fig, axes = makeLayout4(figsize, dpi=300)


for k in NPS:
    labels = [renamer[k]() for k in refs[k].names]
    dendro = referenceDendroMaker(
        refs[k], ax=axes[f"{k}Ax"], labels=labels, color_threshold=0
    )
    axes[f"{k}Ax"].tick_params(axis="both", which="major", pad=labelPad)
    for i, l in enumerate(dendro["leaves"]):
        l += bias[k]
        img = OffsetImage(imread(f"topDownFull{l:04}.png"), zoom=zoom)
        n = 0
        offset = -0.05
        ab = AnnotationBbox(
            img,
            (i * 10 + 5, 0),
            xybox=(i * 10 + 5, n + offset),
            frameon=False,
            xycoords="data",
            # box_alignment=(0.5, 0.5),
        )
        axes[f"{k}Ax"].add_artist(ab)
    axes[f"{k}Ax"].set_yticks([])
    for spine in ["top", "right", "bottom", "left"]:
        axes[f"{k}Ax"].spines[spine].set_visible(False)

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
    offset = -0.05
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
scaledict = {8: 1.75, 7: 1.75, 3: 1.7, 2: 1.6}
for i, (label, width) in enumerate(topDownLabels):
    place = (pos + width / 2) * 10
    pos += width
    axes[f"{k}Ax"].annotate(
        label,
        (place, -0.27),
        (place, -0.4),
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
axes[f"{k}Ax"].set_ylim(bottom=-0.27)

for np in [
    "dh1086_7_1_3",
    "dh1734_5_4_4",
    "ico923_6",
    # "to807_11_3",
    "to976_12_4",
    "dh348_3_2_3",
    "ico309",
    "to309_9_4",
]:
    axes[f"{np}Im"].imshow(imread(f"{np}_topDown.png"))

for spine in ["top", "right", "bottom", "left"]:
    axes[f"{k}Ax"].spines[spine].set_visible(False)

axes[f"{k}Ax"].set_yticks([])
#%%
fig.savefig(f"figure4.png", bbox_inches="tight", pad_inches=0, dpi=300)
# %%
