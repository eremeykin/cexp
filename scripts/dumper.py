import os
import pickle
from math import sqrt
from optparse import OptionParser
from time import time
import MySQLdb
import numpy as np
from scripts.utils import *
from sklearn.metrics import adjusted_rand_score as ari

host_name = '127.0.0.1'
user_name = 'root'
password = '1580'
database = 'experiment'

SELECT_DATASETS = """SELECT DISTINCT dataset FROM tasks"""
SELECT_RESULT = """SELECT p, beta, sw FROM (SELECT * FROM tasks 
INNER JOIN results ON
tasks.id = results.task) AS j
WHERE j.dataset='{dataset}'"""

SELECT_LABELS = """SELECT p, beta, labels FROM (SELECT * FROM tasks 
INNER JOIN results ON
tasks.id = results.task) AS j
WHERE j.dataset='{dataset}'"""


class Dumper:
    def __init__(self, directory, host_name, user_name, password, db_name, ds_directory, type):
        self.conn = MySQLdb.connect(host=host_name, user=user_name, passwd=password, db=db_name)
        self.directory = directory
        self.type = type
        self.ds_directory = ds_directory
        if not os.path.isdir(directory):
            os.makedirs(directory)

    def select_datasets(self):
        cursor = self.conn.cursor()
        cursor.execute(SELECT_DATASETS)
        res = cursor.fetchall()
        datasets = []
        for row in res:
            datasets.append(row[0])
        return datasets

    def select_results(self, dataset):
        cursor = self.conn.cursor()
        if self.type == "sw":
            cursor.execute(SELECT_RESULT.format(dataset=dataset))
            res = cursor.fetchall()
            return res
        if self.type == "ari":
            cursor.execute(SELECT_LABELS.format(dataset=dataset))
            res = cursor.fetchall()
            return res

    def form_matrix(self, result, dataset):
        n = int(sqrt(len(result)))
        res_matrix = np.empty((n, n,))
        res_matrix[:] = np.nan
        if self.type == "sw":
            for result_row in result:
                p, beta, sw = result_row
                row = beta_to_row(beta)  # 50 - int(beta * 10)
                col = p_to_col(p)  # int(p * 10) - 10
                res_matrix[row, col] = sw
        if self.type == "ari":
            for result_row in result:
                p, beta, labels = result_row
                labels = labels.replace("[", "")
                labels = labels.replace("]", "")
                labels = np.fromstring(labels, sep=" ", dtype=int)
                row = beta_to_row(beta)  # 50 - int(beta * 10)
                col = p_to_col(p)  # int(p * 10) - 10
                labels_true = np.loadtxt(ds_directory + "/" + cut_extention(dataset) + ".lbs", skiprows=1)
                labels_true = labels_true.astype(int)
                res_matrix[row, col] = ari(labels_true, labels)
        return res_matrix

    def dump_all(self):
        datasets = self.select_datasets()
        for dataset in datasets:
            start = time()
            result = self.select_results(dataset)
            matrix = self.form_matrix(result, dataset)
            with open(self.directory + "/" + self.type + "/" + cut_extention(dataset) + "." + self.type + ".dump",
                      "wb") as dump_file:
                pickle.dump((dataset, matrix), dump_file)
            end = time()
            print("{} dumped OK ({} sec).".format(dataset, end - start))


class UnDumper:
    def __init__(self, directory):
        self.directory = directory

    def undump(self, dump_file_name):
        with open(dump_file_name, 'rb') as dump_file:
            undump = pickle.load(dump_file)
            dataset = undump[0]
            sw_matrix = undump[1]
            return dataset, sw_matrix

    def undump_all(self):
        results = dict()
        for dump_file in os.listdir(self.directory):
            start = time()
            full_path = "/".join([self.directory, dump_file])
            dataset, sw_matrix = self.undump(full_path)
            results[dataset] = sw_matrix
            end = time()
            # print("{} undumped OK ({} sec).".format(dump_file, end - start))
        return results


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--directory", dest="directory", default="./../dump", type="str", help="directory to save dumps")
    parser.add_option("--ds_directory", dest="ds_directory", default="/home/eremeykin/experiment/datasets", type="str",
                      help="directory to save dumps")

    options, args = parser.parse_args()
    directory = options.directory
    ds_directory = options.ds_directory

    dumper = Dumper(directory, host_name, user_name, password, database, ds_directory, "ari")
    dumper.dump_all()
    # undumper = UnDumper(directory)
    # all = undumper.undump_all()
