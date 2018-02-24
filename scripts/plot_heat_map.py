import matplotlib.pyplot as plt
from optparse import OptionParser
import MySQLdb
import numpy as np
from scripts.utils import get_k_star
import os

hostname = '10.42.0.2'
username = 'eremeykin'
password = '1580'
database = 'experiment'


class Plotter:
    N = 41
    SELECT_DATASETS = """SELECT DISTINCT dataset FROM tasks"""
    SELECT_RESULT = """SELECT p, beta, sw FROM (SELECT * FROM tasks 
INNER JOIN results ON
tasks.id = results.task) AS j
WHERE j.dataset='{dataset}'"""

    def __init__(self, db_name):
        self.conn = MySQLdb.connect(host=hostname, user=username, passwd=password, db=db_name)
        plt.grid()
        # plt.colorbar()

    def select_base_datasets(self):
        cursor = self.conn.cursor()
        cursor.execute(Plotter.SELECT_DATASETS)
        res = cursor.fetchall()
        datasets = []
        for row in res:
            if row[0][:3] == "rc_":
                continue
            datasets.append(row[0])
        return datasets

    def select_result(self, dataset):
        cursor = self.conn.cursor()
        cursor.execute(Plotter.SELECT_RESULT.format(dataset=dataset))
        res = cursor.fetchall()
        return res

    def form_matrix(self, result):
        sw_matrix = np.empty((Plotter.N, Plotter.N,))
        sw_matrix[:] = np.nan
        for result_row in result:
            p, beta, sw = result_row
            row = 50 - int(beta * 10)
            col = int(p * 10) - 10
            sw_matrix[row, col] = sw
        return sw_matrix

    def plot_heatmap(self, sw_matrix, dataset):
        plt.imshow(sw_matrix, cmap='hot', interpolation='nearest')
        plt.title(dataset)
        range = np.linspace(1.0, 5.0, 41, endpoint=True)
        plt.xticks(np.arange(len(range)), range, rotation='vertical')
        plt.yticks(np.arange(len(range)), reversed(range))
        plt.subplots_adjust(left=0.1, right=0.98, top=0.98, bottom=0.1)
        figure = plt.gcf()
        figure.set_size_inches(19, 10)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--dbname", dest="dbname", default="experiment", type="str", help="database file name")

    options, args = parser.parse_args()
    db_name = options.dbname
    plotter = Plotter(db_name)
    from pprint import pprint

    dsets = plotter.select_base_datasets()
    flag = True
    for dset in dsets:
        res = plotter.select_result(dset)
        if len(res) < Plotter.N ** 2:
            continue
        sw_matrix = plotter.form_matrix(res)
        plotter.plot_heatmap(sw_matrix, dset)
        if flag:
            plt.colorbar(ticks=np.linspace(-1, 1, 21, endpoint=True))
            flag = False
        results_dir = "../img/" + str(get_k_star(dset)) + "/"
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        plt.savefig(results_dir + dset + ".png", dpi=300)
        print(dset)
