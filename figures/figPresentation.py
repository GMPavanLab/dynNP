#%%atomicNumbers
import matplotlib.pyplot as plt
import numpy
from ase.data import chemical_symbols as symbols
from seaborn import heatmap

#%%
atomicNumbers = [1, 8]
lmax = 0
nmax = 2

fullmat = nmax * nmax * (lmax + 1)
upperDiag = ((nmax + 1) * nmax) // 2 * (lmax + 1)

t = numpy.empty((fullmat + 2 * upperDiag), dtype=numpy.object_)
tn = numpy.empty((fullmat + 2 * upperDiag), dtype=int)
i = 0
for Z in atomicNumbers:
    for Zp in atomicNumbers:
        for l in range(lmax + 1):
            for n in range(nmax):
                for np in range(nmax):
                    if (np, Zp) >= (n, Z):
                        low = min(Z, Zp)
                        high = max(Z, Zp)
                        lowN = n if low == Z else np
                        highN = np if low == Z else n
                        t[
                            i
                        ] = f"${symbols[low]}^{{n{lowN}}} {symbols[high]}^{{n{highN}}}$"
                        tn[i] = i
                        print(i, t[i])
                        i += 1

#%%

tHH = [[0, 1], [1, 2]]
tHO = [[3, 4], [6, 5]]
tOO = [[7, 8], [8, 9]]
#%%
fig = plt.figure(figsize=(10, 5))
mainGrid = fig.add_gridspec(2, 3)
for i, mat in enumerate([tHH, tHO, tOO]):
    ax = fig.add_subplot(mainGrid[0, i])
    heatmap(
        mat,
        vmin=0,
        vmax=9,
        ax=ax,
        fmt="s",
        annot=t[mat],
        square=True,
        cmap="tab10",
        cbar=None,
    )
    ax.axis("off")
ax = fig.add_subplot(mainGrid[1, :])
heatmap(
    tn.reshape(1, -1),
    vmin=0,
    vmax=9,
    ax=ax,
    fmt="s",
    # annot=t.reshape(1, -1),
    cmap="tab10",
    cbar=None,
    square=True,
)
ax.axis("off")
fig.savefig("SOAPReordering.png", bbox_inches="tight", pad_inches=0, dpi=300)

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

data = {}
refs = getDefaultReferences("../topDown/References.hdf5")
for NPname in ["ico309"]:
    data[NPname] = dict()
    classificationFile = f"../topDown/{NPname}TopBottom.hdf5"
    fsm.loadClassificationTopDown(classificationFile, data[NPname], NPname)
    fsm.loadClassificationTopDown("../minimized.hdf5", data[NPname], NPname)


for NP in data:
    for T in data[NP]:
        if T == "Ideal":
            continue
        fsm.addTmatTD(data[NP][T])
        fsm.addTmatNNTD(data[NP][T])

#%%
def work(data, NP):
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


for NP in data:
    work(data, NP)

# %%
import seaborn

fig, ax = plt.subplots(1, 2, figsize=(10, 5))
mask = data[NP][300]["tmatNN"] == 0
i = 0
tmatOpts = dict(
    ax=ax[i],
    annot=True,
    mask=mask,
    square=True,
    cmap="rocket_r",
    # vmax=1,
    # vmin=0,
    xticklabels=False,
    yticklabels=False,
    linewidth=1,
)
# tmatOpts.update(tmatOptions)
seaborn.heatmap(
    data[NP][300]["tmat"],
    **tmatOpts,
)
reorder = list(range(10))
fsm.decorateTmatWithLegend("topDown", reorder, ax[i], zoom=0.02)
