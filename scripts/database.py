import sqlite3 as lite
import os
from optparse import OptionParser
import MySQLdb

hostname = '10.42.0.2'
username = 'eremeykin'
password = '1580'
database = 'experiment'

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--datasetdir", dest="datasetdir", type="str", help="directory of datasets folder")
    parser.add_option("--dbname", dest="dbname", default="experiment", type="str", help="database file name")

    options, args = parser.parse_args()
    dataset_dir = options.datasetdir
    db_name = options.dbname
    con = MySQLdb.connect(host=hostname, user=username, passwd=password, db=db_name)

    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS results")
        cur.execute("DROP TABLE IF EXISTS tasks")
        cur.execute("CREATE TABLE tasks("
                    "id INTEGER PRIMARY KEY,"
                    "dataset TEXT,"
                    "p REAL,"
                    "beta REAL,"
                    "status TEXT,"
                    "priority INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS results("
                    "task INTEGER PRIMARY KEY,"
                    "algorithm TEXT,"
                    "time_init REAL,"
                    "time_kmeans REAL,"
                    "time_award REAL,"
                    "pc_config TEXT,"
                    "labels TEXT,"
                    "sw REAL,"
                    "FOREIGN KEY(task) REFERENCES tasks(id))")
        datasets = [x for x in os.listdir(dataset_dir) if x[-4:] == ".pts"]
        p_range = [x / 10 for x in range(10, 51)]
        beta_range = [x / 10 for x in range(10, 51)]
        id = 1
        status = None
        priority = 1
        datasets.sort(key=lambda x: len(x))
        for dataset in datasets:
            for p in p_range:
                for beta in beta_range:
                    print(dataset, p, beta)
                    cur.execute(
                        "INSERT INTO tasks VALUES(%s,%s,%s,%s,%s,%s)", (id, dataset, p, beta, status, priority))
                        # "INSERT INTO tasks VALUES(?,?,?,?,?,?)", (id, dataset, p, beta, status, priority))
                    id += 1
            priority += 1
