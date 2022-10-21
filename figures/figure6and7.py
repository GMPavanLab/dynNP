#%%
from matplotlib.image import imread
import figureSupportModule as fsm

import numpy


#%% Loading Data

data = {}
for NPname in ["dh348_3_2_3", "to309_9_4"]:
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


def addNPImages(axes, data, NP):
    clusters0K = []
    NClasses = 10
    for T in ["Ideal", 300, 400, 500]:
        p = [1.0]
        if T == "Ideal":
            ideal = data[T]["ClassTD"].references[0]
            clusters0K += [
                c for c in range(3, 10) if numpy.count_nonzero(ideal == c) > 0
            ]
        elif len(clusters0K) != 7:
            # print(clusters0K)
            clusterCountNotID = numpy.zeros(
                (data[T]["ClassTD"].references.shape[0]), dtype=float
            )
            clusterCountID = numpy.zeros(
                (data[T]["ClassTD"].references.shape[0]), dtype=float
            )
            for c in range(3, 10):
                if c in clusters0K:
                    clusterCountID += numpy.count_nonzero(
                        data[T]["ClassTD"].references == c, axis=-1
                    )
                else:
                    clusterCountNotID += numpy.count_nonzero(
                        data[T]["ClassTD"].references == c, axis=-1
                    )
            surfClusters = clusterCountID + clusterCountNotID
            clusterCountID /= surfClusters
            clusterCountNotID /= surfClusters
            p[0] = numpy.mean(clusterCountID)
            p += [numpy.mean(clusterCountNotID)]
        axes[f"np{T}"].imshow(imread(f"{NP}_{T}-topDown.png"))
        title = f"{T}\u2009K" if T != "Ideal" else "Ideal"
        axes[f"np{T}"].set_title(title)
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
            f" {int(p[1]*100)}%", (0, 0), (1, -1), color="#ed2fce", fontsize=15
        )


if __name__ == "__main__":
    for i, NP in enumerate(["dh348_3_2_3", "to309_9_4"], 6):
        figsize = numpy.array([3.8, 3]) * 4
        fig, axes = fsm.makeLayout6and7(
            labelsOptions=dict(fontsize=15), figsize=figsize, dpi=300
        )
        addNPImages(axes, data[NP], NP)
        for T in [300, 400, 500]:
            fsm.AddTmatsAndChord5_6_7(
                axes,
                data[NP][T],
                T,
                cbarAx=None if T != 500 else axes["tmatCMAP"],
                tmatOptions=dict(
                    # cmap="vlag_r",
                    # annot=fsm.getCompactedAnnotationsForTmat_percent(data[NP][T]["tmat"]),
                    # fmt='s',
                    linewidth=1,
                    cbar_kws={} if T != 500 else {"label": "Probability"},
                ),
                chordOptions=dict(
                    visualizationScale=0.85,
                    labels=fsm.topDownLabels,
                    labelpos=1.2,
                    # labelskwargs = dict(),
                ),
            )

        fsm.HistoMaker(
            axes["Histo"],
            data[NP],
            positions=[0, 1, 2, 9, 8, 3, 7, 5, 6, 4],
            barWidth=0.16,
            barSpace=0.05,
        )
        fig.savefig(f"figure{i}.png", bbox_inches="tight", pad_inches=0, dpi=300)


#%%
