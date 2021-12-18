import csv
import itertools
import heapq
import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Problem17b:
    def check_trajectory(self, vix, viy, xmin, xmax, ymin, ymax) -> Tuple[bool, int, int, int]:
        vx = vix
        vy = viy
        x, y = 0, 0
        max_y = y
        while x < xmax and y > ymin:
            x += vx
            y += vy
            if y > max_y:
                max_y = y
            vx = max(0, vx - 1)
            vy -= 1
            if xmin <= x <= xmax and ymin <= y <= ymax:
                return True, max_y, x, y

        return False, max_y, x, y


    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        line = lines[0].strip().split(": ")[1]
        xs, ys = line.split(", ")
        xs = [int(x) for x in xs.split("=")[1].split("..")]
        ys = [int(y) for y in ys.split("=")[1].split("..")]
        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)

        y_max = 0
        y_max_pos = (0, 0)

        hits = {}
        mult = 5
        for viy in range(min(ys)*mult, max(xs)*mult):
            for vix in range(xmax*mult):
                hit, peak_y, last_x, last_y = self.check_trajectory(vix, viy, xmin, xmax, ymin, ymax)
                if hit:
                    hits[(vix, viy)] = 1
                if hit and peak_y > y_max:
                    y_max = max(y_max, peak_y)
                    y_max_pos = (vix, viy)

        print(f"Solution to 17b: {len(hits.keys())}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem17b()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
