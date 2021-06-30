'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper.
Date         : 2021-06-23 22:23:06
LastEditTime : 2021-06-30 14:42:53
'''

import sys
import csv
import time
import math
import subprocess
import numpy as np
import matplotlib.pyplot as plt

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


def run_long(para_n, time_out):
    server_proc = subprocess.run(
        "echo " + sudo + " | sudo -S ./redis-server &> /dev/null &",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)
    try:
        benchmark_proc = subprocess.run(
            "echo " + sudo + " | sudo -S ./redis-benchmark -n " + para_n,
            shell=True,
            timeout=time_out,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.TimeoutExpired:
        terminate_benchm = subprocess.run(
            "echo " + sudo + " | sudo -S pkill -9 redis-benchmark",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        terminate_server = subprocess.run(
            "echo " + sudo + " | sudo -S pkill -9 redis-server",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


def write_shard(fname, raw, mean, stdv):
    with open(fname, "ab") as f:
        np.savetxt(f, raw.astype(int), fmt="%i")
        np.savetxt(f, [mean], fmt="%1.3f")
        np.savetxt(f, [stdv], fmt="%1.3f")
        f.close()


def post_shard(shard1, shard2, shard3, shard4):
    minlen1 = min(map(len, shard1))
    minlen2 = min(map(len, shard2))
    minlen3 = min(map(len, shard3))
    minlen4 = min(map(len, shard4))
    minlen = min([minlen1, minlen2, minlen3, minlen4])

    for i in range(len(shard1)):
        shard1[i] = shard1[i][: minlen]
        shard1[i].pop(-1)
    for i in range(len(shard2)):
        shard2[i] = shard2[i][: minlen]
        shard2[i].pop(-1)
    for i in range(len(shard3)):
        shard3[i] = shard3[i][: minlen]
        shard3[i].pop(-1)
    for i in range(len(shard4)):
        shard4[i] = shard4[i][: minlen]
        shard4[i].pop(-1)

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


def post_replic(replication):
    replication = np.array(replication)
    mean = replication.mean(0)
    stdv = replication.std(0)
    with open("replic.csv", "ab") as f:
        np.savetxt(f, replication.astype(int), fmt="%i")
        np.savetxt(f, [mean], fmt="%1.3f")
        np.savetxt(f, [stdv], fmt="%1.3f")
        f.close()


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
    return result


def read_replic():
    result = []
    with open("results.txt", "r") as fobj:
        content = fobj.readlines()
        for i in range(len(content)):
            reading = content[i].split(",")[0]
            if reading == "Replication checkpoint...\n":
                continue
            reading = int(reading)
            if reading == 0:
                break
            else:
                result.append(reading)
        fobj.close()
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

    replication = []

    if str(sys.argv[1]) == "sharding":
        for i in range(int(sys.argv[2])):
            run_long(500000, 150)
            print("[info] finish one, left", int(sys.argv[2]) - 1)
            shard1.append(read_shard("sharding_914_results.txt"))
            shard2.append(read_shard("sharding_915_results.txt"))
            shard3.append(read_shard("sharding_916_results.txt"))
            shard4.append(read_shard("sharding_917_results.txt"))
        post_shard(shard1, shard2, shard3, shard4)

    elif str(sys.argv[1]) == "replication":
        for i in range(int(sys.argv[2])):
            run_long(3500000, 150)
            print("[info] finish one, left", int(sys.argv[2]) - 1)
            replication.append(read_replic())
            subprocess.run(
                "echo " + sudo + " | sudo -S rm results.txt",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        minlen = min(map(len, replication))
        for i in range(len(replication)):
            replication[i] = replication[i][: minlen]
        post_replic(replication)

    else:
        sys.exit("[ERROR] Wrong input!")


if __name__ == "__main__":
    main()
