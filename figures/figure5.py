#%%
from matplotlib import offsetbox
import matplotlib.pyplot as plt
import numpy
import figureSupportModule as fsm
from string import ascii_lowercase as alph
from matplotlib.image import imread
import scipy.cluster.hierarchy as sch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from figure6and7 import addNPImages
import sys

sys.path.insert(0, "../topDown")
from referenceMaker import (
    getDefaultReferencesSubdict,
    getDefaultReferences,
    referenceDendroMaker,
    renamer,
)

#%%
data = {}
refs = getDefaultReferences("../topDown/References.hdf5")
for NPname in ["ico309"]:
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
figsize = numpy.array([5, 4]) * 3
zoom = 0.01
fig, axes = fsm.makeLayout5(figsize, dpi=300)
# ['dendro', 'legend', 'npIdeal', 'np300', 'tmat300', 'chord300', 'np400', 'tmat400', 'chord400', 'np500', 'tmat500', 'chord500', 'Histo']
NP = "ico309"
addNPImages(axes, data[NP], NP)
fsm.HistoMaker(
    axes["Histo"],
    data[NP],
    positions=[0, 1, 2, 9, 8, 3, 7, 5, 6, 4],
    barWidth=0.16,
    barSpace=0.05,
)
for T in [300, 400, 500]:
    fsm.AddTmatsAndChord5_6_7(
        axes,
        data[NP][T],
        T,
        zoom=zoom,
        cbarAx=None,  # $ if T != 500 else axes["tmatCMAP"],
        linewidth=0.1,
        cbar_kws={} if T != 500 else {"label": "Probability"},
    )
dendro = referenceDendroMaker(
    refs,
    ax=axes[f"dendro"],
    color_threshold=0,
    # labels=fsm.topDownLabelFound,
    p=10,
    truncate_mode="lastp",
)
axes[f"dendro"].set_xticks(axes[f"dendro"].get_xticks(), fsm.topDownLabelFound)
axes[f"dendro"].set_yticks([])
axes[f"dendro"].set_ylim(bottom=-0.1)
for spine in ["top", "right", "bottom", "left"]:
    axes[f"dendro"].spines[spine].set_visible(False)

for i, l in enumerate(fsm.topDownLabels):
    img = OffsetImage(imread(f"topDown{i:04}.png"), zoom=zoom)
    n = 0
    offset = -0.05
    pos = fsm.topDownLabelFound.index(l)
    ab = AnnotationBbox(
        img,
        (pos * 10 + 5, 0),
        xybox=(pos * 10 + 5, n + offset),
        frameon=False,
        xycoords="data",
        # box_alignment=(0.5, 0.5),
    )
    axes[f"dendro"].add_artist(ab)
    ab = AnnotationBbox(
        img,
        (i, 0),
        # xybox=(i, n + offset),
        frameon=False,
        xycoords="data",
        # box_alignment=(0.5, 0.5),
    )
    axes[f"legend"].annotate(l, (i, 0.1), ha="center")
    axes[f"legend"].add_artist(ab)
axes[f"legend"].set_xlim(-0.5, 10.5)
axes[f"legend"].set_ylim(-0.5, 0.5)
axes[f"legend"].axis("off")
