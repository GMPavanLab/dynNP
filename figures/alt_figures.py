#%%
import figureSupportModule as fsm
import numpy
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import AxesZero

NPs = ["ico309", "dh348_3_2_3", "to309_9_4"]
#%%
data = {}
ChosenNP = NPs[0]


def dataLoaderBottomUp(filename):
    import h5py

    dataContainer = dict()
    dataContainer["xlims"] = [numpy.finfo(float).max, numpy.finfo(float).min]
    dataContainer["ylims"] = [numpy.finfo(float).max, numpy.finfo(float).min]
    with h5py.File(filename, "r") as f:
        pcas = f["/PCAs/ico309-SV_18631-SL_31922-T_300"]
        for k in pcas:
            dataContainer["nat"] = f[f"/SOAP/{k}"].shape[1]
            T = fsm.getT(k)
            dataContainer[T] = dict(pca=pcas[k][:, :, :2].reshape(-1, 2))
            dataContainer["xlims"][0] = fsm.getMin(
                dataContainer["xlims"][0], dataContainer[T]["pca"][:, 0]
            )
            dataContainer["xlims"][1] = fsm.getMax(
                dataContainer["xlims"][1], dataContainer[T]["pca"][:, 0]
            )
            dataContainer["ylims"][0] = fsm.getMin(
                dataContainer["ylims"][0], dataContainer[T]["pca"][:, 1]
            )
            dataContainer["ylims"][1] = fsm.getMax(
                dataContainer["ylims"][1], dataContainer[T]["pca"][:, 1]
            )

    return dataContainer


data[ChosenNP] = dataLoaderBottomUp(f"../bottomUp/{ChosenNP}soap.hdf5")
fsm.loadClassificationBottomUp(
    data[ChosenNP], f"../bottomUp/{ChosenNP}classifications.hdf5"
)
nat = data[ChosenNP]["nat"]

for T in [300, 400, 500]:
    fsm.addPseudoFes(
        data[ChosenNP][T],
        150,
        rangeHisto=[data[ChosenNP]["xlims"], data[ChosenNP]["ylims"]],
    )
    fsm.addTmatBUNN(data[ChosenNP][T], nat)


for NPname in [ChosenNP]:
    classificationFile = f"../topDown/{NPname}TopBottom.hdf5"
    fsm.loadClassificationTopDown(classificationFile, data[NPname], NPname)
#%%
def dataLoaderBottomUpMinimized(filename, k):
    import h5py

    dataContainer = dict()
    dataContainer["xlims"] = [numpy.finfo(float).max, numpy.finfo(float).min]
    dataContainer["ylims"] = [numpy.finfo(float).max, numpy.finfo(float).min]
    with h5py.File(filename, "r") as f:
        pcas = f[f"/PCAs/ico309-SV_18631-SL_31922-T_300/{k}"]
        dataContainer["nat"] = f[f"/SOAP/{k}"].shape[1]
        dataContainer = dict(pca=pcas[:, :, :3].reshape(-1, 3))

    return dataContainer


dataMIN = dataLoaderBottomUpMinimized("../minimized.hdf5", ChosenNP)

#%%
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(1, 1, 1, axes_class=AxesZero)
ax.scatter(
    data[ChosenNP][300]["pca"][:, 0],
    data[ChosenNP][300]["pca"][:, 1],
    s=0.1,
    c=numpy.array(fsm.topDownColorMap)[
        data[ChosenNP][300]["ClassTD"].references.reshape(-1)
    ],
    alpha=0.5,
)

for ax in [ax]:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    for direction in ["left", "bottom"]:
        ax.axis[direction].set_axisline_style("-|>")

    for direction in ["right", "top"]:
        ax.axis[direction].set_visible(False)

fig.savefig("PCATD.png", bbox_inches="tight", pad_inches=0, dpi=300)
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(1, 1, 1, axes_class=AxesZero)
ax.scatter(
    data[ChosenNP][300]["pca"][:, 0],
    data[ChosenNP][300]["pca"][:, 1],
    s=0.1,
    c=numpy.array(fsm.bottomUpColorMap)[data[ChosenNP][300]["labelsNN"]],
    alpha=0.5,
)

for ax in [ax]:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    for direction in ["left", "bottom"]:
        ax.axis[direction].set_axisline_style("-|>")

    for direction in ["right", "top"]:
        ax.axis[direction].set_visible(False)

fig.savefig("PCABU.png", bbox_inches="tight", pad_inches=0, dpi=300)

#%%
fig, ax = plt.subplots(1, 1, figsize=(5, 5))
chordOpts = dict(
    colors=fsm.bottomUpColorMap,
    ax=ax,
    onlyFlux=True,
)

fsm.ChordDiagram(data[ChosenNP][500]["tmatNN"], **chordOpts)
#%%
T = 300
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.scatter(
    data[ChosenNP][T]["pca"][:, 0],
    data[ChosenNP][T]["pca"][:, 1],
    s=0.1,
    c=numpy.array(fsm.bottomUpColorMap)[data[ChosenNP][T]["labelsNN"].reshape(-1)],
    alpha=0.5,
)

countourOptions = dict(
    levels=10,
    colors="k",
    linewidths=0.1,
    zorder=2,
)
ax.contour(
    data[ChosenNP][T]["pFESLimitsX"],
    data[ChosenNP][T]["pFESLimitsY"],
    data[ChosenNP][T]["pFES"],
    **countourOptions,
)

ax.scatter(
    dataMIN["pca"][:, 0],
    dataMIN["pca"][:, 1],
    s=20,
    c="k",
    # alpha=0.5,
)

ax.scatter(
    dataMIN["pca"][:, 0],
    dataMIN["pca"][:, 1],
    s=10,
    c="r",
    # alpha=0.5,
)
#%%
T = 300
fig = plt.figure(figsize=(10, 5))


mainGrid = fig.add_gridspec(3, 3)
axes = numpy.empty((3, 3), dtype=numpy.object_)
for i in [0, 1, 2]:
    for j in [0, 1, 2]:
        if i <= j:
            ax = fig.add_subplot(
                mainGrid[j, i],
                sharex=axes[i, j - 1] if j > 0 else None,
                sharey=axes[i - 1, j] if i > 0 else None,
            )
            # ax.set_title(f"{i}, {j}")
            axes[i, j] = ax
            ii = i
            ax.scatter(
                data[ChosenNP][T]["pca"][:, ii],
                data[ChosenNP][T]["pca"][:, j],
                s=0.1,
                c=numpy.array(fsm.bottomUpColorMap)[
                    data[ChosenNP][T]["labelsNN"].reshape(-1)
                ],
                alpha=0.5,
            )
            ax.scatter(
                dataMIN["pca"][:, ii],
                dataMIN["pca"][:, j],
                s=20,
                c="k",
                # alpha=0.5,
            )

            ax.scatter(
                dataMIN["pca"][:, ii],
                dataMIN["pca"][:, j],
                s=10,
                c="r",
                # alpha=0.5,
            )
