from scipy.spatial.distance import cdist
import hdbscan, numpy, h5py


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

    def dist_vector(self, point):
        result = {}
        for cluster in self.exemplars:
            result[cluster] = cdist([point], self.exemplars[cluster]["points"]).min()
        return numpy.array(list(result.values()))

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
        for j, (p, l) in enumerate(zip(data, labelsNoNoise)):
            if l == -1:
                labelsNoNoise[j] = numpy.argmax(self.dist_membership_vector(p))
        return (labels, strenghts), membership_vector, labelsNoNoise


#%%
# _, _, lbl = hdnc.predict(pca)


with h5py.File("ico309soap.hdf5", "r") as fitfile:
    fitset = fitfile[
        "PCAs/ico309-SV_18631-SL_31922-T_300/ico309-SV_18631-SL_31922-T_300"
    ][:, :, :3].reshape(-1, 3)
    hdnc = hdbscanNoiseClassifier(
        fitset, min_cluster_size=125, cluster_selection_method="eom"
    )


for fname in ["dh348_3_2_3", "ico309", "to309_9_4"]:
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
                "labelsStrength", shape=memshape, dtype=int, data=strg.reshape(memshape)
            )
            resGroup.create_dataset(
                "labelsNN", shape=labelshape, dtype=int, data=lblNN.reshape(labelshape)
            )
            resGroup.create_dataset(
                "memberships", shape=memshape, dtype=int, data=mem.reshape(memshape)
            )
