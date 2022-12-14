#%%
import h5py
from sklearn.decomposition import PCA
import SOAPify

#%%
def preparePCAFitSet(
    fitsetData: h5py.Dataset, PCAdim: int, dataSetSlice: slice = slice(None)
):
    # given a fitset makes the PCA algorithm learn the parameters
    fitset = fitsetData[dataSetSlice].reshape(-1, fitsetData.shape[-1])
    print(
        f"Fitset shape: {fitset.shape}, frames from simulation: {fitsetData[dataSetSlice].shape[0]}"
    )
    lmax = fitsetData.attrs["l_max"]
    nmax = fitsetData.attrs["n_max"]
    fitset = SOAPify.fillSOAPVectorFromdscribe(fitset, lmax, nmax)
    fitset = SOAPify.normalizeArray(fitset)
    pcaMaker = PCA(PCAdim)
    pcaMaker.fit(fitset[:])
    return pcaMaker


def _applypca(SOAPFile, PCAFile, pcaMaker, pcaname, soapGroupName="SOAP"):
    chunklen = 1000
    pcadim = pcaMaker.n_components_
    pcaGroup = PCAFile.require_group(f"PCAs/{pcaname}")
    pcaGroup.attrs["PCAOrigin"] = f"{pcaname}"
    SOAPGroup = SOAPFile[soapGroupName]
    for key in SOAPGroup.keys():
        print(f"appling PCA to {key}")
        data = SOAPGroup[key]
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


def applypcaNewFile(fname, pcaFileName, pcaMaker, pcaname, soapGroupName="SOAP"):
    with h5py.File(fname, "r") as SOAPFile, h5py.File(pcaFileName, "a") as PCAFile:
        _applypca(SOAPFile, PCAFile, pcaMaker, pcaname, soapGroupName)


def applypca(fname, pcaMaker, pcaname, soapGroupName="SOAP"):
    with h5py.File(fname, "a") as SOAPFile:
        _applypca(SOAPFile, SOAPFile, pcaMaker, pcaname, soapGroupName)
        

if __name__ == "__main__":
    #%%
    # loading the fitset
    with h5py.File("ico309soap.hdf5", "r") as file:
        pcaMaker = preparePCAFitSet(file["SOAP/ico309-SV_18631-SL_31922-T_300"], 8)
    #%%
    for fname in ["dh348_3_2_3soap.hdf5", "ico309soap.hdf5", "to309_9_4soap.hdf5"]:
        applypca(fname, pcaMaker, "ico309-SV_18631-SL_31922-T_300")
    #%%
    for fname in ["../minimized.hdf5"]:
        applypca(fname, pcaMaker, "ico309-SV_18631-SL_31922-T_300")
