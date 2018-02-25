import os
import pickle
from math import sqrt
from optparse import OptionParser
from time import time
import MySQLdb
import numpy as np

from scripts.utils import *

host_name = '127.0.0.1'
user_name = 'root'
password = '1580'
database = 'experiment'

SELECT_DATASETS = """SELECT DISTINCT dataset FROM tasks"""
SELECT_RESULT = """SELECT p, beta, sw FROM (SELECT * FROM tasks 
INNER JOIN results ON
tasks.id = results.task) AS j
WHERE j.dataset='{dataset}'"""


class Dumper:
    def __init__(self, directory, host_name, user_name, password, db_name):
        self.conn = MySQLdb.connect(host=host_name, user=user_name, passwd=password, db=db_name)
        self.directory = directory
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
        cursor.execute(SELECT_RESULT.format(dataset=dataset))
        res = cursor.fetchall()
        return res

    def form_matrix(self, result):
        n = int(sqrt(len(result)))
        sw_matrix = np.empty((n, n,))
        sw_matrix[:] = np.nan
        for result_row in result:
            p, beta, sw = result_row
            row = 50 - int(beta * 10)
            col = int(p * 10) - 10
            sw_matrix[row, col] = sw
        return sw_matrix

    def dump_all(self):
        datasets = self.select_datasets()
        for dataset in datasets:
            start = time()
            result = self.select_results(dataset)
            sw_matrix = self.form_matrix(result)
            with open(self.directory + "/" + cut_extention(dataset) + ".dump", "wb") as dump_file:
                pickle.dump((dataset, sw_matrix), dump_file)
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

    options, args = parser.parse_args()
    directory = options.directory

    # dumper = Dumper(directory, host_name, user_name, password, database)
    # dumper.dump_all()
    undumper = UnDumper(directory)
    all = undumper.undump_all()
    print(len(all))
