#%%
from h5py import File
from HDF5er import saveXYZfromTrajGroup, MDA2HDF5
import numpy
from MDAnalysis import Universe as mdaUniverse
from SOAPify import (
    saponifyGroup,
    createReferencesFromTrajectory,
    getReferencesFromDataset,
    mergeReferences,
    SOAPdistanceNormalized,
    saveReferences,
    SOAPReferences,
)
from dataclasses import dataclass
import scipy.cluster.hierarchy as sch

#%%
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
        s_toVEdge111_111=(0, 723),
    ),
    to976_12_4=dict(
        s_toVer=(0, 974),
        s_toVEdge001_111=(0, 970),
        s_toVEdge001_111l=(0, 972),
        s_toVEdge111_111l=(0, 924),
        s_to001=(0, 950),
        s_to001l=(0, 940),
        s_to111=(0, 676),
        s_to111l=(0, 920),
        ss_toVer=(0, 611),
        ss_to001=(0, 258),
        ss_to111=(0, 278),
        b_toFCC_core=(0, 57),
    ),
    dh1086_7_1_3=dict(
        s_dh5Vert=(0, 10),
        s_dhSlimEdgeV=(0, 1071),
        s_dhEdgelv=(0, 50),
        s_dhEdgelc=(0, 798),
        s_dhEdge=(0, 536),
        s_dhSlimEdge=(0, 1068),
        s_dhSlimEdgenv=(0, 1070),
        s_dhSlimEdgel=(0, 1011),
        s_dhConcaveEdge=(0, 925),
        s_dh111=(0, 670),
        ss_dhHCP=(0, 360),
        ss_dhFCC=(0, 669),
        ss_dhFCCnearConcave=(0, 921),
        ss_dhHCPnearConcave=(0, 797),
        b_dhFCC=(0, 399),
        b_dhHCP=(0, 154),
        b_dh5folded=(0, 4),
        v_dhcon=(0, 924),
        #        ev_dhcon=(0, 1018),
        ev_dhcon=(0, 1024),
    ),
    dh1734_5_4_4=dict(
        s_dhconcave=(0, 1130),
        s_dhconcavel=(0, 1132),
        s_dh001=(0, 1643),
        # ev_dhcon=(0, 1542),
        # 1130
        # ev_dhcon1=(0, 1133),
        # ev_dhcon2=(0, 1542),
    ),
)


desiredReferenceOrder = [
    "s_icoVert",  # v_ih_5f
    "s_icoEdge",  # e_ih_(111)
    "s_icoEdgel",  # e_vih_(111)
    "s_ico111",  # s_ih_(111)
    "s_ico111l",  # s_eih_(111)
    "ss_ico5FAxis",  # ss__5f
    "ss_icoFCC",  # ss_ih_FCC
    "ss_icoHCP",  # ss_ih_HCP
    "b_ico5FAxis",  # b_ih_5f
    "b_icoHCP",  # b_ih_HCP
    "b_icoFCC",  # b_ih_FCC
    "b_icoCenter",  # b_ih_c
    #
    "s_toVEdge111_111",  # e_to_(111)
    "s_toVer",  # v_to
    "s_toVEdge001_111",  # e_to_(001)
    "s_toVEdge001_111l",  # e_vto_(001)
    "s_toVEdge111_111l",  # e_vto_(111)
    "s_to001",  # s_to_(001)
    "s_to001l",  # s_eto_(001)
    "s_to111",  # s_to_(111)
    "s_to111l",  # s_eto_(111)
    "ss_toVer",  # ss_to_v
    "ss_to001",  # ss_to_(001)
    "ss_to111",  # ss_to_(111)
    "b_toFCC_core",  # b_to_FCC
    #
    "s_dh5Vert",  # v_dh_5f
    "s_dhSlimEdgeV",  # v__slim
    "s_dhEdgelv",  # e_vdh_(111)
    "s_dhEdgelc",  # e_cdh_(111)
    "s_dhEdge",  # e_dh_(111)
    "s_dhSlimEdge",  # e__slim
    "s_dhSlimEdgenv",  # e_nv_slim
    "s_dhSlimEdgel",  # s_slim_(111)
    "s_dhConcaveEdge",  # v_con_(111)
    "s_dhconcave",  # e__con
    "s_dhconcavel",  # e_v_con
    "v_dhcon",  # v__con
    "ev_dhcon",  # ev__con
    "s_dh111",  # s_dh_(111)
    "s_dh001",  # s_dh_(001)
    "ss_dhHCP",  # ss_dh_HCP
    "ss_dhFCC",  # ss_dh_FCC
    "ss_dhFCCnearConcave",  # ss_con_FCC
    "ss_dhHCPnearConcave",  # ss_con_HCP
    "b_dhFCC",  # b_dh_FCC
    "b_dhHCP",  # b_dh_HCP
    "b_dh5folded",  # b_dh_5f
]


@dataclass
class Names:
    A: str
    B: str = ""
    C: str = " "

    def __call__(self) -> str:
        toret = "{" + self.A + "}"
        if self.B != "":
            toret += "_{\!_{" + self.B + "}}"
        if self.C != "":
            toret += "^{" + self.C + "}"
        return f"${toret}$"


renames = dict(
    s_icoVert=Names("v", "5f", "ih"),
    s_icoEdge=Names("e", "(111)", "ih"),
    s_icoEdgel=Names("e", "(111)", "vih"),
    s_ico111=Names("s", "(111)", "ih"),
    ss_ico5FAxis=Names("ss", "5f"),
    ss_icoFCC=Names("ss", "FCC", "ih"),
    ss_icoHCP=Names("ss", "HCP", "ih"),
    b_ico5FAxis=Names("b", "5f", "ih"),
    b_icoHCP=Names("b", "HCP", "ih"),
    b_icoFCC=Names("b", "FCC", "ih"),
    b_icoCenter=Names("b", "c", "ih"),
    #
    s_toVEdge111_111=Names("e", "(111)", "to"),
    s_toVer=Names("v", "to"),
    s_toVEdge001_111=Names("e", "(001)", "to"),
    s_toVEdge001_111l=Names("e", "(001)", "vth"),
    s_toVEdge111_111l=Names("e", "(111)", "vth"),
    s_to001=Names("s", "(001)", "to"),
    s_to001l=Names("s", "(001)", "e"),
    s_to111=Names("s", "(111)", "ih"),
    s_to111l=Names("s", "(111)", "e"),
    ss_toVer=Names("ss", "v", "to"),
    ss_to001=Names("ss", "(001)", "ih"),
    ss_to111=Names("ss", "(111)", "ih"),
    b_toFCC_core=Names("b", "FCC", "to"),
    #
    s_dh5Vert=Names("v", "5f", "dh"),
    s_dhSlimEdgeV=Names("v", "slim"),
    s_dhEdgelv=Names("e", "(111)", "vdh"),
    s_dhEdgelc=Names("e", "(111)", "cdh"),
    s_dhEdge=Names("e", "(111)", "dh"),
    s_dhSlimEdge=Names("e", "slim"),
    s_dhSlimEdgel=Names("s", "(111)", "slim"),
    s_dhConcaveEdge=Names("v", "con"),
    s_dhconcave=Names("e", "con"),
    s_dhconcavel=Names("e", "con", "v"),
    s_dh111=Names("s", "(111)", "dh"),
    s_dh001=Names("s", "(001)", "dh"),
    ss_dhHCP=Names("ss", "HCP", "dh"),
    ss_dhFCC=Names("ss", "FCC", "dh"),
    ss_dhFCCnearConcave=Names("ss", "FCC", "con"),
    ss_dhHCPnearConcave=Names("ss", "HCP", "con"),
    b_dhFCC=Names("b", "FCC", "dh"),
    b_dhHCP=Names("b", "HCP", "dh"),
    b_dh5folded=Names("b", "5f", "dh"),
)


def referenceDendroMaker(reference, orientation="left"):
    ndataset = len(reference)
    print(ndataset)
    wholeDistances = numpy.zeros((int(ndataset * (ndataset - 1) / 2)))
    cpos = 0
    for i in range(ndataset):
        for j in range(i + 1, ndataset):
            wholeDistances[cpos] = SOAPdistanceNormalized(
                reference.spectra[i], reference.spectra[j]
            )
            cpos += 1
    sch.dendrogram(
        sch.linkage(wholeDistances, method="complete"),
        labels=reference.names,
        orientation=orientation,
    )


#%%

"""
##%%
for NPID in FramesRequest:
    fname = f"{NPID}_minimized.data"
    u = mdaUniverse(fname, atom_style="id type x y z")
    u.atoms.types = ["Au"] * len(u.atoms)
    MDA2HDF5(u, "referenceFrames.hdf5", f"{NPID}", trajChunkSize=1000)

with File("referenceFrames.hdf5", "a") as workFile:
    saponifyGroup(
        trajContainers=workFile["Trajectories"],
        SOAPoutContainers=workFile.require_group("SOAP"),
        SOAPOutputChunkDim=1000,
        SOAPnJobs=32,
        SOAPrcut=4.48023312,
        SOAPnmax=8,
        SOAPlmax=8,
    )

##%%
"""
references = dict()

with File("referenceFrames.hdf5", "r") as workFile:
    for k in FramesRequest:
        references[k] = createReferencesFromTrajectory(
            workFile[f"SOAP/{k}"], FramesRequest[k], 8, 8
        )
# temporary
#%%
dhRefs = mergeReferences(*[references[k] for k in references if "dh" in k])
referenceDendroMaker(mergeReferences(*[references[k] for k in references]), "top")
#%%
with File("References.hdf5", "w") as refFile:
    g = refFile.require_group("NPReferences")
    for k in references:
        saveReferences(g, k, references[k])
#%%

myreferences = dict()

with File("References.hdf5", "r") as refFile:
    g = refFile["NPReferences"]
    for k in g:
        myreferences[k] = getReferencesFromDataset(g[k])

allRefs = mergeReferences(*[myreferences[k] for k in myreferences])
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
icoRefs = mergeReferences(*[myreferences[k] for k in myreferences if "ico" in k])  # OK!
toRefs = mergeReferences(*[myreferences[k] for k in myreferences if "to" in k])  # OK!
#%%
# -3 envs

dhRefs = mergeReferences(*[myreferences[k] for k in myreferences if "dh" in k])


referenceDendroMaker(dhRefs)

#%%
from SOAPify import fillSOAPVectorFromdscribe, normalizeArray

with File("referenceFrames.hdf5", "r") as workFile:
    data1086 = normalizeArray(
        fillSOAPVectorFromdscribe(workFile[f"SOAP/dh1086_7_1_3"][0, :], 8, 8)
    )
    data1734 = normalizeArray(
        fillSOAPVectorFromdscribe(workFile[f"SOAP/dh1734_5_4_4"][0, :], 8, 8)
    )

#%%
t1086 = []
ref = data1086[924]
ref = data1086[1011]
print(SOAPdistanceNormalized(data1086[924], data1086[1011]))
for i in range(1086):
    d = SOAPdistanceNormalized(ref, data1086[i])
    # d2 = SOAPdistanceNormalized(ref2, data1086[i])
    if d < 0.08 and d > 0.005:
        t1086.append((i, d))
print(len(t1086))
#%%
t1734 = []
print(SOAPdistanceNormalized(ref, ref2))
for i in range(1086):
    d = SOAPdistanceNormalized(ref, data1734[i])
    d2 = SOAPdistanceNormalized(ref2, data1734[i])
    if d < 0.08 and d > 0.005 and d < d2:
        t1734.append((i, d))
print(t1734)
#%%
ndataset = len(data1086)
wholeDistances = numpy.zeros((int(ndataset * (ndataset - 1) / 2)))
cpos = 0
for i in range(ndataset):
    for j in range(i + 1, ndataset):
        wholeDistances[cpos] = SOAPdistanceNormalized(data1086[i], data1086[j])
        cpos += 1


sch.dendrogram(
    sch.linkage(wholeDistances, method="complete"),
    # labels=reference.names,
)

#%%
def explor(data):
    t = []
    ndataset = len(data)
    for i in [924]:  # range(ndataset):
        d = SOAPdistanceNormalized(data1086[i], data1086[1011])
        if d < 0.06 and d > 0.0007:
            for j in range(ndataset):
                dd = SOAPdistanceNormalized(data1086[i], data[j])
                dr = SOAPdistanceNormalized(data1086[1011], data[j])
                if dd < d and dd > 0.0022:
                    t.append((i, j, dd))
    print(len(t))
    print(t)


explor(data1734)
#%%
SOAPdistanceNormalized(ref, ref)
