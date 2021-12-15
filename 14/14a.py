import csv

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Problem14a:
    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        rep_dict = {}
        for ix in range(2, len(lines)):
            f, i = lines[ix].strip().split(" -> ")
            rep_dict[f] = i

        input = lines[0].strip()
        steps = 10

        for _ in range(steps):
            ix = 0
            while ix < len(input)-1:
                match = input[ix:ix+2]
                input = input[0:ix+1] + rep_dict[match] + input[ix+1:]
                ix += 2

        uniques = ''.join(set(input))

        unique_lengths = [input.count(unique) for unique in uniques]


        print(f"Solution to 14a: {max(unique_lengths) - min(unique_lengths)}")


if __name__ == '__main__':
    import time
    problem = Problem14a()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
