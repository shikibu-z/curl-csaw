'''
Description  : This is the evaluation script that runs experiments. This file 
is a part of the csaw paper at the University of Pennsylvania.
Author       : Junyong Zhao (junyong@seas.upenn.edu)
Date         : 2021-06-19 13:24:35
LastEditors  : Junyong Zhao (junyong@seas.upenn.edu)
LastEditTime : 2021-06-24 22:21:06
'''

import sys
import csv
import time
import math
import subprocess

sudo = ""
monitor = ""
server = ""


def read_config():
    try:
        with open("exp_config.txt", "r") as fcon:
            configs = fcon.readlines()
            global sudo
            global monitor
            global server
            sudo = str(configs[0].split("\n")[0])
            monitor = str(configs[1].split("\n")[0])
            server = str(configs[2].split("\n")[0])
    except FileNotFoundError:
        sys.exit("[ERROR] Need a configure file for password, server IP, etc.")


def compart_process(cmd1, cmd2, repeat_time, times, return_code, mean):
    """Run the modified version of cURL"""
    for i in range(repeat_time):
        monitor_start = subprocess.run(
            cmd1, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        start_time = time.time()
        result = subprocess.run(cmd2, shell=True)
        end_time = time.time()
        times.append(end_time - start_time)
        return_code.append(result.returncode)
        mean += (end_time - start_time)
    return times, return_code, mean


def compute_stdv(times, mean, repeat_time):
    """Compute standard deviation"""
    stdv = 0
    for i in range(repeat_time):
        stdv += (times[i] - mean) ** 2
    stdv /= repeat_time
    stdv = math.sqrt(stdv)
    return stdv


def write_result(csv_name, times, return_code, mean, stdv):
    """Write results to a csv file"""
    with open(csv_name + ".csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(times)
        writer.writerow(return_code)
        writer.writerow([mean])
        writer.writerow([stdv])
        f.close()


def main():
    if len(sys.argv) != 5:
        sys.exit(
            "[ERROR] Usage: python3 test.py [curl-version] [file-name] [repeat time] [machine choice]")
    else:
        print("[STATUS] Running:", sys.argv[1],
              sys.argv[2], sys.argv[3], sys.argv[4])

    read_config()

    curl = str(sys.argv[1])
    file_name = str(sys.argv[2])
    repeat_time = int(sys.argv[3])
    machine = str(sys.argv[4])

    times = []
    return_code = []
    mean = 0
    stdv = 0
    csv_name = curl + "-" + \
        file_name.split(".")[0] + "-" + str(repeat_time) + "-" + machine

    # the baseline curl
    if curl == "curl-base" and machine == "local":
        # change this sudo password and URL for your own test
        cmd = "echo " + sudo + " | sudo -S ./curl-base " + \
            server + file_name + " --output /dev/null"
        for i in range(repeat_time):
            time.sleep(1)
            start_time = time.time()
            result = subprocess.run(cmd, shell=True)
            end_time = time.time()
            times.append(end_time - start_time)
            return_code.append(result.returncode)
            mean += (end_time - start_time)

    # modified version on the same machine
    elif curl == "curl-compart" and machine == "local":
        # change this sudo password and URL for your own test
        cmd1 = "echo " + sudo + " | sudo -S ./curl-monitor " + \
            server + file_name + " --output /dev/null &"
        cmd2 = "echo " + sudo + " | sudo -S ./curl-compart " + \
            server + file_name + " --output /dev/null"
        times, return_code, mean = compart_process(
            cmd1, cmd2, repeat_time, times, return_code, mean)

    # modified version on seperate VMs
    elif curl == "curl-compart" and machine == "cross":
        # change this sudo password and URL for your own test
        cmd1 = "screen -dm sshpass -p '" + sudo + "' ssh " + monitor + " 'echo " + \
            sudo + " | sudo -S ./curl-monitor " + server + file_name + " --output /dev/null'"
        cmd2 = "echo " + sudo + " | sudo -S ./curl-compart " + \
            server + file_name + " --output /dev/null"
        times, return_code, mean = compart_process(
            cmd1, cmd2, repeat_time, times, return_code, mean)

    else:
        sys.exit("[ERROR] Wrong input combination!")

    mean /= repeat_time
    stdv = compute_stdv(times, mean, repeat_time)
    print("mean:", mean)
    print("stdv:", stdv)
    print(times)
    write_result(csv_name, times, return_code, mean, stdv)


if __name__ == "__main__":
    main()
