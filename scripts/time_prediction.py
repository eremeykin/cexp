from generators.kovaleva import kovaleva
import time as timer
import numpy as np
from clustering.agglomerative.pattern_initialization.ap_init import APInit
from clustering.agglomerative.ik_means.ik_means import IKMeans
from clustering.agglomerative.a_ward import AWard


def generate(n_objects, n_clusters=None, cardinality=None, features=None, a=0.5):
    seed = 45634
    if n_clusters is None:
        n_clusters = int(19 * n_objects / 1000)
    if features is None:
        features = int(8 * n_objects / 1000)
    if cardinality is None:
        cardinality = int(0.75 * n_objects / n_clusters)
    assert n_objects >= cardinality * n_clusters
    np.random.seed(seed)
    data, labels = kovaleva(cardinality, n_clusters, (n_objects, features), a)
    return data, n_clusters


def award_single_run(data, k_star, alpha=None, threshold=1):
    start = timer.time()
    run_ap_init = APInit(data, threshold)
    run_ap_init()
    end_init = timer.time()
    run_ik_means = IKMeans(run_ap_init.cluster_structure)
    run_ik_means()
    end_kmeans = timer.time()
    cs = run_ik_means.cluster_structure
    run_a_ward = AWard(cs, k_star, alpha)
    result = run_a_ward()
    end = timer.time()
    return end - start, end_init - start, end_kmeans - end_init, end - end_kmeans


def time_trial(n):
    data, k_star = generate(n)
    # start = timer.time()
    time, time_init, time_kmeans, time_ward = award_single_run(data, k_star)
    # end = timer.time()
    return time, time_init, time_kmeans, time_ward


if __name__ == "__main__":
    n0 = 125
    # prev = time_trial(n0)
    prev, prev_init, prev_kmeans, prev_ward = time_trial(n0)
    for f in range(2, 32):
        n = n0 * (2 ** f)
        time, time_init, time_kmeans, time_ward = time_trial(n)
        print("{:6d}\t{:10.2f},{:<10.2f}\t{:10.2f},{:<10.2f}\t{:10.2f},{:<10.2f}\t{:10.2f},{:<10.2f}".format(n, time,
                                                                                                             time / prev,
                                                                                                             time_init,
                                                                                                             time_init / prev_init,
                                                                                                             time_kmeans,
                                                                                                             time_kmeans / prev_kmeans,
                                                                                                             time_ward,
                                                                                                             time_ward / prev_ward))
        prev, prev_init, prev_kmeans, prev_ward = time, time_init, time_kmeans, time_ward
