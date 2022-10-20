from BU00_pca import preparePCAFitSet, applypcaNewFile
from BU01_hdbscanPrediction import trainNoiseClassifier, classifyNPs
import h5py

fitSetSlice = slice(10000, None, 10)


def applyPCA():
    with h5py.File("../ico309soap.hdf5", "r") as file:
        pcaMaker = preparePCAFitSet(
            file["SOAP/ico309-SV_18631-SL_31922-T_300"],
            8,
            dataSetSlice=fitSetSlice,
        )

    for name in ["ico309", "dh348_3_2_3", "to309_9_4"]:
        fname = f"../{name}soap.hdf5"
        pcaFname = f"../{name}pca.hdf5"
        applypcaNewFile(fname, pcaFname, pcaMaker, "ico309-SV_18631-SL_31922-T_300")


def classify():
    hdnc = trainNoiseClassifier(
        soapFile="../ico309pca.hdf5",
        fitsetAddress="PCAs/ico309-SV_18631-SL_31922-T_300/ico309-SV_18631-SL_31922-T_300",
        fitSetSlice=fitSetSlice,
    )
    # main NPs
    for fname in ["ico309", "dh348_3_2_3", "to309_9_4"]:
        classifyNPs(
            hdnc,
            soapFile=f"../{fname}pca.hdf5",
            PCAGroupAddr="PCAs/ico309-SV_18631-SL_31922-T_300",
            outFile=f"../{fname}classifications.hdf5",
            whereToSave="Classifications/ico309-SV_18631-SL_31922-T_300",
        )


if __name__ == "__main__":
    from sys import argv

    if argv[1] == "pca":
        applyPCA()
    elif argv[1] == "classify":
        classify()
    else:
        applyPCA()
        classify()
