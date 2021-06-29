'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper.
Date         : 2021-06-25 21:37:03
LastEditTime : 2021-06-28 18:38:33
'''

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['ps.fonttype'] = 42
plt.rcParams['pdf.fonttype'] = 42


def plot_replic():
    results = np.genfromtxt("redis_results/replic_2min_1.csv")
    mean = results[-2][: 120]
    stdv = results[-1][: 120]

    # adjust time step, compensate for "Migration..." log
    times = np.arange(len(mean)) + 1
    times[14:] += 1  # TODO: 15s don't need to add 1
    times[29:] += 1
    times[44:] += 1
    times[59:] += 1
    times[74:] += 1
    times[89:] += 1
    times[104:] += 1
    times[119:] += 1

    fig = plt.figure()
    plt.errorbar(times, mean/1000, yerr=stdv/1000, capsize=2, ecolor="green",
                 elinewidth=0.7, label="Avg Query/s")
    # Migration time line
    plt.axvline(x=15, color="red", ls="--", lw=0.7, label="Migrate")
    plt.axvline(x=30, color="red", ls="--", lw=0.7)
    plt.axvline(x=45, color="red", ls="--", lw=0.7)
    plt.axvline(x=60, color="red", ls="--", lw=0.7)
    plt.axvline(x=75, color="red", ls="--", lw=0.7)
    plt.axvline(x=90, color="red", ls="--", lw=0.7)
    plt.axvline(x=105, color="red", ls="--", lw=0.7)
    plt.axvline(x=120, color="red", ls="--", lw=0.7)
    plt.title("Replication Experiment")
    plt.xlabel("Time (s)")
    plt.ylabel("K Query/s")
    plt.legend()
    plt.grid(True)
    # plt.show()
    fig.savefig("replication.pdf", bbox_inches="tight")


def plot_sharding():
    shard1 = np.genfromtxt("redis_results/shard1_2min.csv")
    shard2 = np.genfromtxt("redis_results/shard2_2min.csv")
    shard3 = np.genfromtxt("redis_results/shard3_2min.csv")
    shard4 = np.genfromtxt("redis_results/shard4_2min.csv")

    mean1 = shard1[-2][: 120]
    stdv1 = shard1[-1][: 120]
    mean2 = shard2[-2][: 120]
    stdv2 = shard2[-1][: 120]
    mean3 = shard3[-2][: 120]
    stdv3 = shard3[-1][: 120]
    mean4 = shard4[-2][: 120]
    stdv4 = shard4[-1][: 120]

    times = np.arange(len(mean1)) + 1
    fig = plt.figure()
    plt.errorbar(times, mean1/1000, yerr=stdv1/1000,
                 linewidth=0.7, marker=".", elinewidth=0.7)
    plt.errorbar(times, mean2/1000, yerr=stdv2/1000,
                 linewidth=0.7, marker="1", elinewidth=0.7)
    plt.errorbar(times, mean3/1000, yerr=stdv3/1000,
                 linewidth=0.7, marker="+", elinewidth=0.7)
    plt.errorbar(times, mean4/1000, yerr=stdv4/1000,
                 linewidth=0.7, marker="x", elinewidth=0.7)
    plt.legend(["Shard 1", "Shard 2", "Shard 3", "Shard 4"])
    plt.title("Accumulated Queries in 4 Shards", fontsize=12)
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel("Accumulated Queries (K)", fontsize=12)
    plt.grid(True)
    plt.show()
    # fig.savefig("sharding_size.pdf", bbox_inches="tight")


def main():
    # plot_replic()
    plot_sharding()


if __name__ == "__main__":
    main()
