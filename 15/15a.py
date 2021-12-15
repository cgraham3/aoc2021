import csv

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Problem15a:
    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        input = []
        for line in lines:
            input.append([int(c) for c in list(line.strip())])

        grid = np.array(input)

        sums = grid.copy()

        for i in reversed(range(grid.shape[1])):
            for j in reversed(range(grid.shape[0])):
                if i + 1 < grid.shape[1] and j + 1 < grid.shape[0]:
                    sums[i, j] += min(sums[i + 1, j], sums[i, j + 1])
                elif i + 1 < grid.shape[1]:
                    sums[i, j] += sums[i + 1, j]
                elif j + 1 < grid.shape[0]:
                    sums[i, j] += sums[i, j + 1]

        sums -= grid

        print(f"Solution to 15a: {sums[0, 0]}")


if __name__ == '__main__':
    import time
    problem = Problem15a()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
