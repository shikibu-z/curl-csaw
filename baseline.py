'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper.
Date         : 2021-06-29 01:20:42
LastEditTime : 2021-06-30 14:55:02
'''

import sys
import time
import subprocess
import numpy as np

sudo = ""

try:
    with open("exp_config.txt", "r") as fcon:
        configs = fcon.readlines()
        sudo = str(configs[0].split("\n")[0])
        fcon.close()
except FileNotFoundError:
    sys.exit("[ERROR] Need a configure file for password, server IP, etc.")

results_set = []
results_get = []

for i in range(len(5)):
    server_proc = subprocess.run(
        "echo " + sudo + " | sudo -S ./redis-server &> /dev/null &",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1)
    benchmark_proc = subprocess.check_output(
        "echo " + sudo + " | sudo -S ./redis-benchmark -q -n 500000",
        shell=True
    )
    time.sleep(1)
    terminate = subprocess.run(
        "echo " + sudo + " | sudo -S pkill -9 redis-server",
        shell=True
    )
    benchmark_proc = benchmark_proc.decode().split["\n"]
    results_set.append(float(benchmark_proc[0].split(" ")[1]))
    results_get.append(float(benchmark_proc[1].split(" ")[1]))

results_set = np.array(results_set)
results_get = np.array(results_get)
mean_set = results_set.mean()
stdv_set = results_set.std()
mean_get = results_get.mean()
stdv_get = results_get.std()

with open("base_line_shard_set.csv", "ab") as f:
    np.savetxt(f, [results_set], fmt="%1.3f")
    np.savetxt(f, [mean_set], fmt="%1.3f")
    np.savetxt(f, [stdv_set], fmt="%1.3f")
    f.close()

with open("base_line_shard_get.csv", "ab") as f:
    np.savetxt(f, [results_get], fmt="%1.3f")
    np.savetxt(f, [mean_get], fmt="%1.3f")
    np.savetxt(f, [stdv_get], fmt="%1.3f")
    f.close()
