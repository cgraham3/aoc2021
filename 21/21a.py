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


class Problem21a:

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines]

        p1_start = int(lines[0].strip().split(" ")[-1])
        p2_start = int(lines[1].strip().split(" ")[-1])

        players = [p1_start, p2_start]
        scores = [0, 0]
        die = Die()

        end = False

        while not end:
            for ix, pos in enumerate(players):
                roll = 0
                for i in range(3):
                    roll += die.roll()
                players[ix] += roll
                players[ix] -= 1
                players[ix] %= 10
                players[ix] += 1
                scores[ix] += players[ix]

                if scores[ix] >= 1000:
                    not_me_score = [score for score in scores if score != scores[ix]][0]
                    s21a = die.roll_count * not_me_score
                    end = True
                    break

        print(f"Solution to 21a: {s21a}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem21a()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
