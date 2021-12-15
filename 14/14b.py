import csv

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Problem14b:
    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        rep_dict = {}
        unique_dict = {}
        for ix in range(2, len(lines)):
            f, i = lines[ix].strip().split(" -> ")
            rep_dict[f] = i
            unique_dict[i] = 0
            unique_dict[f[0]] = 0
            unique_dict[f[1]] = 0

        input = lines[0].strip()
        steps = 40

        pair_dict = {input[ix:ix+2]: 1 for ix in range(len(input)-1)}
        pair_dict_temp = {}

        for i in input:
            unique_dict[i] += 1

        for _ in range(steps):
            print(_)
            for pair in pair_dict:
                insert = rep_dict[pair]
                unique_dict[insert] += pair_dict[pair]

                new_pair = pair[0] + insert
                if new_pair not in pair_dict_temp:
                    pair_dict_temp[new_pair] = 0
                pair_dict_temp[new_pair] += pair_dict[pair]

                new_pair = insert + pair[1]
                if new_pair not in pair_dict_temp:
                    pair_dict_temp[new_pair] = 0
                pair_dict_temp[new_pair] += pair_dict[pair]

            pair_dict = pair_dict_temp
            pair_dict_temp = {}

        print(f"Solution to 14b: {max(list(unique_dict.values())) - min(list(unique_dict.values()))}")


if __name__ == '__main__':
    import time
    problem = Problem14b()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
