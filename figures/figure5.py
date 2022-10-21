#%%
import numpy
import figureSupportModule as fsm
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from figure6and7 import addNPImages
import sys

sys.path.insert(0, "../topDown")
from TD00_referenceMaker import (
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
    classificationFile = f"../{NPname}TopBottom.hdf5"
    fsm.loadClassificationTopDown(
        classificationFile, data[NPname], NPname, fsm.trajectorySlice
    )
    fsm.loadClassificationTopDown("../minimized.hdf5", data[NPname], NPname)


for NP in data:
    for T in data[NP]:
        if T == "Ideal":
            continue
        fsm.addTmatTD(data[NP][T])
        fsm.addTmatTDNN(data[NP][T])
#%%
figsize = numpy.array([5, 4]) * 3
zoom = 0.01

fig, axes = fsm.makeLayout5(labelsOptions=dict(fontsize=15), figsize=figsize, dpi=300)
# ['dendro', 'legend', 'npIdeal', 'np300', 'tmat300', 'chord300',
#  'np400', 'tmat400', 'chord400', 'np500', 'tmat500', 'chord500', 'Histo']
##%%
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
    axes[f"tmat{T}"].tick_params(axis="both", which="major", pad=15)
    axes[f"tmat{T}"].xaxis.set_ticks_position("none")
    fsm.AddTmatsAndChord5_6_7(
        axes,
        data[NP][T],
        T,
        zoom=zoom,
        cbarAx=None if T != 500 else axes["tmatCMAP"],
        tmatOptions=dict(
            linewidth=1,
            cbar_kws={} if T != 500 else {"label": "Probability"},
            xticklabels=fsm.topDownLabels,
        ),
        chordOptions=dict(
            visualizationScale=0.85,
            labels=fsm.topDownLabels,
            labelpos=1.2,
            # labelskwargs = dict(),
        ),
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
axes[f"dendro"].set_ylim(bottom=-0.05)
for spine in ["top", "right", "bottom", "left"]:
    axes[f"dendro"].spines[spine].set_visible(False)
n = 0
offset = -0.05
for i, l in enumerate(fsm.topDownLabels):
    img = OffsetImage(imread(f"topDown{i:04}.png"), zoom=zoom)

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
axes[f"legend"].set_xlim(-0.5, 9.5)
axes[f"legend"].set_ylim(-0.5, 0.5)
axes[f"legend"].axis("off")
pos = 0
scaledict = {1: 1.35, 2: 2.75, 3: 3.4}
scaledictH = {1: 1.35, 2: 3.0, 3: 3.9}
for label, width in [
    ("bulk", 1),
    ("subSurf", 2),
    ("concave", 2),
    ("surface", 3),
    ("vertex", 2),
]:
    place = pos + width / 2
    pos += width
    axes[f"legend"].annotate(
        label,
        (place - 0.5, -0.1),
        (place - 0.5, -0.4),
        xycoords="data",
        textcoords="data",
        # size="large", color="tab:blue",
        horizontalalignment="center",
        verticalalignment="center",
        arrowprops=dict(
            arrowstyle=f"-[,widthB={scaledict[width]*width/2}, lengthB=1.0, angleB=0",  # ="-[",
            #    connectionstyle="arc3,rad=-0.05",
            # color=reorderedColors[i],
            #    shrinkA=5,
            #    shrinkB=5,
            #    patchB=l,
        ),
        # bbox=dict(boxstyle="square", fc="w"),
    )
    # axes['tmat300'].annotate(
    #     label,
    #     (0,place),
    #     (-2,place),
    #     xycoords="data",
    #     textcoords="data",
    #     horizontalalignment="right",
    #     verticalalignment="center",
    #     arrowprops=dict(
    #         arrowstyle=f"-[,widthB={scaledictH[width]*width/2}, lengthB=1.0, angleB=0",  # ="-[",
    #     ),
    # )

# %%
fig.savefig("figure5.png", bbox_inches="tight", pad_inches=0, dpi=300)
