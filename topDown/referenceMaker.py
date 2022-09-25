from h5py import File
from HDF5er import saveXYZfromTrajGroup,MDA2HDF5,saveXYZfromTrajGroup
import numpy
from MDAnalysis import Universe as mdaUniverse
from SOAPify import (saponifyGroup, 
                    createReferencesFromTrajectory,
                    mergeReferences,
                    SOAPdistanceNormalized,
                    saveReferences,
                    )