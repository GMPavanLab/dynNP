#%%
from symbol import parameters
import h5py
from sklearn.decomposition import PCA
import SOAPify

#%%
def preparePCAFitSet(fitsetData: h5py.Dataset, PCAdim: int):
    # given a fitset makes the PCA algorithm learn the parameters
    fitset = fitsetData[:].reshape(-1, fitsetData.shape[-1])
    print(fitset.shape)
    lmax = fitsetData.attrs["l_max"]
    nmax = fitsetData.attrs["n_max"]
    fitset = SOAPify.fillSOAPVectorFromdscribe(fitset, lmax, nmax)
    fitset = SOAPify.normalizeArray(fitset)
    pcaMaker = PCA(PCAdim)
    pcaMaker.fit(fitset[:])
    return pcaMaker


def applypca(fname, pcaMaker, pcaname):
    chunklen = 100
    pcadim = pcaMaker.n_components_
    with h5py.File(fname, "a") as SOAPFile:
        pcaGroup = SOAPFile.require_group(f"PCAs/{pcaname}")
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
                    SOAPify.fillSOAPVectorFromdscribe(data[chunkTraj], lmax, nmax)
                )
                pcaRes = pcaMaker.transform(
                    normalizedData.reshape((-1, normalizedData.shape[-1]))
                )
                pcaout[chunkTraj[0]] = pcaRes.reshape((-1, data.shape[1], pcadim))

            pcaout.attrs["variance"] = pcaMaker.explained_variance_ratio_


#%%
# loading the fitset
with h5py.File("ico309soap.hdf5", "r") as file:
    pcaMaker = preparePCAFitSet(file["SOAP/ico309-SV_18631-SL_31922-T_300"], 8)
#%%
for fname in ["dh348_3_2_3soap.hdf5", "ico309soap.hdf5", "to309_9_4soap.hdf5"]:
    applypca(fname, pcaMaker, "ico309-SV_18631-SL_31922-T_300")
