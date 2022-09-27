from MDAnalysis import Universe as mdaUniverse
import h5py
from HDF5er import MDA2HDF5
from SOAPify import saponifyGroup
from os import path


def worker(completefilename: str):
    filename = path.basename(completefilename)
    trajname = filename.split(".")[0]
    topo = trajname + ".data"

    print(f"from topology {topo} creating a new trajectory in")
    print(f'"minimized.hdf5/Trajectories/{trajname}"')
    u = mdaUniverse(topo, completefilename, atom_style="id type x y z")
    u.atoms.types = ["Au"] * len(u.atoms)

    MDA2HDF5(u, "minimized.hdf5", trajname, trajChunkSize=1)


def doSoap(trajFileName: str) -> None:
    soapFileName = trajFileName.split(".")[0] + "soap.hdf5"
    print(trajFileName, soapFileName)
    with h5py.File(trajFileName, "a") as workFile:
        saponifyGroup(
            trajContainers=workFile["Trajectories"],
            SOAPoutContainers=workFile.require_group("SOAP"),
            SOAPOutputChunkDim=1000,
            SOAPnJobs=32,
            SOAPrcut=4.48023312,
            SOAPnmax=8,
            SOAPlmax=8,
        )


if __name__ == "__main__":
    from sys import argv

    topos = argv[1:]
    ts = "5fs"
    ff = "SMATB"
    for d in topos:
        worker(d)
    doSoap("minimized.hdf5")
