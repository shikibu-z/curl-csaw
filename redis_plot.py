'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper.
Date         : 2021-06-25 21:37:03
LastEditTime : 2021-07-01 00:38:10
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
    x_set_base = [0, 0, 1]
    y_set_base = [0, 0.9361, 1]
    x_set_rep = [0, 0, 1, 2]
    y_set_rep = [0, 0.9283, 1, 1]
    x_set_key = [0, 0, 1, 2]
    y_set_key = [0, 0.8613, 1, 1]
    x_set_size = [0, 0, 1]
    y_set_size = [0, 0.8406, 1]

    x_get_base = [0, 0, 1, 2]
    y_get_base = [0, 0.9374, 0.9999, 1]
    x_get_rep = [0, 0, 1]
    y_get_rep = [0, 0.9311, 0.9999]
    x_get_key = [0, 0, 1]
    y_get_key = [0, 0.8607, 1]
    x_get_size = [0, 0, 1]
    y_get_size = [0, 0.8375, 1]

    fig1, ax1 = plt.subplots()
    ax1.plot(x_set_base, y_set_base, lw=2, marker="o")
    ax1.plot(x_set_rep, y_set_rep, ls="-.", lw=2)
    ax1.plot(x_set_key, y_set_key, ls="--", lw=2, marker="^")
    ax1.plot(x_set_size, y_set_size, ls=":", lw=2)
    ax1.legend(["Baseline", "Replication",
               "Shard by Key Hash", "Shard by Key Size"])
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Cumulative Probability")
    ax1.set_title("CDF of Req Latency of SET")
    ax1.grid(True)
    # plt.show()
    fig1.savefig("set_cdf.pdf", bbox_inches="tight")

    fig2, ax2 = plt.subplots()
    ax2.plot(x_get_base, y_get_base, lw=2, marker="o")
    ax2.plot(x_get_rep, y_get_rep, ls="-.", lw=2)
    ax2.plot(x_get_key, y_get_key, ls="--", lw=2, marker="^")
    ax2.plot(x_get_size, y_get_size, ls=":", lw=2)
    ax2.legend(["Baseline", "Replication",
               "Shard by Key Hash", "Shard by Key Size"])
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Cumulative Probability")
    ax2.set_title("CDF of Req Latency of GET")
    ax2.grid(True)
    # plt.show()
    fig2.savefig("get_cdf.pdf", bbox_inches="tight")

def main():
    # plot_replic()
    # plot_sharding()
    plot_ecdf()


if __name__ == "__main__":
    main()
