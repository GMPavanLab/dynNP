#%%
import figureSupportModule as fsm
import matplotlib.pyplot as plt
import numpy
from matplotlib.image import imread

#%%
data = fsm.dataLoaderBottomUp("../bottomUp/ico309soap.hdf5")
fsm.loadClassification(data)

fsm.addPseudoFes(data[300], 150, rangeHisto=[data["xlims"], data["ylims"]])
fsm.addPseudoFes(data[400], 150, rangeHisto=[data["xlims"], data["ylims"]])
fsm.addPseudoFes(data[500], 150, rangeHisto=[data["xlims"], data["ylims"]])
fsm.addTmat(data[300])
fsm.addTmat(data[400])
fsm.addTmat(data[500])
#%%
# for fig 1
figsize = numpy.array([2, 1]) * 8
fig1 = plt.figure(figsize=figsize, dpi=300)
grid1 = fig1.add_gridspec(2, 4)


axesFig1 = dict(
    soapAx=fig1.add_subplot(grid1[0, 0]),
    idealAx=fig1.add_subplot(grid1[0, 1]),
    idealSlicedAx=fig1.add_subplot(grid1[0, 2]),
    legendAx=fig1.add_subplot(grid1[0, 3]),
)
axesFig1["idealAx"].imshow(
    imread("fittedOn_ico309-SV_18631-SL_31922-T_300-125-eom_ideal.png")
)
axesFig1["idealSlicedAx"].imshow(
    imread("fittedOn_ico309-SV_18631-SL_31922-T_300-125-eom_ideal_sliced.png")
)

axesFig1.update(
    fsm.createSimulationFigs(grid1[1, :].subgridspec(1, 4), fig1, name="300")
)
for ax in [
    axesFig1[f"soapAx"],
    axesFig1[f"idealSlicedAx"],
    axesFig1[f"idealAx"],
    axesFig1[f"img300Ax"],
]:
    ax.axis("off")
axesFig1["img300Ax"].imshow(
    imread(
        "ico309-SV_18631-SL_31922-T_300-fittedOn_ico309-SV_18631-SL_31922-T_300-125-eom.png"
    )
)
fsm.plotTemperatureData(
    axesFig1, 300, data[300], data["xlims"], data["ylims"], zoom=0.02
)
#%%
fig2 = plt.figure(figsize=figsize, dpi=300)
grid2 = fig2.add_gridspec(2, 4)
axesFig2 = dict()
axesFig2.update(
    fsm.createSimulationFigs(grid2[0, :].subgridspec(1, 4), fig2, name="400")
)
axesFig2.update(
    fsm.createSimulationFigs(grid2[1, :].subgridspec(1, 4), fig2, name="500")
)


for T in [400, 500]:
    fsm.plotTemperatureData(
        axesFig2, T, data[T], data["xlims"], data["ylims"], zoom=0.02
    )

#%%
