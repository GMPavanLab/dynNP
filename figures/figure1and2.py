#%%
import figureSupportModule as fsm
import matplotlib.pyplot as plt
import numpy
from matplotlib.image import imread

#%%
data = fsm.dataLoaderBottomUp("../bottomUp/ico309soap.hdf5")
fsm.loadClassificationBottomUp(data, "../bottomUp/ico309classifications.hdf5")

fsm.addPseudoFes(data[300], 150, rangeHisto=[data["xlims"], data["ylims"]])
fsm.addPseudoFes(data[400], 150, rangeHisto=[data["xlims"], data["ylims"]])
fsm.addPseudoFes(data[500], 150, rangeHisto=[data["xlims"], data["ylims"]])
fsm.addTmatBU(data[300], 309)
fsm.addTmatBU(data[400], 309)
fsm.addTmatBU(data[500], 309)
#%% Figure 1
# for fig 1
figsize = numpy.array([2, 1]) * 8
fig1, axesFig1 = fsm.makeLayout1(figsize=figsize, dpi=300)

axesFig1["idealAx"].imshow(
    imread("fittedOn_ico309-SV_18631-SL_31922-T_300-125-eom_ideal.png")
)
axesFig1["idealSlicedAx"].imshow(
    imread("fittedOn_ico309-SV_18631-SL_31922-T_300-125-eom_ideal_sliced.png")
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
    axesFig1, 300, data[300], data["xlims"], data["ylims"], zoom=0.02
)
#%% Figure 2
# for fig 2
fig2, axesFig2 = fsm.makeLayout2(figsize=figsize, dpi=300)

for T in [400, 500]:
    fsm.plotTemperatureData(
        axesFig2, T, data[T], data["xlims"], data["ylims"], zoom=0.02
    )
    axesFig2[f"img{T}Ax"].imshow(imread(f"ico309_{T}-bottomUP.png"))
    axesFig2[f"img{T}Ax"].axis("off")

#%%
