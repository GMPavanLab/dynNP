from BU00_pca import preparePCAFitSet, applypcaNewFile
from BU01_hdbscanPrediction import trainNoiseClassifier, classifyNPs
import h5py

"""
with h5py.File("ico309soap.hdf5", "r") as file:
    pcaMaker = preparePCAFitSet(file["SOAP/ico309-SV_18631-SL_31922-T_300"], 8)

for name in ["ico309", "dh348_3_2_3", "to309_9_4"]:
    fname = f"../{name}soap.hdf5"
    pcaFname = f"../{name}pca.hdf5"
    applypcaNewFile(fname, pcaFname, pcaMaker, "ico309-SV_18631-SL_31922-T_300")
"""
hdnc = trainNoiseClassifier(
    soapFile="ico309soap.hdf5",
    fitsetAddress="PCAs/ico309-SV_18631-SL_31922-T_300/ico309-SV_18631-SL_31922-T_300",
)
# main NPs
for fname in ["ico309", "dh348_3_2_3", "to309_9_4"]:
    classifyNPs(
        hdnc,
        PCAFile=f"../{fname}pca.hdf5",
        PCAGroupAddr="PCAs/ico309-SV_18631-SL_31922-T_300",
        outFile=f"../{fname}classifications.hdf5",
        whereToSave="Classifications/ico309-SV_18631-SL_31922-T_300",
    )
