#%%

import figureSupportModule as fsm

import numpy
from matplotlib.cm import ScalarMappable
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


#%%
AtomID = 155
data = {300: dict(), 400: dict(), 500: dict()}
fsm.loadClassificationBottomUp("../bottomUp/ico309classifications.hdf5", data, "ico309")
dictionary = numpy.array([fsm.bottomReordering_r.index(i) for i in range(8)])
colors = [fsm.bottomUpColorMap[i] for i in data[300]["ClassBU"].references[:, AtomID]]
#%%
figsize = numpy.array([4, 2]) * 3


fig, axes = fsm.makeLayout3(figsize=figsize, dpi=300)  # labelsOptions=dict(fontsize=15)

axes[f"NPTime"].imshow(imread(f"ico309_300_Tracking{AtomID}_Time.png"))
axes[f"NPClasses"].imshow(imread(f"ico309_300_Tracking{AtomID}_bottomUP.png"))
fig.colorbar(
    ScalarMappable(cmap="hot"),
    cax=axes[f"NPcbar"],
    orientation="horizontal",
    label=r"$\mu$ s",
    shrink=0.5,
)

for ax in [axes[f"NPTime"], axes[f"NPClasses"]]:
    ax.axis("off")
frames = list(range(1000))
for ax in [axes[f"followGraph"], axes[f"graphT400"]]:
    ax.set_yticks(
        list(range(8)), [fsm.bottomUpLabels[i] for i in fsm.bottomReordering_r]
    )

axes[f"followGraph"].scatter(
    frames,
    dictionary[data[300]["ClassBU"].references[:, AtomID]],
    c=colors,
)

axes[f"followGraph"].plot(
    frames, dictionary[data[300]["ClassBU"].references[:, AtomID]], c="k", alpha=0.5
)
axes[f"followGraph"].set_ylim(-0.25, 7.25)
for T in [300, 400, 500]:
    for i in range(data[T]["ClassBU"].references.shape[-1]):
        axes[f"graphT{T}"].plot(
            frames, dictionary[data[T]["ClassBU"].references[:, i]], c="k", alpha=0.025
        )
for ax in [axes[f"followGraph"], axes[f"graphT400"]]:
    ax.tick_params(axis="y", which="major", pad=15)
for ax in [axes[f"graphT300"], axes[f"graphT500"]]:
    ax.set_yticks(
        list(range(len(fsm.bottomUpLabels))), labels=[] * len(fsm.bottomUpLabels)
    )
imgzoom = 0.01
for i, l in enumerate(fsm.bottomUpLabels):
    img = OffsetImage(imread(f"bottomUp{i:04}.png"), zoom=imgzoom)
    pos = fsm.bottomUpLabels_ordered.index(l)

    for ax in [
        axes[f"followGraph"],
        axes[f"graphT400"],
        axes[f"graphT300"],
        axes[f"graphT500"],
    ]:
        ax.set_xticks(
            list(range(0, 1001, 200)), labels=["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"]
        )
        ax.set_xlabel("MD Time [$\mu$s]")
        ax.add_artist(
            AnnotationBbox(
                img,
                (0, pos),
                xybox=(-100, pos),
                frameon=False,
                xycoords="data",
                # box_alignment=(0.5, 0.5),
            )
        )


# %%
fig.savefig("figure3.png", bbox_inches="tight", pad_inches=0, dpi=300)
