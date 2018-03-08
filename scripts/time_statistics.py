import os
import pickle
from math import sqrt
from optparse import OptionParser
from time import time
import MySQLdb
import numpy as np

import matplotlib.pyplot as plt

from scripts.utils import *

Q9550_CONFIG = 'Intel(R) Core(TM)2 Quad CPU    Q9550  @ 2.83GHz / 3950 Mb'
SELECT_TIME = """SELECT {time_type} from results WHERE pc_config='{config}' AND task>50430"""

host_name = '127.0.0.1'
user_name = 'root'
password = '1580'
database = 'experiment'


class StatisticsAnalyzer:
    def __init__(self, host_name, user_name, password, db_name):
        self.conn = MySQLdb.connect(host=host_name, user=user_name, passwd=password, db=db_name)

    def select_times(self):
        cursor = self.conn.cursor()
        size = cursor.execute(SELECT_TIME.format(time_type='time_award', config=Q9550_CONFIG))
        times = np.zeros(size)
        for i, row in enumerate(cursor.fetchall()):
            times[i] = row[0]
        plt.hist(times, 100, normed=1, facecolor='g', alpha=0.75)
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    sa = StatisticsAnalyzer(host_name, user_name, password, database)
    sa.select_times()
