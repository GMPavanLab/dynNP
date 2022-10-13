#%%
from deeptime.decomposition import TICA
import h5py
import SOAPify
import numpy

import matplotlib.pyplot as plt
import hdbscan

#%%


def ticaPrepper(dataset):
    soapDIMS = dataset.shape[2]
    NAT = dataset.shape[1]
    nframes = dataset.shape[0]
    data = numpy.empty((NAT, nframes, soapDIMS), dtype=dataset.dtype)
    for i in range(NAT):
        data[i, :, :] = dataset[:, i, :]
    return data


def ticaDePrepper(ticaDataset):
    ticaDIMS = ticaDataset.shape[2]
    NAT = ticaDataset.shape[1]
    nframes = ticaDataset.shape[0]
    data = numpy.empty((nframes, NAT, ticaDIMS), dtype=ticaDataset.dtype)
    print("tica", ticaDataset.shape)
    print("data", data.shape)
    for i in range(NAT):
        data[:, i, :] = ticaDataset[i, :, :]
    return data


def preparePCAFitSet(fitsetData: h5py.Dataset, PCAdim: int, lagtime: int = 2):
    # given a fitset makes the PCA algorithm learn the parameters
    # fitset = ticaPrepper(fitsetData[:])
    fitset = fitsetData[:]
    lmax = fitsetData.attrs["l_max"]
    nmax = fitsetData.attrs["n_max"]
    fitset = SOAPify.fillSOAPVectorFromdscribe(fitset, lmax, nmax)
    fitset = SOAPify.normalizeArray(fitset)
    pcaMaker = TICA(dim=PCAdim, lagtime=lagtime)
    pcaMaker.fit(fitset[:])
    return pcaMaker


def applypca(fname, ticaFName, pcaMaker, pcaname):
    chunklen = 100
    pcadim = pcaMaker.dim
    with h5py.File(fname, "r") as SOAPFile, h5py.File(ticaFName, "a") as ticaFile:
        pcaGroup = ticaFile.require_group(f"TICAs/{pcaname}")
        pcaGroup.attrs["PCAOrigin"] = f"{pcaname}"
        for key in SOAPFile["SOAP"].keys():
            print(f"appling PCA to {key}")
            data = SOAPFile["SOAP"][key]
            lmax = data.attrs["l_max"]
            nmax = data.attrs["n_max"]
            pcaout = pcaGroup.require_dataset(
                key,
                shape=(data.shape[0], data.shape[1], pcadim),
                dtype=data.dtype,
                chunks=(chunklen, data.shape[1], pcadim),
                maxshape=(None, data.shape[1], pcadim),
                compression="gzip",
            )
            for chunkTraj in data.iter_chunks():
                print(f'{key}:working on SOAP chunk "{chunkTraj}"')
                normalizedData = SOAPify.normalizeArray(
                    SOAPify.fillSOAPVectorFromdscribe(
                        # ticaPrepper(
                        data[chunkTraj]
                        # )
                        ,
                        lmax,
                        nmax,
                    )
                )
                print("ndata", normalizedData.shape)
                pcaRes = pcaMaker.transform(ticaPrepper(normalizedData))
                pcaout[chunkTraj[0]] = pcaRes.reshape(-1, data.shape[1], pcadim)

            # pcaout.attrs["model"] = pcaMaker.model


#%%
# loading the fitset
with h5py.File("ico309soap.hdf5", "r") as file:
    pcaMaker = preparePCAFitSet(file["SOAP/ico309-SV_18631-SL_31922-T_300"], 3)

#%%
for fname in [
    "ico309soap.hdf5"
]:  # ["dh348_3_2_3soap.hdf5", "ico309soap.hdf5", "to309_9_4soap.hdf5"]:
    applypca(fname, "TICA_" + fname, pcaMaker, "ico309-SV_18631-SL_31922-T_300")
#%%

printData = dict()
pcaname = "ico309-SV_18631-SL_31922-T_300"
with h5py.File("TICA_ico309soap.hdf5", "r") as ticaFile:
    pcaGroup = ticaFile[f"TICAs/{pcaname}"]
    for key in pcaGroup.keys():
        printData[key] = pcaGroup[key][:].reshape(-1, pcaGroup[key].shape[-1])

#%%


clusterer = hdbscan.HDBSCAN().fit(printData[key][:])
#%%
print(set(clusterer.labels_))
plt.scatter(
    printData[key][:, 0], printData[key][:, 1], s=0.1, alpha=0.01, c=clusterer.labels_
)
numpy.
#%%
fig = plt.figure(figsize=(15, 15))

dims = printData[key].shape[-1]
mainGrid = fig.add_gridspec(dims, dims)
axes = numpy.empty((dims, dims), dtype=numpy.object_)
for i in range(dims):
    for j in range(dims):
        if i <= j:
            ax = fig.add_subplot(
                mainGrid[j, i],
                sharex=axes[i, j - 1] if j > 0 else None,
                sharey=axes[i - 1, j] if i > 0 else None,
            )
            # ax.set_title(f"{i}, {j}")
            axes[i, j] = ax
            ii = i
            ax.scatter(
                printData[key][:, ii],
                printData[key][:, j],
                s=0.1,
                c=clusterer.labels_,
                alpha=0.5,
            )
#%%
from HDF5er import getXYZfromTrajGroup

for NPname in ["ico309"]:
    data = {300: {"tica": clusterer.labels_}}
    # Exporting xyz
    with h5py.File(f"../bottomUp/{NPname}_fitted.hdf5", "r") as trajFile:
        g = trajFile["Trajectories"]
        for k in g:
            T = 300
            if T in data and str(T) in k:
                print(f"\t{T}")
                nat = g[k]["Types"].shape[-1]
                with open(f"{NPname}_{T}lastUs@1nsTICA.xyz", "w") as icoFile:
                    getXYZfromTrajGroup(
                        icoFile,
                        g[k],
                        allFramesProperty='Origin="-40 -40 -40"',
                        tica=data[T]["tica"].reshape(-1, nat),
                    )
