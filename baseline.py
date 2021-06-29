'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper.
Date         : 2021-06-29 01:20:42
LastEditTime : 2021-06-29 01:34:10
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

results = []

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
    results.append(float(benchmark_proc[1].split(" ")[1]))

results = np.array(results)
mean = results.mean()
stdv = results.std()

with open("base_line_shard.csv", "ab") as f:
    np.savetxt(f, [results], fmt="%1.3f")
    np.savetxt(f, [mean], fmt="%1.3f")
    np.savetxt(f, [stdv], fmt="%1.3f")
    f.close()
