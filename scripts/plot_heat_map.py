import matplotlib.pyplot as plt
from optparse import OptionParser
import numpy as np
from scripts.utils import *
import os
from scripts.dumper import UnDumper
from time import time

def plot_heatmap(sw_matrix, dataset):
    plt.imshow(sw_matrix, cmap='hot', interpolation='nearest')
    plt.title(dataset)
    range = np.linspace(1.0, 5.0, 41, endpoint=True)
    plt.xticks(np.arange(len(range)), range, rotation='vertical')
    plt.yticks(np.arange(len(range)), reversed(range))
    plt.subplots_adjust(left=0.1, right=0.98, top=0.95, bottom=0.1)
    figure = plt.gcf()
    figure.set_size_inches(12, 10)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--dumpdirectory", dest="dumpdirectory", default="../dump", type="str",
                      help="directory to read dumps")
    parser.add_option("--imgdirectory", dest="imgdirectory", default="../img", type="str",
                      help="directory to read dumps")

    options, args = parser.parse_args()
    dump_directory = options.dumpdirectory
    img_directory = options.imgdirectory

    undumper = UnDumper(dump_directory)
    all_results = undumper.undump_all()
    draw_colorbar = True

    for dataset, sw_matrix in all_results.items():
        start = time()
        plot_heatmap(sw_matrix, dataset)
        plt.colorbar(ticks=np.linspace(-1, 1, 21, endpoint=True))
        plt.grid()
        ds_basename = get_basename(dataset)
        chunk_size = get_chunk_size(dataset)
        k_star = str(get_k_star(dataset))
        results_dir = "/".join([img_directory, k_star, ds_basename])
        if chunk_size > 0:
            results_dir = "/".join([results_dir, str(chunk_size)])
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        plt.savefig(results_dir + "/" + cut_extention(dataset) + ".png", dpi=150)
        plt.close()
        end = time()
        print("{} completed successfully in {} sec. ".format(dataset, end - start))
