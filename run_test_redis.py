'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper.
Date         : 2021-06-23 22:23:06
LastEditTime : 2021-06-25 15:34:40
'''

import sys
import csv
import time
import math
import subprocess
import numpy as np

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

sudo = ""


def read_config():
    try:
        with open("exp_config.txt", "r") as fcon:
            configs = fcon.readlines()
            global sudo
            sudo = str(configs[0].split("\n")[0])
            fcon.close()
    except FileNotFoundError:
        sys.exit("[ERROR] Need a configure file for password, server IP, etc.")


def run_sharding():
    server_proc = subprocess.run(
        "echo " + sudo + " | sudo -S ./redis-server &> /dev/null &",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)
    benchmark_proc = subprocess.run(
        "echo " + sudo + " | sudo -S ./redis-benchmark",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)
    terminate = subprocess.run(
        "echo " + sudo + " | sudo -S pkill -9 redis-server",
        shell=True
    )


def write_shard(fname, raw, mean, stdv):
    with open(fname, "ab") as f:
        np.savetxt(f, raw.astype(int), fmt="%i")
        np.savetxt(f, [mean], fmt="%1.3f")
        np.savetxt(f, [stdv], fmt="%1.3f")
        f.close()


def plot_shard(mean1, mean2, mean3, mean4, stdv1, stdv2, stdv3, stdv4):
    plt.rcParams['ps.fonttype'] = 42
    plt.rcParams['pdf.fonttype'] = 42

    times = np.arange(len(mean1)) + 1
    fig = plt.figure()
    plt.errorbar(times, mean1, yerr=stdv1, marker="o", linewidth=0.6)
    plt.errorbar(times, mean2, yerr=stdv2, marker="*", linewidth=0.6)
    plt.errorbar(times, mean3, yerr=stdv3, marker="^", linewidth=0.6)
    plt.errorbar(times, mean4, yerr=stdv4, marker="x", linewidth=0.6)
    plt.legend(["Shard 1", "Shard 2", "Shard 3", "Shard 4"])
    plt.title("Queries in 4 Shards", fontsize=12)
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel("Queries/s", fontsize=12)
    plt.grid(True)
    fig.savefig("sharding.pdf", bbox_inches="tight")


def post_process(shard1, shard2, shard3, shard4):
    shard1 = np.array(shard1)
    shard2 = np.array(shard2)
    shard3 = np.array(shard3)
    shard4 = np.array(shard4)

    mean1 = shard1.mean(0)
    mean2 = shard2.mean(0)
    mean3 = shard3.mean(0)
    mean4 = shard4.mean(0)

    stdv1 = shard1.std(0)
    stdv2 = shard2.std(0)
    stdv3 = shard3.std(0)
    stdv4 = shard4.std(0)

    write_shard("shard1.csv", shard1, mean1, stdv1)
    write_shard("shard2.csv", shard2, mean2, stdv2)
    write_shard("shard3.csv", shard3, mean3, stdv3)
    write_shard("shard4.csv", shard4, mean4, stdv4)

    plot_shard(mean1, mean2, mean3, mean4, stdv1, stdv2, stdv3, stdv4)


def read_shard(name):
    result = [0]
    with open(name, "r") as fobj:
        content = fobj.readlines()
        for i in range(len(content)):
            reading = int(content[i].split(",")[0])
            if reading == 0:
                break
            else:
                result.append(result[i - 1] + reading)
                if result[0] == 0:
                    result.pop(0)
        fobj.close()
    if len(result) >= 4:
        result.pop(-1)
    return result


def main():
    if len(sys.argv) != 3:
        sys.exit("[ERROR] Usage: python3 run_test_redis.py [test] [repeat time]")
    else:
        print("[INFO] Running", sys.argv[1], sys.argv[2])

    read_config()

    shard1 = []
    shard2 = []
    shard3 = []
    shard4 = []

    if str(sys.argv[1]) == "sharding":
        for i in range(int(sys.argv[2])):
            run_sharding()
            shard1.append(read_shard("sharding_914_results.txt"))
            shard2.append(read_shard("sharding_915_results.txt"))
            shard3.append(read_shard("sharding_916_results.txt"))
            shard4.append(read_shard("sharding_917_results.txt"))
        post_process(shard1, shard2, shard3, shard4)

    elif str(sys.argv[1]) == "replication":
        pass
    else:
        sys.exit("[ERROR] Wrong input!")


if __name__ == "__main__":
    main()
