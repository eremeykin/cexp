import numpy as np
from generators.kovaleva import kovaleva
from optparse import OptionParser

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--seed", dest="seed", type="int", help="generator seed")
    parser.add_option("--cardinality", dest="cardinality", type="int", help="min cardinality of any cluster")
    parser.add_option("--n_clusters", dest="n_clusters", type="int", help="number of clusters in dataset")
    parser.add_option("--features", dest="features", type="int", help="number of features")
    parser.add_option("--n_objects", dest="n_objects", type="int", help="number of objects")
    parser.add_option("--a", dest="a", type="float", help="'a' box parameter of Kovaleva generator")
    parser.add_option("--folder", dest="folder", type="str", help="folder where to save")
    parser.add_option("--basename", dest="basename", type="str", help="base name of file")

    options, args = parser.parse_args()
    seed = options.seed
    cardinality = options.cardinality
    n_clusters = options.n_clusters
    features = options.features
    n_objects = options.n_objects
    a = options.a
    folder = options.folder.strip("/")
    base_name = options.basename

    np.random.seed(seed)
    assert n_objects >= cardinality * n_clusters
    data, labels = kovaleva(cardinality, n_clusters, (n_objects, features), a)
    name = "{}_{n_obj}x{features}_c{n_cls}_m{card}_a{a}_s{seed}".format(base_name,
                                                                        n_obj=n_objects,
                                                                        features=features,
                                                                        n_cls=n_clusters,
                                                                        card=cardinality,
                                                                        a=a,
                                                                        seed=seed)
    pts_name = name + ".pts"
    lbs_name = name + ".lbs"
    pts_path = "/".join([folder, pts_name])
    lbs_path = "/".join([folder, lbs_name])

    np.savetxt(pts_path, data, delimiter=',', comments='',
               header=','.join(['F' + str(i) for i in range(data.shape[1])]))
    np.savetxt(lbs_path, labels, delimiter=',', comments='',
               header=','.join(['F' + str(i) for i in range(data.shape[1])]))

