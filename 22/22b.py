import csv
import itertools
import heapq
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Cube:
    def __init__(self, x, y, z, on):
        self.zmax = max(z)
        self.zmin = min(z)
        self.ymax = max(y)
        self.ymin = min(y)
        self.xmax = max(x)
        self.xmin = min(x)
        self.on = on

    def count(self) -> int:
        return (self.xmax - self.xmin + 1) * (self.ymax - self.ymin + 1) * (self.zmax - self.zmin + 1)

    def check_overlap(self, cube):
        return self.xmax >= cube.xmin and self.xmin <= cube.xmax and self.ymax >= cube.ymin and self.ymin <= cube.ymax and self.zmax >= cube.zmin and self.zmin <= cube.zmax

    def subtract(self, cube) -> List["Cube"]:
        if not self.check_overlap(cube):
            return [self]

        x_min = self.xmin
        y_min = self.ymin
        z_min = self.zmin
        x_max = self.xmax
        y_max = self.ymax
        z_max = self.zmax

        sub_cubes = []
        if x_min < cube.xmin:
            sub_cubes.append(Cube((x_min, cube.xmin - 1), (y_min, y_max), (z_min, z_max), on=True))
            x_min = cube.xmin
        if x_max > cube.xmax:
            sub_cubes.append(Cube((cube.xmax + 1, x_max), (y_min, y_max), (z_min, z_max), on=True))
            x_max = cube.xmax
        if y_min < cube.ymin:
            sub_cubes.append(Cube((x_min, x_max), (y_min, cube.ymin - 1), (z_min, z_max), on=True))
            y_min = cube.ymin
        if y_max > cube.ymax:
            sub_cubes.append(Cube((x_min, x_max), (cube.ymax + 1, y_max), (z_min, z_max), on=True))
            y_max = cube.ymax
        if z_min < cube.zmin:
            sub_cubes.append(Cube((x_min, x_max), (y_min, y_max), (z_min, cube.zmin - 1), on=True))
        if z_max > cube.zmax:
            sub_cubes.append(Cube((x_min, x_max), (y_min, y_max), (cube.zmax + 1, z_max), on=True))

        return sub_cubes

    def __repr__(self):
        return f"[v1=({self.xmin},{self.ymin},{self.zmin}) v2=({self.xmax},{self.ymax},{self.zmax}), on={self.on}, count={self.count()}]"


class Problem22b:

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines]
        cubes: List[Cube] = []

        for line in lines:
            line = line.replace("=", "").replace("x", "").replace("y", "").replace("z", "")
            action, extra = line.split(" ")
            x, y, z = extra.split(",")
            xmin, xmax = [int(i) for i in x.split("..")]
            ymin, ymax = [int(i) for i in y.split("..")]
            zmin, zmax = [int(i) for i in z.split("..")]

            cube = Cube((xmin, xmax), (ymin, ymax), (zmin, zmax), action == "on")
            cubes.append(cube)

        done_cubes = []
        for ix, cube in enumerate(cubes):
            new_cubes = []
            for done_cube in done_cubes:
                new_cubes.extend(done_cube.subtract(cube))
            done_cubes = new_cubes
            if cube.on:
                done_cubes.append(cube)
        total_on = sum([cube.count() for cube in done_cubes])
        print(total_on)

        print(f"Solution to 22b: {np.sum(total_on)}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem22b()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
