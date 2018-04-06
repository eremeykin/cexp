import pandas as pd

if __name__ == "__main__":
    times = pd.read_csv("times.csv", index_col=0)
    times['time'] = times['init'] + times['kmeans'] + times['award']
    del times['init']
    del times['kmeans']
    del times['award']
    print("!!!!!!!!!!!!!!!!!!!!!")
    print("Full")
    print("!!!!!!!!!!!!!!!!!!!!!")
    for c in [7, 12, 19]:
        print("___________")
        times_ = times.filter(regex="^kov.*_c{}_.*".format(c), axis=0)
        print("c = {}".format(c))
        print("mean = {}".format(times_.mean()[0]))
        print("std = {}".format(times_.std()[0]))
    print("!!!!!!!!!!!!!!!!!!!!!")
    print("1-100")
    print("!!!!!!!!!!!!!!!!!!!!!")
    for c in [7, 12, 19]:
        print("___________")
        times_ = times.filter(regex="rc_ch100_s1981_\[kovaleva_1000x15_c{}_m.*_a0\.5_s.*\]".format(c), axis=0)
        print("c = {}".format(c))
        print("mean = {}".format(times_.mean()[0]))
        print("std = {}".format(times_.std()[0]))
    print("!!!!!!!!!!!!!!!!!!!!!")
    print("1-200")
    print("!!!!!!!!!!!!!!!!!!!!!")
    for c in [7, 12, 19]:
        print("___________")
        times_ = times.filter(regex="rc_ch200_s1981_\[kovaleva_1000x15_c{}_m.*_a0\.5_s.*\]".format(c), axis=0)
        print("c = {}".format(c))
        print("mean = {}".format(times_.mean()[0]))
        print("std = {}".format(times_.std()[0]))
    print("!!!!!!!!!!!!!!!!!!!!!")
    print("5-100")
    print("!!!!!!!!!!!!!!!!!!!!!")
    for c in [7, 12, 19]:
        print("___________")
        times_ = times.filter(regex="rc_ch100_s.*_\[kovaleva_1000x15_c{}_m.*_a0\.5_s.*\]".format(c), axis=0)
        times_['seed_main'] = times_.index.str.slice(47, 51)
        times_ = times_.groupby(["seed_main"]).sum()
        print("c = {}".format(c))
        print("mean = {}".format(times_.mean()[0]))
        print("std = {}".format(times_.std()[0]))
    print("!!!!!!!!!!!!!!!!!!!!!")
    print("5-200")
    print("!!!!!!!!!!!!!!!!!!!!!")
    for c in [7, 12, 19]:
        print("___________")
        times_ = times.filter(regex="rc_ch200_s.*_\[kovaleva_1000x15_c{}_m.*_a0\.5_s.*\]".format(c), axis=0)
        times_['seed_main'] = times_.index.str.slice(47, 51)
        times_ = times_.groupby(["seed_main"]).sum()
        print("c = {}".format(c))
        print("mean = {}".format(times_.mean()[0]))
        print("std = {}".format(times_.std()[0]))