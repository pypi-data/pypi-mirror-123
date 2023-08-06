from itertools import combinations

import networkx as nx
import numpy as np
import pandas as pd

from ..independence import KCI_UInd
from ..utils import overlap_cluster
from ..utils.kernel import GaussianKernel


def cal_eijk(i, j, k):
    return i - np.cov(i, k)[0, 1] * j / np.cov(j, k)[0, 1]


def triad(data, alpha=.05):
    # cov = np.cov(data.T)
    if data.shape[1] < 3:
        return
    latent_id = 0
    v_labels = ['X' + str(i + 1) for i in range(data.shape[1])]
    kv = {'X' + str(i + 1): i for i in range(data.shape[1])}
    g = nx.DiGraph()
    for i in v_labels:
        g.add_node(i)

    kcitest = KCI_UInd(sample_size=data.shape[0], kernelX=GaussianKernel(), kernelY=GaussianKernel(), approx=False)

    # Phase 1: Finding Clusters
    cont = True
    while cont:
        cluster_list = []
        if len(v_labels) < 3:
            break
        for (i, j) in combinations(v_labels, 2):
            same_cluster = True
            for k in v_labels:
                if k == i or k == j:
                    continue
                eijk = cal_eijk(data[:, kv[i]], data[:, kv[j]], data[:, kv[k]])
                pval = kcitest.compute_pvalue(eijk, data[:, kv[k]])

                print(i, j, k, pval)
                if pval <= alpha:
                    same_cluster = False
                    break

            if same_cluster:
                cluster_list.append([i, j])

        if len(cluster_list) == 0:
            break
        else:
            print(cluster_list)
            cluster_list = overlap_cluster(cluster_list)
            print(cluster_list)
            v_set = set(v_labels)
            for i in cluster_list:
                latent_name = "L" + str(latent_id + 1)
                latent_id += 1
                v_set |= {latent_name}
                for j in i:
                    v_set -= {j}
                    g.add_edge(latent_name, j)

                kv[latent_name] = kv[i[0]]
            v_labels = list(v_set)

        cont = False
        for i in v_labels:
            if i[0] == 'X':
                cont = True

    # Phase 2: Learning the Structure of Latent Variables
    latent_root_set = set()
    not_root_latent = set()
    for i in g.nodes():
        if i[0] == 'L':
            latent_root_set |= {i}
        for _, j in g.edges(i):
            if j[0] == 'L':
                not_root_latent |= {j}
    latent_root_set -= not_root_latent

    datasets = pd.DataFrame()

    for i in latent_root_set:
        cnt = 0
        for _, j in g.edges(i):
            datasets[(i, cnt)] = data[:, kv[j]]
            cnt += 1
            if cnt == 2:
                break

    while len(latent_root_set) > 1:
        latent_root = ""
        for i in latent_root_set:
            is_root = True
            for j in latent_root_set:
                if j == i:
                    continue
                ekij = cal_eijk(datasets[(j, 0)], datasets[(i, 0)], datasets[(i, 1)])
                if kcitest.compute_pvalue(ekij, datasets[(i, 1)]) <= alpha:
                    is_root = False
                    break
            if is_root:
                latent_root = i
                break
        if latent_root == "":
            break

        for i in latent_root_set:
            if i == latent_root:
                continue
            g.add_edge(latent_root, i)
            datasets[(i, 0)] = cal_eijk(datasets[(i, 0)],
                                        datasets[(latent_root, 0)], datasets[(latent_root, 1)])

        latent_root_set -= {latent_root}
    return g
