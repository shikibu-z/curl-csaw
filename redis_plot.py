'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper.
Date         : 2021-06-25 21:37:03
LastEditTime : 2021-06-27 21:01:45
'''

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['ps.fonttype'] = 42
plt.rcParams['pdf.fonttype'] = 42


def plot_replic():
    results = np.genfromtxt("redis_results/replic_2min_1.csv")
    mean = results[-2]
    stdv = results[-1]
    times = np.arange(len(mean)) + 1
    fig = plt.figure()
    plt.errorbar(times, mean/1000, yerr=stdv/1000, capsize=1, ecolor="green",
                 elinewidth=0.7)
    plt.title("Replication Experiment")
    plt.xlabel("Time (s)")
    plt.ylabel("K Queries / s")
    plt.grid(True)
    plt.show()


shard1 = np.genfromtxt("redis_results/shard1.csv")
shard2 = np.genfromtxt("redis_results/shard2.csv")
shard3 = np.genfromtxt("redis_results/shard3.csv")
shard4 = np.genfromtxt("redis_results/shard4.csv")

mean1 = shard1[-2]
stdv1 = shard1[-1]
mean2 = shard2[-2]
stdv2 = shard2[-1]
mean3 = shard3[-2]
stdv3 = shard3[-1]
mean4 = shard4[-2]
stdv4 = shard4[-1]

times = np.arange(len(mean1)) + 1
fig = plt.figure()
plt.errorbar(times, mean1/1000, yerr=stdv1/1000, marker="o", linewidth=0.7)
plt.errorbar(times, mean2/1000, yerr=stdv2/1000, marker="*", linewidth=0.7)
plt.errorbar(times, mean3/1000, yerr=stdv3/1000, marker="^", linewidth=0.7)
plt.errorbar(times, mean4/1000, yerr=stdv4/1000, marker="x", linewidth=0.7)
plt.legend(["Shard 1", "Shard 2", "Shard 3", "Shard 4"])
plt.title("Accumulated Queries in 4 Shards", fontsize=12)
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Accumulated Queries (K)", fontsize=12)
plt.grid(True)
# plt.show()
fig.savefig("sharding.pdf", bbox_inches="tight")


# def plot_shard(mean1, mean2, mean3, mean4, stdv1, stdv2, stdv3, stdv4):
#     plt.rcParams['ps.fonttype'] = 42
#     plt.rcParams['pdf.fonttype'] = 42

#     times = np.arange(len(mean1)) + 1
#     fig = plt.figure()
#     plt.errorbar(times, mean1, yerr=stdv1, marker="o", linewidth=0.6)
#     plt.errorbar(times, mean2, yerr=stdv2, marker="*", linewidth=0.6)
#     plt.errorbar(times, mean3, yerr=stdv3, marker="^", linewidth=0.6)
#     plt.errorbar(times, mean4, yerr=stdv4, marker="x", linewidth=0.6)
#     plt.legend(["Shard 1", "Shard 2", "Shard 3", "Shard 4"])
#     plt.title("Queries in 4 Shards", fontsize=12)
#     plt.xlabel("Time (s)", fontsize=12)
#     plt.ylabel("Queries/s", fontsize=12)
#     plt.grid(True)
#     fig.savefig("sharding.pdf", bbox_inches="tight")
