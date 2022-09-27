#%%
import matplotlib.pyplot as plt
import numpy
import figureSupportModule as fsm
from matplotlib.image import imread
import h5py
import re
reT=re.compile("T_([0-9]*)")
def getT(s):
    return reT.search(s).group(1)
    
#%% Loading Data
for NPname in ["dh348_3_2_3", "to309_9_4"]:
    classificationFile = f"../topDown/{NPname}TopBottom.hdf5"
    with h5py.File(classificationFile, "r") as distFile:
        ClassG = distFile["Classifications/icotodh"]
        for k in ClassG:
            if NPname in k:
                T=getT(k)
                


#%%
figsize = numpy.array([4, 3]) * 3
fig, axes = fsm.makeLayout6and7(figsize, dpi=300)
