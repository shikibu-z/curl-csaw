'''
Description  : This is the evaluation script that compare number increase from
input files. This file is a part of the csaw paper.
Date         : 2021-06-19 13:24:35
LastEditTime : 2021-06-24 22:23:52
'''

import os
import sys
import csv
import math


def main():
    if len(sys.argv) != 3:
        sys.exit("[ERROR] Usage: python3 [file1] [file2]!")
    elif not os.path.exists(str(sys.argv[1])) or not os.path.exists(str(sys.argv[2])):
        sys.exit("[ERROR] Wrong file names!")
    else:
        print("[STATUS] Comparing:", sys.argv[1], sys.argv[2])

    file1 = str(sys.argv[1]).split("-")
    file2 = str(sys.argv[2]).split("-")

    if file1[2] != file2[2] or file1[3] != file2[3] or file1[1] == file2[1]:
        sys.exit(
            "[ERROR] Compare: you may want to compare different binaries in the same setup!")

    # read mean from a csv file
    buf = []
    with open(str(sys.argv[1]), "r") as f1:
        reader = csv.reader(f1)
        for i in reader:
            buf.append(i)
        f1.close()
    mean1 = float(buf[2][0])
    buf = []
    with open(str(sys.argv[2]), "r") as f2:
        reader = csv.reader(f2)
        for i in reader:
            buf.append(i)
        f2.close()
    mean2 = float(buf[2][0])

    # compute percentage increase
    increase = 0
    if file1[1] == "base":
        increase = round((mean2 - mean1) / mean1 * 100, 2)
        with open(file1[2] + "-" + file1[3] + "-" + file2[4].split(".")[0] + "-increase", "w") as result:
            print("compart increase percentage:",
                  str(increase) + "%", file=result)
        result.close()

    else:
        increase = round((mean1 - mean2) / mean2 * 100, 2)
        with open(file2[2] + "-" + file2[3] + "-" + file1[4].split(".")[0] + "-increase", "w") as result:
            print("compart increase percentage:",
                  str(increase) + "%", file=result)
        result.close()


if __name__ == "__main__":
    main()
