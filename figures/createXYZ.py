#%%
from HDF5er import getXYZfromTrajGroup
import h5py
import figureSupportModule as fsm

#%% Trajectories
for NPname in ["dh348_3_2_3", "to309_9_4", "ico309"]:
    print(f"{NPname}:")
    data = {300: {}, 400: {}, 500: {}}
    # loading data
    fsm.loadClassificationBottomUp(data, f"../bottomUp/{NPname}classifications.hdf5")
    fsm.dataLoaderTopDown(f"../topDown/{NPname}TopBottom.hdf5", data, NPname)
    # Exporting xyz
    with h5py.File(f"../bottomUp/{NPname}_fitted.hdf5", "r") as trajFile:
        g = trajFile["Trajectories"]
        for k in g:
            T = fsm.getT(k)
            print(f"\t{T}")
            if T in data:
                nat = g[k]["Types"].shape[-1]
                with open(f"{NPname}_{T}lastUs@1ns.xyz", "w") as icoFile:
                    getXYZfromTrajGroup(
                        icoFile,
                        g[k],
                        allFramesProperty='Origin="-40 -40 -40"',
                        topDown=data[T]["Class"].references,
                        bottomUP=data[T]["labelsNN"].reshape(-1, nat),
                    )
#%% Ideals:
for NPname in ["dh348_3_2_3", "to309_9_4", "ico309"]:
    print(f"{NPname}:")
    data = {"Ideal": {}}
    T = "Ideal"
    # loading data

    with h5py.File(f"../minimized.hdf5", "r") as f:
        Simulations = f["/Classifications/ico309-SV_18631-SL_31922-T_300"]
        data["Ideal"]["labelsNN"] = Simulations[NPname]["labelsNN"][:].reshape(-1)
    # fsm.loadClassificationBottomUp(data, f"../minimized.hdf5")
    fsm.dataLoaderTopDown("../minimized.hdf5", data, NPname)

    # Exporting xyz
    with h5py.File(f"../minimized.hdf5", "r") as trajFile:
        g = trajFile[f"Trajectories/{NPname}"]
        nat = g["Types"].shape[-1]
        with open(f"{NPname}_{T}.xyz", "w") as icoFile:
            getXYZfromTrajGroup(
                icoFile,
                g,
                allFramesProperty='Origin="-40 -40 -40"',
                topDown=data[T]["Class"].references,
                bottomUP=data[T]["labelsNN"].reshape(-1, nat),
            )

# %%
