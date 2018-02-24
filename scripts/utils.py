import re


def get_k_star(datasetname):
    return int(re.search('_c(\d+)_', datasetname).group(1))
