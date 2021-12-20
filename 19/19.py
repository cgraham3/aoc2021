import csv
import itertools
import heapq
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


# use scanner 0 beacons as relative to everything else
# compare each beacon against scanner 0 in all different orientations & look for duplicate distances
# 12+ = match


@dataclass
class Orientation:
    facing: int
    rotation: int


@dataclass
class Vector:
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"

    def get_rotation(self, index):
        rots = [
            Vector(self.x, self.y, self.z),
            Vector(self.z, self.y, -self.x),
            Vector(-self.x, self.y, -self.z),
            Vector(-self.z, self.y, self.x),
            Vector(self.x, -self.z, self.y),
            Vector(self.x, -self.y, -self.z),
            Vector(self.x, self.z, -self.y),
            Vector(-self.y, self.x, self.z),
            Vector(self.z, self.x, self.y),
            Vector(self.y, self.x, -self.z),
            Vector(-self.z, self.x, -self.y),
            Vector(-self.y, -self.z, self.x),
            Vector(-self.y, -self.x, -self.z),
            Vector(-self.y, self.z, -self.x),
            Vector(-self.x, -self.y, self.z),
            Vector(self.z, -self.y, self.x),
            Vector(-self.z, -self.y, -self.x),
            Vector(-self.x, -self.z, -self.y),
            Vector(-self.x, self.z, self.y),
            Vector(self.y, -self.x, self.z),
            Vector(self.z, -self.x, -self.y),
            Vector(-self.z, -self.x, self.y),
            Vector(self.y, -self.z, -self.x),
            Vector(self.y, self.z, self.x),
        ]
        return rots[index]

    def get_all_rotations(self):
        rots = [
            Vector(self.x, self.y, self.z),
            Vector(self.z, self.y, -self.x),
            Vector(-self.x, self.y, -self.z),
            Vector(-self.z, self.y, self.x),
            Vector(self.x, -self.z, self.y),
            Vector(self.x, -self.y, -self.z),
            Vector(self.x, self.z, -self.y),
            Vector(-self.y, self.x, self.z),
            Vector(self.z, self.x, self.y),
            Vector(self.y, self.x, -self.z),
            Vector(-self.z, self.x, -self.y),
            Vector(-self.y, -self.z, self.x),
            Vector(-self.y, -self.x, -self.z),
            Vector(-self.y, self.z, -self.x),
            Vector(-self.x, -self.y, self.z),
            Vector(self.z, -self.y, self.x),
            Vector(-self.z, -self.y, -self.x),
            Vector(-self.x, -self.z, -self.y),
            Vector(-self.x, self.z, self.y),
            Vector(self.y, -self.x, self.z),
            Vector(self.z, -self.x, -self.y),
            Vector(-self.z, -self.x, self.y),
            Vector(self.y, -self.z, -self.x),
            Vector(self.y, self.z, self.x),
        ]
        return rots


    # def get_all_rotations(self):
    #     x_rots = []
    #     y_rots = []
    #     z_rots = []
    #     for i in range(4):
    #         rad = np.deg2rad(i * 90)
    #         x_rots.append(np.array([
    #             [round(np.cos(rad), 0), round(-np.sin(rad), 0), 0],
    #             [round(np.sin(rad), 0), round(np.cos(rad), 0), 0],
    #             [0, 0, 1]
    #         ]))
    #         y_rots.append(np.array([
    #             [round(np.cos(rad), 0), 0, round(np.sin(rad), 0)],
    #             [0, 1, 0],
    #             [round(-np.sin(rad), 0), 0, round(np.cos(rad), 0)]
    #         ]))
    #         z_rots.append(np.array([
    #             [1, 0, 0],
    #             [0, round(np.cos(rad), 0), round(-np.sin(rad), 0)],
    #             [0, round(np.sin(rad), 0), round(np.cos(rad), 0)]
    #         ]))
    #     rots = {}
    #     input = np.array([[self.x], [self.y], [self.z]])
    #     for rot in x_rots:
    #         for rot2 in y_rots + z_rots:
    #             rots[tuple(list(np.dot(rot2, np.dot(rot, input)).squeeze()))] = 1
    #
    #     return [[int(rot[0]), int(rot[1]), int(rot[2])] for rot in list(rots.keys())]
    # 1 = x, 2 = y, 3 = z
    # [[1, 2, 3], [3, 2, -1], [-1, 2, -3], [-3, 2, 1], [1, -3, 2], [1, -2, -3], [1, 3, -2], [-2, 1, 3], [3, 1, 2],
    #  [2, 1, -3], [-3, 1, -2], [-2, -3, 1], [-2, -1, -3], [-2, 3, -1], [-1, -2, 3], [3, -2, 1], [-3, -2, -1],
    #  [-1, -3, -2], [-1, 3, 2], [2, -1, 3], [3, -1, -2], [-3, -1, 2], [2, -3, -1], [2, 3, 1]]


@ dataclass
class Beacon:
    position: Vector


@dataclass
class Scanner:
    idx: int
    pos: Vector
    orientation: Orientation
    beacons: List[Beacon]
    possible_beacon_rots = None


class Problem19a:
    def build_0_map(self, zero_map, idx, relative_positon_map):
        for f, t in relative_positon_map:
            if t == idx and f not in zero_map:
                zero_map[f] = [f, *zero_map[t]]
                self.build_0_map(zero_map, f, relative_positon_map)

    def find_path_to_0(self, idx, relative_positon_map):
        paths = []
        for f, t in relative_positon_map:
            if f == idx:
                paths.append([f, *self.find_path_to_0(t, relative_positon_map)])
        return []

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines]

        scanner = None
        scanners = []
        for line in lines:
            if "---" in line:
                scanner = Scanner(
                    idx=int(line.split(" ")[2]),
                    pos=Vector(0, 0, 0),
                    orientation=Orientation(-1, -1),
                    beacons=[]
                )
                scanners.append(scanner)
            elif "," in line:
                pos = line.split(",")
                scanner.beacons.append(Beacon(Vector(int(pos[0]), int(pos[1]), int(pos[2]))))

        for scanner in scanners:
            scanner.possible_beacon_rots = np.array([beacon.position.get_all_rotations() for beacon in scanner.beacons]).T.tolist()

        rel_pos = {}

        for scanner1, scanner2 in itertools.permutations(scanners, 2):
            for rot_idx, s2_rot in enumerate(scanner2.possible_beacon_rots):
                distances = {}
                b = False
                for beacon in s2_rot:
                    for s1_beacon in scanner1.beacons:
                        dist = round(np.linalg.norm([
                            beacon.x - s1_beacon.position.x,
                            beacon.y - s1_beacon.position.y,
                            beacon.z - s1_beacon.position.z,
                        ]), 3)
                        if dist not in distances:
                            distances[dist] = [(rot_idx, s1_beacon.position, beacon)]
                        else:
                            distances[dist].append((rot_idx, s1_beacon.position, beacon))
                for _, dist in distances.items():
                    if len(dist) > 11:
                        rot_idx, beacon1, beacon2 = dist[0]
                        rel_pos[scanner1.idx, scanner2.idx] = (rot_idx, Vector(
                            beacon1.x - beacon2.x,
                            beacon1.y - beacon2.y,
                            beacon1.z - beacon2.z
                        ))
                        print(rel_pos[scanner1.idx, scanner2.idx])
                        b = True
                if b:
                    break

        beacons = {}

        path_to_s0 = {
            0: [0]
        }
        self.build_0_map(path_to_s0, 0, rel_pos)
        t_list = []
        for scanner in scanners:
            translations = []
            if scanner.idx != 0:
                last_i = 0
                rot_list = []
                for i in list(reversed(path_to_s0[scanner.idx]))[1:]:
                    v = list(rel_pos[(last_i, i)])
                    for rot in rot_list:
                        v[1] = v[1].get_rotation(rot)
                    rot_list.insert(0, v[0])
                    translations.insert(0, v[1])
                    last_i = i

            pass

            translation = [0, 0, 0]
            for t in translations:
                translation[0] += t.x
                translation[1] += t.y
                translation[2] += t.z
            t_list.append(translation)


            for beacon in scanner.beacons:
                if scanner.idx != 0:
                    v = beacon.position
                    for rot in rot_list:
                        v = v.get_rotation(rot)
                    print(f"{scanner.idx};{v};{translation}")
                    beacons[(
                        translation[0]+v.x,
                        translation[1]+v.y,
                        translation[2]+v.z,
                    )] = 1
                else:
                    print(f"{scanner.idx};{beacon.position};{translation}")
                    beacons[(
                        beacon.position.x,
                        beacon.position.y,
                        beacon.position.z,
                    )] = 1

        max_d = 0
        for b1, b2 in itertools.permutations(t_list, 2):
            d = abs(b1[0] - b2[0]) + abs(b1[1] - b2[1]) + abs(b1[2] - b2[2])
            if d > max_d:
                max_d = d

        print(f"Solution to 19a: {len(beacons)}")
        print(f"Solution to 19b: {max_d}")


if __name__ == '__main__':
    import time
    problem = Problem19a()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
