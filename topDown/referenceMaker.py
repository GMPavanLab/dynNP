#%%
from operator import index
from h5py import File
from HDF5er import saveXYZfromTrajGroup, MDA2HDF5
import numpy
from MDAnalysis import Universe as mdaUniverse
from SOAPify import (
    saponifyGroup,
    createReferencesFromTrajectory,
    mergeReferences,
    SOAPdistanceNormalized,
    saveReferences,
    SOAPReferences,
)

FramesRequest = dict(
    ico923_6=dict(
        s_icoVert=(0, 566),
        s_icoEdge=(0, 830),
        s_icoEdgel=(0, 828),
        s_ico111=(0, 892),
        s_ico111l=(0, 893),
        ss_ico5FAxis=(0, 312),
        ss_icoFCC=(0, 524),
        ss_icoHCP=(0, 431),
        b_ico5FAxis=(0, 1),
        b_icoHCP=(0, 45),
        b_icoFCC=(0, 127),
        b_icoCenter=(0, 0),
    ),
    to807_11_3=dict(
        s_thVEdge111_111=(0, 723),
    ),
    to976_12_4=dict(
        s_thVer=(0, 974),
        s_thVEdge001_111=(0, 970),
        s_thVEdge001_111l=(0, 972),
        s_thVEdge111_111l=(0, 924),
        s_th001=(0, 950),
        s_th001l=(0, 940),
        s_th111=(0, 676),
        s_th111l=(0, 920),
        ss_thVer=(0, 611),
        ss_th001=(0, 258),
        ss_th111=(0, 278),
        b_thFCC_core=(0, 57),
    ),
    dh1086_7_1_3=dict(
        s_dh5Vert=(0, 10),
        s_dhSlimEdgeV=(0, 1071),
        s_dhEdgelv=(0, 50),
        s_dhEdgelc=(0, 798),
        s_dhEdge=(0, 536),
        s_dhSlimEdge=(0, 1068),
        s_dhSlimEdgel=(0, 1027),
        s_dhConcaveEdge=(0, 925),
        s_dh111=(0, 670),
        ss_dhHCP=(0, 360),
        ss_dhFCC=(0, 669),
        ss_dhFCCnearConcave=(0, 921),
        ss_dhHCPnearConcave=(0, 797),
        b_dhFCC=(0, 399),
        b_dhHCP=(0, 154),
        b_dh5folded=(0, 4),
    ),
    dh1734_5_4_4=dict(
        s_dhconcave=(0, 1130),
        s_dhconcavel=(0, 1132),
        s_dh001=(0, 1643),
    ),
)


desiredReferenceOrder = [
    "s_icoVert",
    "s_icoEdge",
    "s_icoEdgel",
    "s_ico111",
    "s_ico111l",
    "ss_ico5FAxis",
    "ss_icoFCC",
    "ss_icoHCP",
    "b_ico5FAxis",
    "b_icoHCP",
    "b_icoFCC",
    "b_icoCenter",
    "s_thVEdge111_111",
    "s_thVer",
    "s_thVEdge001_111",
    "s_thVEdge001_111l",
    "s_thVEdge111_111l",
    "s_th001",
    "s_th001l",
    "s_th111",
    "s_th111l",
    "ss_thVer",
    "ss_th001",
    "ss_th111",
    "b_thFCC_core",
    "s_dh5Vert",
    "s_dhSlimEdgeV",
    "s_dhEdgelv",
    "s_dhEdgelc",
    "s_dhEdge",
    "s_dhSlimEdge",
    "s_dhSlimEdgel",
    "s_dhConcaveEdge",
    "s_dhconcave",
    "s_dhconcavel",
    "s_dh111",
    "s_dh001",
    "ss_dhHCP",
    "ss_dhFCC",
    "ss_dhFCCnearConcave",
    "ss_dhHCPnearConcave",
    "b_dhFCC",
    "b_dhHCP",
    "b_dh5folded",
]


#%%
for NPID in FramesRequest:
    fname = f"{NPID}_minimized.data"
    u = mdaUniverse(fname, atom_style="id type x y z")
    u.atoms.types = ["Au"] * len(u.atoms)
    MDA2HDF5(u, "references.hdf5", f"{NPID}", trajChunkSize=1000)

with File("references.hdf5", "a") as workFile:
    saponifyGroup(
        trajContainers=workFile["Trajectories"],
        SOAPoutContainers=workFile.require_group("SOAP"),
        SOAPOutputChunkDim=1000,
        SOAPnJobs=32,
        SOAPrcut=4.48023312,
        SOAPnmax=8,
        SOAPlmax=8,
    )


references = dict()

with File("references.hdf5", "r") as workFile:
    for k in FramesRequest:
        references[k] = createReferencesFromTrajectory(
            workFile[f"SOAP/{k}"], FramesRequest[k], 8, 8
        )

#%%
allRefs = mergeReferences(*[references[k] for k in references])
#%% reoredering references


idx = numpy.zeros((len(allRefs.names)), dtype=int)
for i, k in enumerate(desiredReferenceOrder):
    idx[i] = allRefs.names.index(k)

reorderedReferences = SOAPReferences(
    names=desiredReferenceOrder,
    spectra=allRefs.spectra[idx],
    lmax=allRefs.lmax,
    nmax=allRefs.nmax,
)


#%%
with File("References.hdf5", "w") as refFile:
    g = refFile.require_group("NPReferences")
    for k in references:
        saveReferences(g, k, references[k])
#%%
import scipy.cluster.hierarchy as sch


def referenceDendroMaker(reference):
    ndataset = len(reference)
    wholeDistances = numpy.zeros((int(ndataset * (ndataset - 1) / 2)))
    cpos = 0
    for i in range(ndataset):
        for j in range(i + 1, ndataset):
            wholeDistances[cpos] = SOAPdistanceNormalized(
                reference.spectra[i], reference.spectra[j]
            )
            cpos += 1
    sch.dendrogram(sch.linkage(wholeDistances, method="complete"))


#%%
icoRefs = mergeReferences(*[references[k] for k in references if "ico" in k])  # OK!
toRefs = mergeReferences(*[references[k] for k in references if "to" in k])
dhRefs = mergeReferences(*[references[k] for k in references if "dh" in k])
#%%
referenceDendroMaker(toRefs)
