from h5py import File
from referenceMaker import getDefaultReferences, getDefaultReferencesSubdict
from SOAPify import getDistancesFromRefNormalized
import numpy


def elaborateDistancesAndSave(classificationFile):
    with File(classificationFile, "a") as distFile:
        distG = distFile[f"Distances"]
        newClassG = distFile.require_group("Classifications")
        for refKey in distG.keys():
            for key in distG[refKey]:
                dgd = distG[f"{refKey}/{key}"][:]
                classification = numpy.argmin(dgd, axis=-1)
                print(dgd.shape, " -> ", classification.shape)
                classDS = newClassG.require_dataset(
                    f"{refKey}/{key}",
                    shape=classification.shape,
                    dtype=classification.dtype,
                    chunks=True,
                )
                classDS[:] = classification
                classDS.attrs["Reference"] = distG[f"{refKey}/{key}"].attrs["Reference"]
                classDS.attrs["names"] = distG[f"{refKey}/{key}"].attrs["names"]

    # with File(SOAPFileName, "r") as workFile:
    #    g=workFile[f"SOAP"]
    #    for key in g.keys():
    #        t.append((key,references,SOAPFileName))
    # with Pool(processes=len(t)) as p:
    #    p.starmap(calculatedDistancesAndSave,t)


if __name__ == "__main__":
    references = {k: getDefaultReferencesSubdict(k) for k in ["ih", "to", "dh"]}
    references["icotodh"] = getDefaultReferences()

    refFile = "References.hdf5"
    for NPname in ["ico309", "dh348_3_2_3", "to309_9_4"]:
        classificationFile = f"{NPname}TopBottom.hdf5"
        elaborateDistancesAndSave(classificationFile)

    elaborateDistancesAndSave("referenceFrames.hdf5")
    elaborateDistancesAndSave("../minimized.hdf5")
