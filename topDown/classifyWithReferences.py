from msilib.schema import File
from h5py import File
from referenceMaker import getDefaultReferences
from SOAPify import getDistancesFromRefNormalized

if __name__ == "__main__":
    references = getDefaultReferences()
    refFile = "References.hdf5"
    for NPname in ["ico309","dh348_3_2_3","to309_9_4"]:
        SOAPFileName = f"../{NPname}.hdf5"
        with File(SOAPFileName, "r") as workFile, File(
            SOAPFileName.replace("soap.hdf5", "dists.hdf5"), "a"
        ) as distFile:
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
