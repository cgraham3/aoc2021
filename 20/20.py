import csv
import itertools
import heapq
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Problem20:

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines]

        key = [int(c) for c in lines[0].replace("#", "1").replace(".", "0")]
        grid = []
        for line in lines[2:]:
            grid.append([int(c) for c in line.replace("#", "1").replace(".", "0")])

        grid = np.array(grid)
        grid = np.pad(grid, (100, 100))

        for idx in range(50):
            output = np.zeros(shape=grid.shape)
            world = key[int(str(int(grid[0, 0])) * 9, 2)]
            not_world = int(not bool(world))
            #for i in range(50-idx, grid.shape[0]-49+idx):
            #    for j in range(50-idx, grid.shape[1]-49+idx):
            for i in range(1, grid.shape[0]-1):
                for j in range(1, grid.shape[0]-1):
                    st = ""
                    for c in list(grid[i - 1:i + 2, j - 1:j + 2].flatten()):
                        st += str(int(c))
                    x = int(st, 2)
                    output[i, j] = key[x]

            for i in [0, grid.shape[0]-1]:
                for j in range(grid.shape[0]):
                    output[i, j] = world
                    output[j, i] = world

            grid = output

            if idx == 1:
                asoln = np.sum(grid)

        print(f"Solution to 20a: {asoln}")
        print(f"Solution to 20b: {np.sum(grid)}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem20()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
