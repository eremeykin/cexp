import sqlite3 as lite
import os
import sys
import subprocess
from subprocess import Popen, PIPE
from shlex import split
from optparse import OptionParser


def get_cp_info(password):
    p1 = Popen(split("echo " + password), stdout=PIPE)
    p2 = Popen(split("sudo -S lshw"), stdin=p1.stdout, stdout=PIPE)
    p3 = Popen(split("grep -i cpu"), stdin=p2.stdout, stdout=PIPE)
    p4 = Popen(split("grep -i product"), stdin=p3.stdout, stdout=PIPE)
    output, error = p4.communicate()
    cpu = output.decode('utf-8').split(':')[1].strip()
    print('cpu=' + cpu)
    p1 = Popen(split("free -m"), stdout=PIPE)
    p2 = Popen(split("grep -i Mem:"), stdin=p1.stdout, stdout=PIPE)
    output, error = p2.communicate()
    mem = output.decode('utf-8').split()[1]
    return "{cpu} / {mem} Mb".format(cpu=cpu, mem=mem)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--datasetdir", dest="datasetdir", type="str", help="directory of datasets folder")
    parser.add_option("--dbname", dest="dbname", default="experiment", type="str", help="database file name")

    options, args = parser.parse_args()
    dataset_dir = options.datasetdir
    db_name = options.dbname
    con = lite.connect('{dbname}.sqlite3'.format(dbname=db_name))
    with con:
        cur = con.cursor()
        # cur.execute("DROP TABLE IF EXISTS results")
        cur.execute("DROP TABLE IF EXISTS tasks")
        cur.execute("CREATE TABLE tasks("
                    "id INTEGER PRIMARY KEY,"
                    "dataset TEXT,"
                    "p REAL,"
                    "beta REAL,"
                    "status TEXT,"
                    "priority INTEGER,"
                    "algorithm TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS results("
                    "id INTEGER PRIMARY KEY,"
                    "task INTEGER,"
                    "algorithm TEXT,"
                    "time_init REAL,"
                    "time_kmeans REAL,"
                    "time_award REAL,"
                    "pc_config TEXT"
                    "labels TEXT,"
                    "sw REAL,"
                    "FOREIGN KEY(task) REFERENCES tasks(id))")
        datasets = [x for x in os.listdir(dataset_dir) if x[-4:] == ".pts"]
        p_range = [x / 10 for x in range(10, 51)]
        beta_range = [x / 10 for x in range(10, 51)]
        # cur.execute('BEGIN TRANSACTION')
        id = 1
        status = None
        algorithm = None
        for dataset in datasets:
            for p in p_range:
                for beta in beta_range:
                    print(dataset, p, beta)
                    priority = 1
                    cur.execute(
                        "INSERT INTO tasks VALUES(?,?,?,?,?,?,?)", (id, dataset, p, beta, status, priority, algorithm))
                    id += 1
        # cur.execute('COMMIT')
