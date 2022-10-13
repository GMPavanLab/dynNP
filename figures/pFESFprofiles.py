#%%
import figureSupportModule as fsm
import numpy
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from skimage.measure import profile_line
from scipy.ndimage import gaussian_filter


def getNearestPoint(data, x, y):
    idx = numpy.argmin(numpy.abs(data["pFESLimitsX"] - x))
    idy = numpy.argmin(numpy.abs(data["pFESLimitsY"] - y))
    return idx, idy


def plotLineAndProfile(data, LS, LE, axLine, axProfile, color="b"):
    ls = getNearestPoint(data, LS[0], LS[1])
    le = getNearestPoint(data, LE[0], LE[1])
    # axLine.plot(
    #     [data["pFESLimitsX"][ls[0]], data["pFESLimitsX"][le[0]]],
    #     [data["pFESLimitsY"][ls[1]], data["pFESLimitsY"][le[1]]],
    #     c=color,
    # )
    axLine.annotate(
        "",
        xy=[data["pFESLimitsX"][le[0]], data["pFESLimitsY"][le[1]]],
        xytext=[data["pFESLimitsX"][ls[0]], data["pFESLimitsY"][ls[1]]],
        c=color,
        arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3", color=color),
        xycoords="data",
        textcoords="data",
        zorder=5,
    )
    profile = profile_line(pFES, ls[::-1], le[::-1])
    xArray = numpy.linspace(0, 1, len(profile))
    axProfile.plot(xArray, profile, c=color)


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
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
T = 300
smooth = 0.0
t = numpy.array(data[T]["pFES"])
mymax = int(numpy.max(t[numpy.isfinite(t)]))
t[numpy.isinf(t)] = numpy.max(t[numpy.isfinite(t)])
pFES = t
if smooth > 0.0:
    pFES = gaussian_filter(t, sigma=smooth, order=0)

ax[0].contourf(
    data[T]["pFESLimitsX"],
    data[T]["pFESLimitsY"],
    pFES,
    levels=10,
    cmap=fsm.pFEScmap,
    zorder=1,
    extend="max",
    vmax=mymax,
)


# ax[0].set_xlim(right=-0.1)
# ax[0].set_ylim(top=-0.0,bottom=-0.1)
# ax[0].grid(True)
plotLineAndProfile(data[T], (-0.05, 0.12), (-0.025, 0.07), ax[0], ax[1], color="k")
plotLineAndProfile(data[T], (0.31, -0.03), (0.1, -0.01), ax[0], ax[1], color="g")
plotLineAndProfile(data[T], (-0.135, -0.039), (-0.17, -0.053), ax[0], ax[1], color="b")

#%%
