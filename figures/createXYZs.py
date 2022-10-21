#%%
from HDF5er import getXYZfromTrajGroup
import h5py
import figureSupportModule as fsm

#%% Trajectories
trajectorySlice = slice(10000, None, 10)
for NPname in ["dh348_3_2_3", "to309_9_4", "ico309"]:
    print(f"{NPname}:")
    data = {300: {}, 400: {}, 500: {}}
    # loading data
    fsm.loadClassificationBottomUp(f"../{NPname}classifications.hdf5", data, NPname)
    fsm.loadClassificationTopDown(f"../{NPname}TopBottom.hdf5", data, NPname)
    # Exporting xyz
    with h5py.File(f"../{NPname}_fitted.hdf5", "r") as trajFile:
        g = trajFile["Trajectories"]
        for k in g:
            T = fsm.getT(k)
            print(f"\t{T}")
            if T in data:
                # nat = g[k]["Types"].shape[-1]
                with open(f"{NPname}_{T}lastUs@1ns.xyz", "w") as icoFile:
                    getXYZfromTrajGroup(
                        icoFile,
                        g[k],
                        framesToExport=trajectorySlice,
                        allFramesProperty='Origin="-40 -40 -40"',
                        topDown=data[T]["ClassTD"].references[trajectorySlice],
                        bottomUp=data[T]["ClassBU"].references[trajectorySlice],
                    )
#%% Ideals:
from SOAPify import SOAPclassification

for NPname in ["dh348_3_2_3", "to309_9_4", "ico309"]:
    print(f"{NPname}:")
    data = {"Ideal": {}}
    T = "Ideal"
    # loading data

    # with h5py.File(f"../minimized.hdf5", "r") as f:
    #     Simulations = f["/Classifications/ico309-SV_18631-SL_31922-T_300"]
    #     data["Ideal"]["ClassBU"] = SOAPclassification(
    #             [], Simulations[NPname]["labelsNN"][:], fsm.bottomUpLabels
    #         )
    fsm.loadClassificationBottomUp(f"../minimized.hdf5", data, NPname)
    fsm.loadClassificationTopDown("../minimized.hdf5", data, NPname)

    # Exporting xyz
    with h5py.File(f"../minimized.hdf5", "r") as trajFile:
        g = trajFile[f"Trajectories/{NPname}"]
        with open(f"{NPname}_{T}.xyz", "w") as icoFile:
            getXYZfromTrajGroup(
                icoFile,
                g,
                allFramesProperty='Origin="-40 -40 -40"',
                topDown=data[T]["ClassTD"].references,
                bottomUp=data[T]["ClassBU"].references,
            )

# %%
