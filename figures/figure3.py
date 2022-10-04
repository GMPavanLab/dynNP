#%%
import figureSupportModule as fsm
import numpy
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.image import imread

#%%
AtomID = 155
data = {300: dict(), 400: dict(), 500: dict()}
fsm.loadClassificationBottomUp(data, "../bottomUp/ico309classifications.hdf5")
for T in [300, 400, 500]:
    data[T]["labelsNN"] = data[T]["labelsNN"].reshape(1000, -1)
dictionary = numpy.array([fsm.bottomReordering_r.index(i) for i in range(8)])
colors = [fsm.bottomUpColorMap[i] for i in data[300]["labelsNN"][:, AtomID]]
#%%
figsize = numpy.array([4, 2]) * 3

fig, axes = fsm.makeLayout3(figsize, dpi=300)

axes[f"NPTime"].imshow(imread(f"ico309_300_Tracking{AtomID}_Time.png"))
axes[f"NPClasses"].imshow(imread(f"ico309_300_Tracking{AtomID}_bottomUP.png"))
fig.colorbar(
    ScalarMappable(cmap="hot"),
    cax=axes[f"NPcbar"],
    orientation="horizontal",
    label=r"$\mu$ s",
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
    dictionary[data[300]["labelsNN"][:, AtomID]],
    c=colors,
)

axes[f"followGraph"].plot(
    frames, dictionary[data[300]["labelsNN"][:, AtomID]], c="k", alpha=0.5
)
axes[f"followGraph"].set_ylim(-0.25, 7.25)
for T in [300, 400, 500]:
    for i in range(data[T]["labelsNN"].shape[-1]):
        axes[f"graphT{T}"].plot(
            frames, dictionary[data[T]["labelsNN"][:, i]], c="k", alpha=0.05
        )


# %%
