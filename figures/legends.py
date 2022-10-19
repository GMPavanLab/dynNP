#%%
import figureSupportModule as fsm
import numpy
from matplotlib.image import imread
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

#%%
imgzoom = 0.025
fig, ax = plt.subplots(1, 1)
ax
n = 0
offset = -0.05
for i, l in enumerate(fsm.bottomUpLabels):
    img = OffsetImage(imread(f"bottomUp{i:04}.png"), zoom=imgzoom)
    pos = fsm.bottomUpLabels_ordered.index(l)
    ax.add_artist(
        AnnotationBbox(
            img,
            (0, pos),
            # xybox=(i, n + offset),
            frameon=False,
            xycoords="data",
            # box_alignment=(0.5, 0.5),
        )
    )
    ax.annotate(l, (0.1, pos), va="center")

ax.set_xlim(-0.8, 0.5)
ax.set_ylim(-0.5, len(fsm.bottomUpLabels) - 0.5)
ax.axis("off")
pos = 0
scaledict = {1: 2.4, 2: 2.9, 3: 3.1}
for label, width in [
    ("bulk", 2),
    ("subSurf", 2),
    ("concave*", 1),
    ("surface", 3),
]:
    place = pos + width / 2
    pos += width
    ax.annotate(
        label,
        (-0.05, place - 0.5),
        (-0.5, place - 0.5),
        xycoords="data",
        textcoords="data",
        horizontalalignment="left",
        verticalalignment="center",
        arrowprops=dict(
            arrowstyle=f"-[,widthB={scaledict[width]*width/2}, lengthB=1.0, angleB=0",
        ),
    )
fig.savefig("BottomUPLegend.png", bbox_inches="tight", pad_inches=0, dpi=300)
# %%
fig, ax = plt.subplots(1, 1)
ax
n = 0
offset = -0.05

for i, l in enumerate(fsm.topDownLabels):
    img = OffsetImage(imread(f"topDown{i:04}.png"), zoom=imgzoom)

    pos = fsm.topDownLabelFound.index(l)
    ab = AnnotationBbox(
        img,
        (0, i),
        # xybox=(i, n + offset),
        frameon=False,
        xycoords="data",
        # box_alignment=(0.5, 0.5),
    )
    ax.annotate(l, (0.1, i), ha="center")
    ax.add_artist(ab)
ax.set_xlim(-0.8, 0.5)
ax.set_ylim(-0.5, len(fsm.topDownLabelFound) - 0.5)
ax.axis("off")
pos = 0
scaledict = {1: 2.1, 2: 2.45, 3: 2.75}
# scaledictH = {1: 1.35, 2: 3.0, 3: 3.9}
for label, width in [
    ("bulk", 1),
    ("subSurf", 2),
    ("concave", 2),
    ("surface", 3),
    ("vertex", 2),
]:
    place = pos + width / 2
    pos += width
    ax.annotate(
        label,
        (-0.05, place - 0.5),
        (-0.3, place - 0.5),
        xycoords="data",
        textcoords="data",
        # size="large", color="tab:blue",
        horizontalalignment="center",
        verticalalignment="center",
        arrowprops=dict(
            arrowstyle=f"-[,widthB={scaledict[width]*width/2}, lengthB=1.0, angleB=0",  # ="-[",
        ),
    )
fig.savefig("topDownLegend.png", bbox_inches="tight", pad_inches=0, dpi=300)
