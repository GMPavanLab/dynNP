from MDAnalysis import Universe as mdaUniverse
from MDAnalysis import transformations
from HDF5er import MDA2HDF5
from os import path
import re


def worker(completefilename: str, ff: str, ts: str, frames="100ps"):
    filename=path.basename(completefilename)
    name = getName(filename)
    trajname = filename.split(".")[0]
    topo = name + ".data"
    args = createArgs(filename)
    args["frames"] = frames
    args["ts"] = ts
    args["ForceField"] = ff
    print(f"from trajectory {filename} and topology {topo} creating a new trajectory in")
    print(f'"{name}.hdf5/Trajectories/{trajname}"')
    print(f"parameters:", args)
    u = mdaUniverse(topo, completefilename, atom_style="id type x y z")
    u.atoms.types = ["Au"] * len(u.atoms)
    
    MDA2HDF5(u, name + ".hdf5", trajname, trajChunkSize=1000, attrs=args,trajslice=slice(10000,None,10))
    # ref=u.select_atoms("index 0:1")
    ref = mdaUniverse(topo, atom_style="id type x y z")
    u.trajectory.add_transformations(transformations.fit_rot_trans(u, ref))
    MDA2HDF5(u, name + "_fitted.hdf5", f"{trajname}_fitted", trajChunkSize=1000,trajslice=slice(10000,None,10))


getT = re.compile("T_([0-9]*)")
getSV = re.compile("SV_([0-9]*)")
getSL = re.compile("SL_([0-9]*)")
getTopo = re.compile("(ico[0-9_]*|dh[0-9_]*|to[0-9_]*)")


def createArgs(filename: str):
    T = getT.search(filename).group(1)
    SV = getSV.search(filename).group(1)
    SL = getSL.search(filename).group(1)
    return dict(T=T, SL=SL, SV=SV)


def getName(filename: str):
    topo = getTopo.search(filename).group(1)
    return topo


if __name__ == "__main__":
    from sys import argv
    dumps = argv[1:]
    ts = "5fs"
    ff = "SMATB"
    for d in dumps:
        worker(d, ff, ts)
