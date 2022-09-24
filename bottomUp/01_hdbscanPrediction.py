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

t1_start = perf_counter()

with h5py.File("ico309soap.hdf5", "r") as fitfile:
    fitset = fitfile[
        "PCAs/ico309-SV_18631-SL_31922-T_300/ico309-SV_18631-SL_31922-T_300"
    ][:, :, :3].reshape(-1, 3)
    hdnc = hdbscanNoiseClassifier(
        fitset, min_cluster_size=125, cluster_selection_method="eom"
    )

t1_stop = perf_counter()
print(f"Time for training: {t1_stop - t1_start} s")
#%%
"""
for fname in ["ico309"]:
    
    print(f"Working on {fname}")
    t1_start = perf_counter()
    with h5py.File(f"{fname}soap.hdf5", "r") as datafile:
        g = datafile["PCAs/ico309-SV_18631-SL_31922-T_300"]
        for i in range(1):
            
            data = g["ico309-SV_18631-SL_31922-T_300"][0:100, :, :3].reshape(-1, 3)

            labels, _ = hdbscan.approximate_predict(hdnc.clusterer, data)
            labelsNoNoise = labels.copy()
            isNoise = labelsNoNoise == -1
            for cluster in hdnc.exemplars:
                break
                print(
                    "cdistRes",
                    cluster,
                    cdist(data[isNoise], hdnc.exemplars[cluster]["points"])
                    .min(axis=-1)
                    .shape,
                    hdnc.exemplars[cluster]["points"].shape,
                )
            
            #print(labels.shape, labelsNoNoise[isNoise].shape)
            tt = hdnc.dist_vector(data[isNoise])
            #print(tt)
            t = hdnc.dist_membership_vector(data[isNoise])
            #print(t.shape, tt.shape)
            labelsNoNoise[isNoise] = numpy.argmax(
                hdnc.dist_membership_vector(data[isNoise]), axis=-1
            )
            print(set(labelsNoNoise))
            print(numpy.argmax(hdnc.dist_membership_vector(data[isNoise]), axis=-1))
            print(hdnc.dist_membership_vector(data[isNoise]))
"""

#%%
for fname in ["ico309", "dh348_3_2_3", "to309_9_4"]:
    print(f"Working on {fname}")
    t1_start = perf_counter()
    with h5py.File(f"{fname}soap.hdf5", "r") as datafile, h5py.File(
        f"{fname}classifications.hdf5", "w"  # this will overwrite!
    ) as classFile:
        g = datafile["PCAs/ico309-SV_18631-SL_31922-T_300"]
        gout = classFile.require_group("Classifications/ico309-SV_18631-SL_31922-T_300")
        for k in g.keys():
            myshape = g[k].shape

            (lbl, strg), mem, lblNN = hdnc.predict(g[k][:, :, :3].reshape(-1, 3))
            labelshape = (myshape[0], myshape[1])
            memshape = (myshape[0], myshape[1], mem.shape[-1])
            resGroup = gout.require_group(k)
            resGroup.create_dataset(
                "labels", shape=labelshape, dtype=int, data=lbl.reshape(labelshape)
            )
            resGroup.create_dataset(
                "labelsStrength",
                shape=labelshape,
                dtype=int,
                data=strg.reshape(labelshape),
            )
            resGroup.create_dataset(
                "labelsNN", shape=labelshape, dtype=int, data=lblNN.reshape(labelshape)
            )
            resGroup.create_dataset(
                "memberships", shape=memshape, dtype=int, data=mem.reshape(memshape)
            )
    t1_stop = perf_counter()
    print(f"Time for {fname}: {t1_stop - t1_start} s")
