'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper.
Date         : 2021-06-25 21:37:03
LastEditTime : 2021-06-30 21:50:28
'''

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["ps.fonttype"] = 42
plt.rcParams["pdf.fonttype"] = 42


def plot_replic():
    results = np.genfromtxt("redis_results/replic_2.csv")
    mean = results[-2][: 120]
    stdv = results[-1][: 120]

    # adjust time step, compensate for "Migration..." log
    times = np.arange(len(mean)) + 1
    times[16:] += 1
    times[29:] += 1
    times[44:] += 1
    times[59:] += 1
    times[74:] += 1
    times[89:] += 1
    times[104:] += 1
    times[119:] += 1

    fig = plt.figure()
    plt.errorbar(times, mean/1000, yerr=stdv/1000, capsize=2, ecolor="green",
                 elinewidth=0.6)
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
    plt.show()
    # fig.savefig("replication.pdf", bbox_inches="tight")


def plot_sharding():
    shard1_size = np.genfromtxt("redis_results/shard1_size.csv")
    shard2_size = np.genfromtxt("redis_results/shard2_size.csv")
    shard3_size = np.genfromtxt("redis_results/shard3_size.csv")
    shard4_size = np.genfromtxt("redis_results/shard4_size.csv")

    mean1_size = shard1_size[-2][: 120]
    stdv1_size = shard1_size[-1][: 120]
    mean2_size = shard2_size[-2][: 120]
    stdv2_size = shard2_size[-1][: 120]
    mean3_size = shard3_size[-2][: 120]
    stdv3_size = shard3_size[-1][: 120]
    mean4_size = shard4_size[-2][: 120]
    stdv4_size = shard4_size[-1][: 120]

    fig = plt.figure()
    times = np.arange(len(mean1_size))
    plt.errorbar(times, mean1_size/1000, yerr=stdv1_size/1000,
                 linewidth=2, elinewidth=0.7)
    plt.errorbar(times, mean2_size/1000, yerr=stdv2_size/1000,
                 linewidth=2, ls="--", elinewidth=0.7)
    plt.errorbar(times, mean3_size/1000, yerr=stdv3_size/1000,
                 linewidth=2, ls="-.", elinewidth=0.7)
    plt.errorbar(times, mean4_size/1000, yerr=stdv4_size/1000,
                 linewidth=2, ls=":", elinewidth=0.7)
    plt.legend(["Shard 1", "Shard 2",
                "Shard 3", "Shard 4"])
    plt.title("Cumulative Req of Sharding by Key Size",
              fontsize=12)  # * key len from 400 - 950
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel("Cumulative KReq", fontsize=12)
    plt.grid(True)
    # plt.show()
    fig.savefig("shard_size.pdf", bbox_inches="tight")


def plot_ecdf():
    x_set_key = [0, 0, 1, 2]
    y_set_key = [0, 0.8613, 1, 1]
    x_get_key = [0, 0, 1]
    y_get_key = [0, 0.8607, 1]
    x_set_base = [0, 0, 1, 2]
    y_set_base = [0, 0.9114, 1, 1]
    x_get_base = [0, 0, 1]
    y_get_base = [0, 0.9084, 1]

    fig1, ax1 = plt.subplots()
    ax1.plot(x_set_key, y_set_key, lw=2, markersize=7)
    ax1.plot(x_set_base, y_set_base, ls="-.", lw=2, markersize=7)
    ax1.legend(["Shard Key SET", "Base SET", ])
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Cumulative Probability")
    ax1.set_title("CDF of Req Latency of Uneven Sharding by Key Hash")
    ax1.grid(True)
    plt.show()
    # fig1.savefig("shard_size_cdf.pdf", bbox_inches="tight")


def main():
    # plot_replic()
    plot_sharding()
    # plot_ecdf()


if __name__ == "__main__":
    main()
