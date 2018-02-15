from optparse import OptionParser
import pandas as pd
import numpy as np

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--dataset", dest="dataset", type="str",
                      help="full path to dataset to choice from (must be .pts)")
    parser.add_option("--chunksize", dest="chunksize", type="int", help="number of objects to choice")
    parser.add_option("--seed", dest="seed", type="int", help="seed of generator")

    options, args = parser.parse_args()
    dataset = options.dataset
    chunk_size = options.chunksize
    seed = options.seed

    dataset_file = dataset.split("/")[-1]
    dataset_name = dataset_file[:-4]  # without .pts
    folder = "/".join(dataset.split("/")[:-1])

    data = pd.read_csv(dataset)
    data = data.as_matrix()
    labels = pd.read_csv(folder + "/" + dataset_name + ".lbs")
    labels = labels.as_matrix()
    # set seed
    np.random.seed(seed)
    index = np.arange(0, len(data))
    chunk_index = np.random.choice(index, size=chunk_size, replace=False)
    chunk_data = data[chunk_index]
    chunk_labels = labels[chunk_index]

    new_name = "rc_ch{chunksize}_s{seed}_[{dataset}]".format(chunksize=chunk_size,
                                                             seed=seed,
                                                             dataset=dataset_name)
    pts_path = "/".join([folder, new_name + ".pts"])
    lbs_path = "/".join([folder, new_name + ".lbs"])
    # save data
    np.savetxt(pts_path, chunk_data, delimiter=',', comments='',
               header=','.join(['F' + str(i) for i in range(data.shape[1])]))
    # save labels
    np.savetxt(lbs_path, chunk_labels, delimiter=',', comments='', header="L")
