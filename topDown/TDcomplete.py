from TD00_referenceMaker import getDefaultReferences, getDefaultReferencesSubdict
from TD01_calculateDistancesFromReferences import calculatedDistancesAndSave
from TD02_elaborateDistances import elaborateDistancesAndSave

if __name__ == "__main__":
    references = {k: getDefaultReferencesSubdict(k) for k in ["ih", "to", "dh"]}
    references["icotodh"] = getDefaultReferences()

    refFile = "References.hdf5"
    for NPname in ["ico309", "dh348_3_2_3", "to309_9_4"]:
        SOAPFileName = f"../{NPname}soap.hdf5"
        classificationFile = f"../{NPname}TopBottom.hdf5"
        calculatedDistancesAndSave(
            references, SOAPFileName, classificationFile, refFile="References.hdf5"
        )
        elaborateDistancesAndSave(classificationFile)
    calculatedDistancesAndSave(
        references,
        "referenceFrames.hdf5",
        "referenceFrames.hdf5",
        refFile="References.hdf5",
    )
    elaborateDistancesAndSave("referenceFrames.hdf5")
    calculatedDistancesAndSave(
        references,
        "../minimized.hdf5",
        "../minimized.hdf5",
        refFile="References.hdf5",
    )
    elaborateDistancesAndSave("../minimized.hdf5")
