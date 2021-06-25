'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper at the University of Pennsylvania.
Author       : Junyong Zhao (junyong@seas.upenn.edu)
Date         : 2021-06-23 22:23:06
LastEditors  : Junyong Zhao (junyong@seas.upenn.edu)
LastEditTime : 2021-06-24 20:43:57
'''

import sys
import csv
import time
import math
import subprocess


def run_sharding():
    server_proc = subprocess.run(
        "echo 'junyong' | sudo -S ./redis-server &> /dev/null &",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    benchmark_proc = subprocess.run(
        "echo 'junyong' | sudo -S ./redis-benchmark",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    terminate = subprocess.run(
        "echo 'junyong' | sudo -S pkill -9 redis-server",
        shell=True
    )


def post_process(result):
    pass


def rshard(name):
    result = []
    with open(name, "r") as fobj:
        content = fobj.readlines()
        temp = []
        for i in range(len(content)):
            reading = int(content[i].split(",")[0])
            if reading == 0 and int(content[i - 1].split(",")[0]) != 0:
                temp.pop(-1)
                rsub = []
                rsub.append(temp[0])
                for j in range(len(temp) - 1):
                    rsub.append(temp[j + 1] + rsub[j])
                result.append(rsub)
                temp = []
                # break  # we might do sth different here
            elif reading != 0:
                temp.append(reading)
            else:
                continue
    return result


def main():
    r = rshard("test.txt")
    print(r)


if __name__ == "__main__":
    main()
