#%%
from HDF5er import getXYZfromTrajGroup
import h5py
import figureSupportModule as fsm

#%%

bias = dict(dh=12 + 13, to=12, ih=0)


def xyzMakerForFig4(h5File, NPs):
    with h5py.File(h5File, "r") as f:
        g = f["Classifications"]
        classifications = dict()
        for NP in NPs:
            for npRef in ["dh", "ih", "to"]:
                data = g[f"{npRef}/{NP}"]
                classifications[npRef] = data[:] + bias[npRef]
                # print(npRef, NP, data.shape)
            with open(f"{NP}_topDown.xyz", "w") as icoFile:
                getXYZfromTrajGroup(
                    icoFile,
                    f[f"Trajectories/{NP}"],
                    allFramesProperty='Origin="-40 -40 -40"',
                    **classifications,
                )


#%%
xyzMakerForFig4(
    "../topDown/referenceFrames.hdf5",
    [
        "dh1086_7_1_3",
        "dh1734_5_4_4",
        "ico923_6",
        "to807_11_3",
        "to976_12_4",
    ],
)
#%%
xyzMakerForFig4("../minimized.hdf5", ["dh348_3_2_3", "ico309", "to309_9_4"])

# %%
