'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper at the University of Pennsylvania.
Author       : Junyong Zhao (junyong@seas.upenn.edu)
Date         : 2021-06-23 22:23:06
LastEditors  : Junyong Zhao (junyong@seas.upenn.edu)
LastEditTime : 2021-06-24 22:18:25
'''

import sys
import csv
import time
import math
import subprocess

sudo = ""


def read_config():
    try:
        with open("exp_config.txt", "r") as fcon:
            configs = fcon.readlines()
            global sudo
            sudo = str(configs[0].split("\n")[0])
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


def post_process(result):
    pass


def rshard(name):
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
    return result


def main():
    r = rshard("test.txt")
    print(r)


if __name__ == "__main__":
    main()
