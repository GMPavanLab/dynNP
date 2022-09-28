#%%

import matplotlib.pyplot as plt

from matplotlib.image import imread
import figureSupportModule as fsm

import numpy


#%% Loading Data

data = {}
for NPname in ["dh348_3_2_3", "to309_9_4"]:
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


def makeLayout6and7(figsize, **figkwargs):
    axes = dict()
    fig = plt.figure(figsize=figsize, **figkwargs)
    mainGrid = fig.add_gridspec(nrows=3, ncols=2, width_ratios=[3, 1], wspace=0.1)
    npGrid = mainGrid[0, 0].subgridspec(1, 4)
    tmatGrid = mainGrid[2, 0].subgridspec(1, 4, width_ratios=[1, 1, 1, 0.05])
    chordGrid = mainGrid[:, 1].subgridspec(3, 1)
    axes[f"npIdeal"] = fig.add_subplot(npGrid[0])
    for i, T in enumerate([300, 400, 500]):
        axes[f"np{T}"] = fig.add_subplot(npGrid[i + 1])
        axes[f"tmat{T}"] = fig.add_subplot(tmatGrid[i])
        axes[f"chord{T}"] = fig.add_subplot(chordGrid[i])
    axes[f"tmatCMAP"] = fig.add_subplot(tmatGrid[3])
    axes[f"nps"] = fig.add_subplot(npGrid[:])
    axes[f"tmats"] = fig.add_subplot(tmatGrid[:])
    axes[f"chords"] = fig.add_subplot(chordGrid[:])
    axes["Histo"] = fig.add_subplot(mainGrid[1, 0])
    for i, ax in enumerate(
        [
            axes["nps"],
            axes["Histo"],
            axes["tmats"],
            axes["chords"],
        ]
    ):
        ax.set_title(alph[i], **__titleDict)
    for ax in [axes["nps"], axes["tmats"], axes["chords"]]:
        ax.axis("off")
    return fig, axes


def addNPImages(axes, data, NP):
    clusters0K = []
    NClasses = 10
    for T in ["Ideal", 300, 400, 500]:
        p = [1.0]
        if T == "Ideal":
            ideal = data[T]["Class"].references[0]
            clusters0K += [
                c for c in range(3, 10) if numpy.count_nonzero(ideal == c) > 0
            ]
        elif len(clusters0K) != 7:
            # print(clusters0K)
            clusterCountNotID = numpy.zeros(
                (data[T]["Class"].references.shape[0]), dtype=float
            )
            clusterCountID = numpy.zeros(
                (data[T]["Class"].references.shape[0]), dtype=float
            )
            for c in range(3, 10):
                if c in clusters0K:
                    clusterCountID += numpy.count_nonzero(
                        data[T]["Class"].references == c, axis=-1
                    )
                else:
                    clusterCountNotID += numpy.count_nonzero(
                        data[T]["Class"].references == c, axis=-1
                    )
            surfClusters = clusterCountID + clusterCountNotID
            clusterCountID /= surfClusters
            clusterCountNotID /= surfClusters
            p[0] = numpy.mean(clusterCountID)
            p += [numpy.mean(clusterCountNotID)]
        axes[f"np{T}"].imshow(imread(f"{NP}_{T}-topDown.png"))
        axes[f"np{T}"].set_title(f"{T}")
        pieax = axes[f"np{T}"].inset_axes([0.7, -0.2, 0.3, 0.3])
        axes[f"np{T}"].axis("off")
        pieax.set_box_aspect(1)
        pieax.pie(
            p,
            colors=["#e6e6e6", "#ed2fce"],
            wedgeprops={"linewidth": 1, "ec": "k"},
        )
        if len(p) == 1:
            p += [0]

        pieax.annotate(
            f"{int(p[1]*100)}%", (0, 0), (1, -1), color="#ed2fce", fontsize=15
        )


for NP in ["dh348_3_2_3", "to309_9_4"]:
    figsize = numpy.array([3.8, 3]) * 4
    # fig, axes = fsm.makeLayout6and7(figsize, dpi=300)
    fig, axes = makeLayout6and7(figsize, dpi=300)
    addNPImages(axes, data[NP], NP)
    for T in [300, 400, 500]:
        fsm.AddTmatsAndChord5_6_7(
            axes,
            data[NP][T],
            T,
            cbarAx=None if T != 500 else axes["tmatCMAP"],
            linewidth=0.1,
            cbar_kws={} if T != 500 else {"label": "Probability"},
        )

    # todo: add the arrows
    fsm.HistoMaker(axes["Histo"], data[NP], positions=[0, 1, 2, 9, 8, 3, 7, 5, 6, 4])


#%%
