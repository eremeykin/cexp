import pickle
import tabulate
from optparse import OptionParser
from scripts.dumper import UnDumper
from scripts.daemon import single_run
from sklearn.metrics import adjusted_rand_score as ari
import numpy as np
import pandas as pd
from scripts.utils import *
from time import time
from pprint import pprint


def max(matrix):
    rows, cols = matrix.shape
    row = np.argmax(matrix) // cols
    col = np.argmax(matrix) - row * cols
    return row, col


def convert_p_beta(row):
    # swap because sw is matrix and
    # row -- zero [0] -- y -- beta
    # col -- first [1] -- x -- p
    return np.array([col_to_p(row[1]), row_to_beta(row[0])])


def pick_best(sw_matrix, strategy, eps=0.000001):
    max_indices = np.argwhere(sw_matrix > np.amax(sw_matrix) - eps)
    max_indices = np.apply_along_axis(convert_p_beta, 1, max_indices)

    if strategy == "first":
        distances = np.sum(max_indices ** 2, 1)
        max_index = max_indices[np.argmin(distances)]
        p, beta = max_index[0], max_index[1]
        # print("p={}, beta={}".format(p, beta))
        return p, beta
    elif strategy == "mean":
        p_m, beta_m = np.mean(max_indices, axis=0)
        return round(p_m), round(beta_m)
    elif strategy == "mean_s":
        raise RuntimeError()
    elif strategy == "mean*":
        p_m, beta_m = np.mean(max_indices, axis=0)
        p_best, beta_best = max_indices[0]
        current_min = (p_best - p_m) ** 2 + (beta_best - beta_m) ** 2
        for p_beta in max_indices:
            p_current, beta_current = p_beta
            new_min = (p_current - p_m) ** 2 + (beta_current - beta_m) ** 2
            if new_min < current_min:
                current_min = new_min
                p_best, beta_best = p_current, beta_current
        return p_best, beta_best
    raise RuntimeError()


def calculate_ari(p, beta, dataset):
    start = time()
    dataset = ".".join([get_basename(dataset), "pts"])
    data_file = "/".join([data_directory, dataset])
    k_star = get_k_star(dataset)
    algorithm, t1, t2, t3, labels, cluster_structure = single_run(data_file, p, beta, k_star)
    labels_file = ".".join([cut_extention(data_file), "lbs"])
    labels_true = pd.read_csv(labels_file).as_matrix().astype(int).flatten()
    assert len(labels_true) == 1000
    ari_value = ari(labels_true=labels_true, labels_pred=labels)
    end = time()
    print("calculate ARI = {} in {:5.2f} sec".format(ari_value, end - start))
    return ari_value


def get_aris(results, base_dataset, algorithm, strategy):
    full_datasets = [ds for ds in results.keys() if ds.startswith(base_dataset)]

    rc100_datasets = dict()
    for fds in full_datasets:
        rc100_datasets[fds] = [ds for ds in results.keys() if ds.startswith("rc_ch100") and cut_extention(fds) in ds]

    rc200_datasets = dict()
    for fds in full_datasets:
        rc200_datasets[fds] = [ds for ds in results.keys() if ds.startswith("rc_ch200") and cut_extention(fds) in ds]

    if algorithm == "1-1000":
        aris = []
        for fds in full_datasets:
            sw_matrix = results[fds]
            p, beta = pick_best(sw_matrix, strategy=strategy)
            aris.append(calculate_ari(p, beta, fds))
        assert len(aris) == 10
        return aris
    if algorithm == "1-100":
        aris = []
        for fds in full_datasets:
            one_rc100_dataset = min(rc100_datasets[fds], key=lambda ds: get_rc_seed(ds))
            sw_matrix = results[one_rc100_dataset]
            p, beta = pick_best(sw_matrix, strategy=strategy)
            aris.append(calculate_ari(p, beta, fds))
        assert len(aris) == 10
        return aris
    if algorithm == "5-100":
        aris = []
        for fds in full_datasets:
            ps, betas = [], []
            for rc100_dataset in rc100_datasets[fds]:
                sw_matrix = results[rc100_dataset]
                p, beta = pick_best(sw_matrix, strategy=strategy)
                ps.append(p)
                betas.append(beta)
            p, beta = np.mean(ps), np.mean(betas)
            aris.append(calculate_ari(p, beta, fds))
        assert len(aris) == 10
        return aris
    if algorithm == "1-200":
        aris = []
        for fds in full_datasets:
            one_rc200_dataset = min(rc200_datasets[fds], key=lambda ds: get_rc_seed(ds))
            sw_matrix = results[one_rc200_dataset]
            p, beta = pick_best(sw_matrix, strategy=strategy)
            aris.append(calculate_ari(p, beta, fds))
        assert len(aris) == 10
        return aris
    if algorithm == "5-200":
        aris = []
        for fds in full_datasets:
            ps, betas = [], []
            for rc200_dataset in rc200_datasets[fds]:
                sw_matrix = results[rc200_dataset]
                p, beta = pick_best(sw_matrix, strategy=strategy)
                ps.append(p)
                betas.append(beta)
            p, beta = np.mean(ps), np.mean(betas)
            aris.append(calculate_ari(p, beta, fds))
        assert len(aris) == 10
        return aris


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--dumpdirectory", dest="dumpdirectory", default="../dump/ari", type="str",
                      help="directory to read dumps")

    parser.add_option("--datadirectory", dest="datadirectory", type="str",
                      help="directory to read datasets")

    options, args = parser.parse_args()
    dump_directory = options.dumpdirectory
    data_directory = options.datadirectory
    data_directory = "/home/eremeykin/experiment/datasets"

    undumper = UnDumper(dump_directory)
    all_results = undumper.undump_all()

    ari_dict = dict()

    base_datasets = list({get_basename(ds)[:-6] for ds in all_results.keys()})
    algorithms = ["1-1000", "1-100", "1-200", "5-100", "5-200"]
    pprint(base_datasets)
    pprint(algorithms)

    i=0
    for strategy in ["first", "mean", "mean*"]:

        headers = ["dataset"] + algorithms
        table = []

        ds = base_datasets[0]
        for dataset in base_datasets:
            row = [dataset]
            for algorithm in algorithms:
                aris = get_aris(all_results, dataset, algorithm, strategy)
                # print("{} for {} ARI mean = {:6.3f}, std = {:6.3f}".format(dataset, algorithm, np.mean(aris), np.std(aris)))
                print("{}/330".format(i))
                i+=1
                row += ["({:6.3f}, {:6.3f})".format(np.mean(aris), np.std(aris))]
            table += [row]
        # with open("table.dump", "wb") as tdump:
        #     pickle.dump(table, tdump)
        # with open("table.dump", "rb") as tdump:
        #     table = pickle.load(tdump)
        t = tabulate.tabulate(table, headers, tablefmt="plain", numalign="right")
        print("strategy:{}".format(strategy))
        print(t)
