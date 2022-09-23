from SOAPify import saponifyGroup
import h5py

def worker(trajFileName: str) -> None:
    soapFileName = trajFileName.split(".")[0] + "soap.hdf5"
    print(trajFileName, soapFileName)
    with h5py.File(trajFileName, "r") as workFile, h5py.File(
        soapFileName, "a"
    ) as soapFile:
        saponifyGroup(
            trajContainers=workFile["Trajectories"],
            SOAPoutContainers=soapFile.require_group("SOAP"),
            SOAPOutputChunkDim=1000,
            SOAPnJobs=32,
            SOAPrcut=4.48023312,
            SOAPnmax=8,
            SOAPlmax=8,
        )


if __name__ == "__main__":
    from sys import argv
    worker(argv[1])
