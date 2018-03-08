import re


def get_k_star(datasetname):
    return int(re.search('_c(\d+)_', datasetname).group(1))


def get_basename(datasetname):
    if datasetname.startswith("rc_"):
        return re.search('\[(.*)\]', datasetname).group(1)
    else:
        return re.search('(.*).pts', datasetname).group(1)


def get_chunk_size(datasetname):
    if datasetname.startswith("rc_"):
        return int(re.search('_ch(\d*)_', datasetname).group(1))
    else:
        return -1


def get_rc_seed(datasetname):
    if datasetname.startswith("rc_"):
        return int(re.search('_s(\d*)_\[', datasetname).group(1))
    else:
        return -1


def cut_extention(string):
    return string[:string.rindex(".")]


def p_to_col(p):
    col = int(p * 10) - 10
    return col


def col_to_p(col):
    p = (col + 10.0) / 10.0
    return p


def beta_to_row(beta):
    row = 50 - int(beta * 10)
    return row


def row_to_beta(row):
    beta = (50.0 - row) / 10.0
    return beta


if __name__ == "__main__":
    assert get_k_star("kovaleva_1000x15_c7_m100_a0.5_s2095.pts") == 7
    assert get_k_star("rc_ch100_s1981_[kovaleva_1000x15_c19_m35_a0.5_s6472].pts") == 19
    assert get_basename("kovaleva_1000x15_c7_m100_a0.5_s2095.pts") == "kovaleva_1000x15_c7_m100_a0.5_s2095"
    assert get_basename(
        "rc_ch100_s1981_[kovaleva_1000x15_c19_m35_a0.5_s6472].pts") == "kovaleva_1000x15_c19_m35_a0.5_s6472"
    assert get_chunk_size("kovaleva_1000x15_c7_m100_a0.5_s2095.pts") == -1
    assert get_chunk_size("rc_ch100_s1981_[kovaleva_1000x15_c19_m35_a0.5_s6472].pts") == 100
    assert get_chunk_size("rc_ch200_s1981_[kovaleva_1000x15_c19_m35_a0.5_s6472].pts") == 200
    assert cut_extention("kovaleva_1000x15_c7_m100_a0.5_s2095.pts") == "kovaleva_1000x15_c7_m100_a0.5_s2095"
    assert 1.4 == col_to_p(p_to_col(1.4))
    assert 16 == p_to_col(col_to_p(16))
    assert 1.4 == row_to_beta(beta_to_row(1.4))
    assert get_rc_seed("rc_ch200_s1981_[kovaleva_1000x15_c19_m35_a0.5_s6472].pts") == 1981
