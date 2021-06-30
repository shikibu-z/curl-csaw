'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper.
Date         : 2021-06-25 21:37:03
LastEditTime : 2021-06-29 17:04:50
'''

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['ps.fonttype'] = 42
plt.rcParams['pdf.fonttype'] = 42


def plot_replic():
    results = np.genfromtxt("redis_results/replic_2min_1.csv")
    mean = results[-2][: 120]
    stdv = results[-1][: 120]

    with open("redis_results/baseline_replic.csv") as f:
        baseline = f.readlines()
        baseline_mean = float(baseline[-2])
        baseline_stdv = float(baseline[-1])
        f.close()

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
                 elinewidth=0.6, label="Modified")
    plt.errorbar(times, [baseline_mean/1000]*len(times), yerr=[baseline_stdv/1000]*len(
        times), ls="--", capsize=2, ecolor="green", elinewidth=0.6, label="Baseline")
    # Migration time line
    plt.axvline(x=15, color="red", ls="--", lw=0.6, label="Replicate")
    plt.axvline(x=30, color="red", ls="--", lw=0.6)
    plt.axvline(x=45, color="red", ls="--", lw=0.6)
    plt.axvline(x=60, color="red", ls="--", lw=0.6)
    plt.axvline(x=75, color="red", ls="--", lw=0.6)
    plt.axvline(x=90, color="red", ls="--", lw=0.6)
    plt.axvline(x=105, color="red", ls="--", lw=0.6)
    plt.axvline(x=120, color="red", ls="--", lw=0.6)
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
    shard1_size = np.genfromtxt("redis_results/shard1_size.csv")
    shard2_size = np.genfromtxt("redis_results/shard2_size.csv")
    shard3_size = np.genfromtxt("redis_results/shard3_size.csv")
    shard4_size = np.genfromtxt("redis_results/shard4_size.csv")
    with open("redis_results/baseline_shard.csv") as f:
        baseline = f.readlines()
        baseline_mean = float(baseline[-2])
        baseline_stdv = float(baseline[-1])
        f.close()

    mean1 = shard1[-2][: 120]
    stdv1 = shard1[-1][: 120]
    mean2 = shard2[-2][: 120]
    stdv2 = shard2[-1][: 120]
    mean3 = shard3[-2][: 120]
    stdv3 = shard3[-1][: 120]
    mean4 = shard4[-2][: 120]
    stdv4 = shard4[-1][: 120]

    mean1_size = shard1_size[-2][: 120]
    stdv1_size = shard1_size[-1][: 120]
    mean2_size = shard2_size[-2][: 120]
    stdv2_size = shard2_size[-1][: 120]
    mean3_size = shard3_size[-2][: 120]
    stdv3_size = shard3_size[-1][: 120]
    mean4_size = shard4_size[-2][: 120]
    stdv4_size = shard4_size[-1][: 120]

    times = np.arange(len(mean1)) + 1
    fig = plt.figure()
    plt.errorbar(times, mean1/1000, yerr=stdv1/1000,linewidth=0.6, marker=".", markersize=5, elinewidth=0.6)
    plt.errorbar(times, mean2/1000, yerr=stdv2/1000,linewidth=0.6, marker="1", markersize=5, elinewidth=0.6)
    plt.errorbar(times, mean3/1000, yerr=stdv3/1000,linewidth=0.6, marker="+", markersize=5, elinewidth=0.6)
    plt.errorbar(times, mean4/1000, yerr=stdv4/1000,linewidth=0.6, marker="x", markersize=5, elinewidth=0.6)
    plt.errorbar(times, (baseline_mean/4000)*times, yerr=(baseline_stdv/4000)* times, ls="--", elinewidth=0.6)
    times = np.arange(len(mean1_size))
    plt.errorbar(times, mean1_size/1000, yerr=stdv1_size/1000,linewidth=0.6, marker="o",markersize=5, elinewidth=0.6)
    plt.errorbar(times, mean2_size/1000, yerr=stdv2_size/1000,linewidth=0.6, marker="^",markersize=5, elinewidth=0.6)
    plt.errorbar(times, mean3_size/1000, yerr=stdv3_size/1000,linewidth=0.6, marker="P",markersize=5, elinewidth=0.6)
    plt.errorbar(times, mean4_size/1000, yerr=stdv4_size/1000,linewidth=0.6, marker="*",markersize=5, elinewidth=0.6)
    plt.legend(["Shard 1 by key", "Shard 2 by key", "Shard 3 by key", "Shard 4 by key",
                "Baseline", "Shard 1 by size", "Shard 2 by size", "Shard 3 by size", "Shard 4 by size"])
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
