from h5py import File
from referenceMaker import getDefaultReferences, getDefaultReferencesSubdict
from SOAPify import getDistancesFromRefNormalized


def calculatedDistancesAndSave(references, SOAPFileName, classificationFile):

    with File(
        SOAPFileName, "r" if SOAPFileName != classificationFile else "a"
    ) as workFile, File(classificationFile, "a") as distFile:
        g = workFile[f"SOAP"]
        distG = distFile.require_group("Distances")
        for key in g.keys():
            for refKey in references:
                t = getDistancesFromRefNormalized(g[key], references[refKey])
                dgd = distG.require_dataset(
                    f"{refKey}/{key}", shape=t.shape, dtype=t.dtype, chunks=True
                )
                dgd[:] = t
                dgd.attrs["Reference"] = f"{refFile}/{refKey}"
                dgd.attrs["names"] = references[refKey].names


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
        SOAPFileName = f"../bottomUp/{NPname}soap.hdf5"
        classificationFile = f"{NPname}TopBottom.hdf5"
        calculatedDistancesAndSave(references, SOAPFileName, classificationFile)
    calculatedDistancesAndSave(
        references, "referenceFrames.hdf5", "referenceFrames.hdf5"
    )
    calculatedDistancesAndSave(references, "../minimized.hdf5", "../minimized.hdf5")
