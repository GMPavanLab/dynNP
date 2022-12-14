#%%
from scipy.spatial.distance import cdist
import hdbscan, numpy, h5py
from time import perf_counter


class hdbscanNoiseClassifier:
    def __init__(self, fitset, **hdbscanArgs):
        self.__fitset = fitset
        self.__clusterer = hdbscan.HDBSCAN(**hdbscanArgs).fit(self.__fitset)
        self.__clusterer.generate_prediction_data()

    @property
    def fitset(self):
        return self.__fitset

    @property
    def clusterer(self):
        return self.__clusterer

    @property
    def exemplars(self):
        if not hasattr(self, "__exemplars"):
            tree = self.__clusterer.condensed_tree_
            raw_tree = tree._raw_tree
            cluster_tree = raw_tree[raw_tree["child_size"] > 1]
            self.__exemplars = dict()
            for i, cluster_id in enumerate(tree._select_clusters()):
                # Get the leaf cluster nodes under the cluster we are considering
                leaves = hdbscan.plots._recurse_leaf_dfs(cluster_tree, cluster_id)
                # Now collect up the last remaining points of each leaf cluster (the heart of the leaf)
                result = numpy.array([])
                for leaf in leaves:
                    max_lambda = raw_tree["lambda_val"][
                        raw_tree["parent"] == leaf
                    ].max()
                    points = raw_tree["child"][
                        (raw_tree["parent"] == leaf)
                        & (raw_tree["lambda_val"] == max_lambda)
                    ]
                    result = numpy.hstack((result, points))
                self.__exemplars[i] = dict(
                    points=self.fitset[result.astype(int)],
                    ids=self.fitset[result.astype(int)],
                )
        return self.__exemplars

    def min_dist_to_exemplar(self, point, clusterID):
        dists = cdist([point], self.exemplars[clusterID]["points"])
        return dists.min()

    def dist_vector(self, points):
        result = numpy.zeros((points.shape[0], len(self.exemplars)), dtype=numpy.double)
        for cluster in self.exemplars:
            result[:, cluster] = cdist(points, self.exemplars[cluster]["points"]).min(
                axis=-1
            )
        return result

    def dist_membership_vector(self, point, softmax=False):
        if softmax:
            result = numpy.exp(1.0 / self.dist_vector(point))
            result[~numpy.isfinite(result)] = numpy.finfo(numpy.double).max
        else:
            result = 1.0 / self.dist_vector(point)
            result[~numpy.isfinite(result)] = numpy.finfo(numpy.double).max
        result /= result.sum()
        return result

    def predict(self, data):
        labels, strenghts = hdbscan.approximate_predict(self.__clusterer, data)
        membership_vector = hdbscan.membership_vector(self.__clusterer, data)
        labelsNoNoise = labels.copy()
        isNoise = labelsNoNoise == -1

        labelsNoNoise[isNoise] = numpy.argmax(
            self.dist_membership_vector(data[isNoise]), axis=-1
        )
        return (labels, strenghts), membership_vector, labelsNoNoise


#%%
def trainNoiseClassifier(
    soapFile: str, fitsetAddress: str, fitSetSlice: slice = slice(None)
):
    print(f"Training HDBSCAN*")
    t1_start = perf_counter()

    with h5py.File(soapFile, "r") as fitfile:
        fitset = fitfile[fitsetAddress][fitSetSlice, :, :3].reshape(-1, 3)
        hdnc = hdbscanNoiseClassifier(
            fitset, min_cluster_size=125, cluster_selection_method="eom"
        )

    t1_stop = perf_counter()
    print(f"Time for training: {t1_stop - t1_start} s")
    return hdnc


#%% main NPs


def classifyNPs(
    hdnc: hdbscanNoiseClassifier,
    soapFile: str,
    PCAGroupAddr: str,
    outFile: str,
    whereToSave: str,
):
    """_summary_

    Args:
        hdnc (hdbscanNoiseClassifier): _description_
        soapFile (str): _description_
        PCAGroupAddr (str): _description_
        outFile (str): _description_
        whereToSave (str): _description_
    """
    print(f"Working on {soapFile} and saving on on {outFile}")
    t1_start = perf_counter()
    with h5py.File(soapFile, "r") as datafile:
        g = datafile[PCAGroupAddr]
        for k in g.keys():
            print(f"Applying prediction to trajectory {k}")
            myshape = g[k].shape
            labelshape = (myshape[0], myshape[1])
            memshape = (
                myshape[0],
                myshape[1],
                len(hdnc.clusterer.condensed_tree_._select_clusters()),
            )
            with h5py.File(outFile, "a") as classFile:
                gout = classFile.require_group(whereToSave)
                resGroup = gout.require_group(k)
                labels = resGroup.require_dataset(
                    "labels",
                    shape=labelshape,
                    dtype=numpy.int32,
                    chunks=True
                    # data=lbl.reshape(labelshape),
                )
                labelsStrength = resGroup.require_dataset(
                    "labelsStrength",
                    shape=labelshape,
                    dtype=numpy.float32,
                    chunks=True
                    # data=strg.reshape(labelshape),
                )
                labelsNN = resGroup.require_dataset(
                    "labelsNN",
                    shape=labelshape,
                    dtype=numpy.int32,
                    chunks=True
                    # data=lblNN.reshape(labelshape),
                )
                memberships = resGroup.require_dataset(
                    "memberships",
                    shape=memshape,
                    dtype=numpy.float64,
                    chunks=True
                    # data=mem.reshape(memshape),
                )
                for chunk in g[k].iter_chunks():
                    framesChunk = chunk[0]
                    print(f"classifying frames {framesChunk}")
                    (lbl, strg), mem, lblNN = hdnc.predict(
                        # g[k][framesChunk, :, :3].reshape(-1, 3)
                        g[k][(framesChunk, slice(None), slice(0, 3, 1))].reshape(-1, 3)
                    )
                    nframes = lbl.reshape(-1, myshape[1]).shape[0]
                    labels[framesChunk] = lbl.reshape(nframes, myshape[1])
                    labelsStrength[framesChunk] = strg.reshape(nframes, myshape[1])
                    labelsNN[framesChunk] = lblNN.reshape(nframes, myshape[1])
                    memberships[framesChunk] = mem.reshape(nframes, myshape[1], -1)
    t1_stop = perf_counter()
    print(f"Time for {soapFile} -> {outFile}: {t1_stop - t1_start} s")


#%% minimized NPs
# TODO: unify this with the function up this
def classifyMinimizedNPs(hdnc: hdbscanNoiseClassifier):
    for fname in ["ico309", "dh348_3_2_3", "to309_9_4"]:
        print(f"Working on {fname}")
        t1_start = perf_counter()
        with h5py.File(f"../minimized.hdf5", "a") as datafile:
            g = datafile["PCAs/ico309-SV_18631-SL_31922-T_300"]
            gout = datafile.require_group(
                "Classifications/ico309-SV_18631-SL_31922-T_300"
            )
            for k in g.keys():
                myshape = g[k].shape

                (lbl, strg), mem, lblNN = hdnc.predict(g[k][:, :, :3].reshape(-1, 3))
                labelshape = (myshape[0], myshape[1])
                memshape = (myshape[0], myshape[1], mem.shape[-1])
                resGroup = gout.require_group(k)
                resGroup.require_dataset(
                    "labels",
                    shape=labelshape,
                    dtype=numpy.int32,
                    data=lbl.reshape(labelshape),
                )
                resGroup.require_dataset(
                    "labelsStrength",
                    shape=labelshape,
                    dtype=numpy.float32,
                    data=strg.reshape(labelshape),
                )
                resGroup.require_dataset(
                    "labelsNN",
                    shape=labelshape,
                    dtype=numpy.int32,
                    data=lblNN.reshape(labelshape),
                )
                resGroup.require_dataset(
                    "memberships",
                    shape=memshape,
                    dtype=numpy.float64,
                    data=mem.reshape(memshape),
                )
        t1_stop = perf_counter()
        print(f"Time for {fname}: {t1_stop - t1_start} s")


# %%
from matplotlib import pyplot as plt


def exemplarPlot3D(
    nc: hdbscanNoiseClassifier,
    x=0,
    y=1,
    z=2,
    ax: plt.Axes = None,
    colors: list = None,
    plotFiteSet=True,
    scatterOptions: dict = {},
):
    if ax is None:
        ax = plt.figure().add_subplot(projection="3d")
    if plotFiteSet:
        fs = nc.fitset
        ax.scatter(fs[:, x], fs[:, y], fs[:, z], c="gray", alpha=0.01, s=0.1)
    scatterOpt = dict(marker="x")
    scatterOpt.update(scatterOptions)
    for cluster in nc.exemplars:
        if colors:
            scatterOpt.update(dict(color=colors[cluster]))
        t = nc.exemplars[cluster]["points"]
        ax.scatter(t[:, x], t[:, y], t[:, z], **scatterOpt)



def exemplarPlot(
    nc: hdbscanNoiseClassifier,
    x: int = 0,
    y: int = 1,
    ax: plt.Axes = None,
    colors: list = None,  # the colors of the clusters
    plotFiteSet=True,
    scatterOptions: dict = {},#optional option to pass to the scatterplot of the exemplars
):
    if ax is None:
        ax: plt.Axes = plt.gca()

    if plotFiteSet:
        fs = nc.fitset
        ax.scatter(fs[:, x], fs[:, y], c="gray", alpha=0.01, s=0.1)
    scatterOpt = dict(marker="x")
    scatterOpt.update(scatterOptions)
    for cluster in nc.exemplars:
        if colors:
            scatterOpt.update(dict(color=colors[cluster]))
        t = nc.exemplars[cluster]["points"]
        ax.scatter(t[:, x], t[:, y], **scatterOpt)



#%%
if __name__ == "__main__":

    hdnc = trainNoiseClassifier(
        soapFile="ico309soap.hdf5",
        fitsetAddress="PCAs/ico309-SV_18631-SL_31922-T_300/ico309-SV_18631-SL_31922-T_300",
    )
    # main NPs
    for fname in ["ico309", "dh348_3_2_3", "to309_9_4"]:
        classifyNPs(
            hdnc,
            soapFile=f"{fname}soap.hdf5",
            PCAGroupAddr="PCAs/ico309-SV_18631-SL_31922-T_300",
            outFile=f"{fname}classifications.hdf5",
            whereToSave="Classifications/ico309-SV_18631-SL_31922-T_300",
        )

    # minimized NPs
    classifyMinimizedNPs(hdnc)
