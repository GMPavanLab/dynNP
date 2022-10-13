#%%
import figureSupportModule as fsm
import numpy
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

#%%
data = fsm.dataLoaderBottomUp("../bottomUp/ico309soap.hdf5")
fsm.loadClassificationBottomUp(data, "../bottomUp/ico309classifications.hdf5")

fsm.addPseudoFes(data[300], 150, rangeHisto=[data["xlims"], data["ylims"]])
fsm.addPseudoFes(data[400], 150, rangeHisto=[data["xlims"], data["ylims"]])
fsm.addPseudoFes(data[500], 150, rangeHisto=[data["xlims"], data["ylims"]])
fsm.addTmatBU(data[300], 309)
fsm.addTmatBU(data[400], 309)
fsm.addTmatBU(data[500], 309)

#%%
figsize = numpy.array([2, 1]) * 8
labelsOptions = dict(fontsize=15)
imgzoom = 0.015
pFESsmoothing = 0.5
#%% Figure 1
# for fig 1

fig1, axesFig1 = fsm.makeLayout1(labelsOptions=labelsOptions, figsize=figsize, dpi=300)

axesFig1["idealAx"].imshow(
    imread("fittedOn_ico309-SV_18631-SL_31922-T_300-125-eom_ideal.png")
)
axesFig1["idealSlicedAx"].imshow(
    imread("fittedOn_ico309-SV_18631-SL_31922-T_300-125-eom_ideal_sliced.png")
)

axesFig1["soapAx"].imshow(imread("ico309SOAPexample.png"))

axesFig1["legendAx"]
n = 0
offset = -0.05
for i, l in enumerate(fsm.bottomUpLabels):
    img = OffsetImage(imread(f"bottomUp{i:04}.png"), zoom=imgzoom)
    pos = fsm.bottomUpLabels_ordered.index(l)
    axesFig1[f"legendAx"].add_artist(
        AnnotationBbox(
            img,
            (0, pos),
            # xybox=(i, n + offset),
            frameon=False,
            xycoords="data",
            # box_alignment=(0.5, 0.5),
        )
    )
    axesFig1[f"legendAx"].annotate(l, (0.1, pos), va="center")

axesFig1[f"legendAx"].set_xlim(-0.8, 0.5)
axesFig1[f"legendAx"].set_ylim(-0.5, len(fsm.bottomUpLabels) - 0.5)
axesFig1[f"legendAx"].axis("off")
pos = 0
scaledict = {1: 1.5, 2: 2.2, 3: 2.45}
for label, width in [
    ("bulk", 2),
    ("subSurf", 2),
    ("concave*", 1),
    ("surface", 3),
]:
    place = pos + width / 2
    pos += width
    axesFig1[f"legendAx"].annotate(
        label,
        (-0.05, place - 0.5),
        (-0.5, place - 0.5),
        xycoords="data",
        textcoords="data",
        # size="large", color="tab:blue",
        horizontalalignment="left",
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
for ax in [
    axesFig1[f"soapAx"],
    axesFig1[f"idealSlicedAx"],
    axesFig1[f"idealAx"],
    axesFig1[f"img300Ax"],
]:
    ax.axis("off")
axesFig1["img300Ax"].imshow(imread("ico309_300-bottomUP.png"))
fsm.plotTemperatureData(
    axesFig1,
    300,
    data[300],
    data["xlims"],
    data["ylims"],
    zoom=imgzoom,
    smooth=pFESsmoothing,
)
#%% Figure 2
# for fig 2
fig2, axesFig2 = fsm.makeLayout2(labelsOptions=labelsOptions, figsize=figsize, dpi=300)

for T in [400, 500]:
    fsm.plotTemperatureData(
        axesFig2,
        T,
        data[T],
        data["xlims"],
        data["ylims"],
        zoom=imgzoom,
        smooth=pFESsmoothing,
    )
    axesFig2[f"img{T}Ax"].imshow(imread(f"ico309_{T}-bottomUP.png"))
    axesFig2[f"img{T}Ax"].axis("off")

#%%
fig1.savefig(f"figure1.png", bbox_inches="tight", pad_inches=0, dpi=300)
fig2.savefig(f"figure2.png", bbox_inches="tight", pad_inches=0, dpi=300)
#%%
