from h5py import File
from SOAPify import getReferencesFromDataset, getDistancesFromRefNormalized

# import numpy
from sys import argv

# from multiprocessing import Pool


def loadDictionaries(filename: str):
    references = {}
    with File(filename, "r") as g:
        for k in g.keys():
            references[k] = getReferencesFromDataset(g[k])
    return references


# def calculatedDistancesAndSave(key: str, references: dict, SoapFILE: str):
#    with File(SoapFILE, "r") as workFile:
#        clss = {}
#        SOAPDataset = workFile[f"SOAP/{key}"]
#        for k in references:
#            t = getDistancesFromRefNormalized(SOAPDataset, references[k])
#            clss[f"Distances_{k}"] = t
#        numpy.savez(f"distances-FromTop{classificationName}-mr-{key}.npz", **clss)


if __name__ == "__main__":
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <reference file[I]> <dataset file[IO]>")
    refFile = argv[1]
    SOAPFileName = argv[2]
    references = loadDictionaries(refFile)
    with File(SOAPFileName, "r") as workFile, File(SOAPFileName.replace("soap.hdf5","dists.hdf5"), "a") as distFile:
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
