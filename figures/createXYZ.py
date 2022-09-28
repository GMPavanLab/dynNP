#%%
from HDF5er import getXYZfromTrajGroup
import h5py
import figureSupportModule as fsm

#%% decahedron and octahedron:
for NPname in ["dh348_3_2_3", "to309_9_4", "ico309"]:
    print(f"{NPname}:")
    data = {300: {}, 400: {}, 500: {}}
    # loading data
    fsm.loadClassificationBottomUp(data, f"../bottomUp/{NPname}classifications.hdf5")
    fsm.dataLoaderTopDown(f"../topDown/{NPname}TopBottom.hdf5", data, NPname)
    # Exporting xyz
    with h5py.File(f"../bottomUp/{NPname}_fitted.hdf5") as trajFile:
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
