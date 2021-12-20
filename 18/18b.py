import csv
import itertools
import heapq
import math

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Pair:
    def __init__(self, x, y, level):
        self.parent = None
        self.x = x
        self.y = y
        self.level = level

    def get_maginitude(self):
        mag = 3 * (self.x.get_maginitude() if isinstance(self.x, Pair) else self.x)
        mag += 2 * (self.y.get_maginitude() if isinstance(self.y, Pair) else self.y)
        return mag

    def increase_level(self):
        if isinstance(self.x, Pair):
            self.x.increase_level()
        if isinstance(self.y, Pair):
            self.y.increase_level()
        self.level += 1

    def explode(self):
        if isinstance(self.x, Pair):
            self.x.explode()
        if isinstance(self.y, Pair):
            self.y.explode()
        if isinstance(self.x, int) and isinstance(self.y, int):
            self.parent.add_left(self.x, self)
            self.parent.add_right(self.y, self)

    def find_root(self) -> "Pair":
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    def handle_splits(self) -> bool:
        if isinstance(self.x, Pair):
            if not self.x.handle_splits():
                if isinstance(self.y, Pair):
                    return self.y.handle_splits()
                elif self.y > 9:
                    self.y = Pair(math.floor(self.y / 2), math.ceil(self.y / 2), self.level + 1)
                    self.y.parent = self
                    return True
            else:
                return True
        elif self.x > 9:
            self.x = Pair(math.floor(self.x / 2), math.ceil(self.x / 2), self.level + 1)
            self.x.parent = self
            return True

        elif isinstance(self.y, Pair):
            return self.y.handle_splits()
        elif self.y > 9:
            self.y = Pair(math.floor(self.y / 2), math.ceil(self.y / 2), self.level+1)
            self.y.parent = self
            return True
        return False

    def handle_explode(self) -> bool:
        if isinstance(self.x, int) and isinstance(self.y, int) and self.level > 3:
            self.explode()  # boom!
            if self.parent.x == self:
                self.parent.x = 0
            elif self.parent.y == self:
                self.parent.y = 0
            return True
        else:
            if isinstance(self.x, Pair):
                if not self.x.handle_explode():
                    if isinstance(self.y, Pair):
                        return self.y.handle_explode()
                else:
                    return True
            elif isinstance(self.y, Pair):
                return self.y.handle_explode()
            return False

    def add_left(self, val, from_node: "Pair"):
        if from_node == self.x:
            if self.parent is not None:
                self.parent.add_left(val, self)
        else:
            if isinstance(self.y, int):
                self.y += val
            elif self.y != from_node:
                self.y.add_left(val, self)
            elif isinstance(self.x, int):
                self.x += val
            elif self.x != from_node:
                self.x.add_left(val, self)
            else:
                raise Exception("please no")

    def add_right(self, val, from_node):
        if from_node == self.y:
            if self.parent is not None:
                self.parent.add_right(val, self)
        else:
            if isinstance(self.x, int):
                self.x += val
            elif self.x != from_node:
                self.x.add_right(val, self)
            elif isinstance(self.y, int):
                self.y += val
            elif self.y != from_node:
                self.y.add_right(val, self)

    def __repr__(self):
        return f"[{self.x.__repr__()},{self.y.__repr__()}]"


class Problem18a:
    def parse_line(self, line):
        print(line)
        pair = self.parse_pair(line)
        print(pair)
        while pair.handle_explode():
            pair.handle_splits()
            pass
        print(pair)

    def parse_pair(self, line, level=0) -> Pair:
        line = line[1:-1]
        tmp_splits = line.split(",")
        if "[" not in tmp_splits[0]:
            x = int(tmp_splits[0])
            yline = line[len(tmp_splits[0])+1:]
            if "," not in yline:
                y = int(yline)
            else:
                y = self.parse_pair(yline, level+1)
            pair = Pair(x, y, level)
            if isinstance(x, Pair):
                x.parent = pair
            if isinstance(y, Pair):
                y.parent = pair
            return pair
        else:
            bracket_ct = 0
            for ix, c in enumerate(line):
                if c == "[":
                    bracket_ct += 1
                elif c == "]":
                    bracket_ct -= 1
                elif c == "," and bracket_ct == 0:
                    xline = line[:ix]
                    yline = line[ix+1:]
                    if "," not in xline:
                        x = int(xline)
                    else:
                        x = self.parse_pair(xline, level+1)
                    if "," not in yline:
                        y = int(yline)
                    else:
                        y = self.parse_pair(yline, level+1)
                    pair = Pair(x, y, level)
                    if isinstance(x, Pair):
                        x.parent = pair
                    if isinstance(y, Pair):
                        y.parent = pair
                    return pair
        raise Exception("https://i.kym-cdn.com/entries/icons/original/000/018/489/nick-young-confused-face-300x256-nqlyaa.jpg")

    def add_pair(self, p1: Pair, p2: Pair) -> Pair:
        p1.increase_level()
        p2.increase_level()
        pair = Pair(p1, p2, 0)
        p1.parent = pair
        p2.parent = pair
        return pair

    def reduce_pair(self, pair):
        while True:
            if pair.handle_explode():
                continue
            if pair.handle_splits():
                continue
            break
        return pair

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines]

        pairs = []

        for line in lines:
            pairs.append(self.parse_pair(line))

        perms = itertools.permutations(lines, 2)
        max_mag = 0
        for l1, l2 in perms:
            p1 = self.parse_pair(l1)
            p2 = self.parse_pair(l2)
            pair = self.add_pair(p1, p2)
            self.reduce_pair(pair)
            mag = pair.get_maginitude()
            if mag > max_mag:
                max_mag = mag

        print(f"Solution to 18a: {max_mag}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem18a()

    # problem.parse_line("[[[[[9,8],1],2],3],4]")
    # problem.parse_line("[7,[6,[5,[4,[3,2]]]]]")
    # problem.parse_line("[[6,[5,[4,[3,2]]]],1]")
    # problem.parse_line("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    # problem.parse_line("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")

    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
