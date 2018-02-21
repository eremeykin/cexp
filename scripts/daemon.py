from clustering.agglomerative.pattern_initialization.ap_init_pb import APInitPB
from clustering.agglomerative.utils.imwk_means_cluster_structure import IMWKMeansClusterStructure
from clustering.agglomerative.ik_means.ik_means import IKMeans
from clustering.agglomerative.a_ward_pb import AWardPB as AWardPB_
from clustering.agglomerative.utils.choose_p import ChooseP
from subprocess import Popen, PIPE
from shlex import split
from optparse import OptionParser
from time import time
import re
import pandas as pd
import pickle
import MySQLdb


def get_pc_info(password):
    p1 = Popen(split("echo " + password), stdout=PIPE)
    p2 = Popen(split("sudo -S lshw"), stdin=p1.stdout, stdout=PIPE)
    p3 = Popen(split("grep -i cpu"), stdin=p2.stdout, stdout=PIPE)
    p4 = Popen(split("grep -i product"), stdin=p3.stdout, stdout=PIPE)
    output, error = p4.communicate()
    cpu = output.decode('utf-8').split(':')[1].strip()
    p1 = Popen(split("free -m"), stdout=PIPE)
    p2 = Popen(split("grep -i Mem:"), stdin=p1.stdout, stdout=PIPE)
    output, error = p2.communicate()
    mem = output.decode('utf-8').split()[1]
    return "{cpu} / {mem} Mb".format(cpu=cpu, mem=mem)


PC_INFO = get_pc_info("1580")

SELECT_TASKS = """SELECT * FROM tasks 
WHERE tasks.status is Null
ORDER BY tasks.priority
LIMIT {limit}"""

SET_STATUS = """UPDATE tasks
SET status = "{status}"
WHERE id IN"""

SELECT_CACHED_LABELS = """SELECT results.sw FROM results
WHERE labels = "{labels}"
LIMIT 1
"""

SW_CACHE = dict()


def get_tasks(conn):
    cursor = conn.cursor()
    cursor.execute(SELECT_TASKS)
    return cursor.fetchall()


def set_status(conn, status, ids):
    cursor = conn.cursor()
    cursor.execute(SET_STATUS.format(status=status) + str(tuple(ids)))
    conn.commit()


def get_k_star(datasetname):
    return int(re.search('_c(\d+)_', datasetname).group(1))


def insert_result(conn, task, algorithm, time_init, time_kmeans, time_award, pc_config, labels, sw):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO results VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
        (task, algorithm, time_init, time_kmeans, time_award, pc_config, labels, sw))


def calculate_sw(conn, labels, cluster_structure, cache):
    if cache == 'db':
        cursor = conn.cursor()
        r_count = cursor.execute(SELECT_CACHED_LABELS.format(labels=labels))
        if r_count == 1:
            res = cursor.fetchall()[0][0]
            print("db cache match")
            return res
    if cache == 'dict':
        if labels in SW_CACHE:
            print("dict cache match")
            return SW_CACHE[labels]
    sw = ChooseP.AvgSilhouetteWidthCriterion()
    SW_CACHE[labels] = sw
    return sw(cluster_structure)


def single_run(data, p, beta, k_star):
    data = pd.read_csv(data)
    data = data.as_matrix()
    # Init
    run_ap_init_pb = APInitPB(data, p, beta)
    init_start = time()
    run_ap_init_pb()
    init_end = time()

    # change cluster structure to matlab compatible
    clusters = run_ap_init_pb.cluster_structure.clusters
    new_cluster_structure = IMWKMeansClusterStructure(data, p, beta)
    new_cluster_structure.add_all_clusters(clusters)

    # IKMeans
    run_ik_means = IKMeans(new_cluster_structure)
    kmeans_start = time()
    run_ik_means()
    kmeans_end = time()
    cs = run_ik_means.cluster_structure

    # AWard
    run_a_ward_pb = AWardPB_(cs, k_star)
    award_start = time()
    result = run_a_ward_pb()
    award_end = time()

    time_init = init_end - init_start
    time_kmeans = kmeans_end - kmeans_start
    time_award = award_end - award_start
    cluster_structure = run_a_ward_pb.cluster_structure
    labels = cluster_structure.current_labels()
    algorithm = "A-Ward_p_beta with p={}, beta={}, k_star={}".format(p, beta, k_star)
    return algorithm, time_init, time_kmeans, time_award, labels, cluster_structure


hostname = '10.42.0.2'
username = 'eremeykin'
password = '1580'
database = 'experiment'

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--datasetdir", dest="datasetdir", type="str", help="directory of datasets folder")
    parser.add_option("--dbname", dest="dbname", default="experiment", type="str", help="database file name")

    parser.add_option("--cache", dest="cache", default="db", type="str", help="type of cache")
    parser.add_option("--limit", dest="limit", default="10", type="str", help="limit of tasks to capture")

    options, args = parser.parse_args()
    db_name = options.dbname
    dataset_dir = options.datasetdir
    cache = options.cache

    limit = options.limit
    SELECT_TASKS = SELECT_TASKS.format(limit=limit)

    conn = MySQLdb.connect(host=hostname, user=username, passwd=password, db=db_name)
    with conn:
        cur = conn.cursor()
        from time import time

        while True:
            s = time()
            tasks = get_tasks(conn)
            if len(tasks) < 1:
                break
            set_status(conn, "PEND", [task[0] for task in tasks])
            for task in tasks:
                task_start = time()
                id, dataset, p, beta, status, priority = task
                k_star = get_k_star(dataset)
                dataset = dataset_dir + "/" + dataset
                algorithm, time_init, time_kmeans, time_award, labels, cluster_structure = single_run(dataset, p, beta,
                                                                                                      k_star)
                sw_start = time()
                sw = calculate_sw(conn, str(labels), cluster_structure, cache=cache)
                task_end = time()
                insert_result(conn, id, algorithm, time_init, time_kmeans, time_award, PC_INFO, str(labels), sw)
                insert_end = time()
                print("{} completed, task: {:15.2f}, sw={:15.2f} ,insert: {:15.2f}".format(id,
                                                                                           task_end - task_start,
                                                                                           task_end - sw_start,
                                                                                           insert_end - task_end))
            set_status(conn, "COMP", [task[0] for task in tasks])
            print("10 completed: {:15.2f}".format(time() - s))
