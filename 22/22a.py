import csv
import itertools
import heapq
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Die:
    def __init__(self):
        self.last_roll = 0
        self.roll_count = 0

    def roll(self) -> int:
        self.last_roll += 1
        self.last_roll %= 100
        self.roll_count += 1
        return self.last_roll


class Problem22a:

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines]

        grid = np.zeros(shape=(101, 101, 101))
        offset = 50

        for line in lines:
            line = line.replace("=", "").replace("x", "").replace("y", "").replace("z", "")
            action, extra = line.split(" ")
            x, y, z = extra.split(",")
            xmin, xmax = [int(i) for i in x.split("..")]
            ymin, ymax = [int(i) for i in y.split("..")]
            zmin, zmax = [int(i) for i in z.split("..")]

            if xmin + offset < 0 or xmax + offset > 100 \
                    or ymin + offset < 0 or ymax + offset > 100 \
                    or zmin + offset < 0 or zmax + offset > 100:
                continue

            grid[
                xmin+offset:xmax+offset+1,
                ymin+offset:ymax+offset+1,
                zmin+offset:zmax+offset+1,
            ] = 1 if action == "on" else 0

        print(f"Solution to 21a: {np.sum(grid)}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem22a()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
