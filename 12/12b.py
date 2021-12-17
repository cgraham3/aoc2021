import csv

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Problem12b:
    def __init__(self):
        self.node_dict: Dict[str, str] = {}
        self.count = 0

    def get_steps(self, node="start", node_path=[], twice=False):
        nptemp = node_path.copy() + [node]
        if node == "end":
            self.count += 1
            print(self.count)
            return 1

        nodes: str = self.node_dict[node]
        count = 0
        for n in nodes:
            if twice and n.islower() and n in node_path:
                continue
            if n.isupper() or node_path.count(n) < 2:
                count += self.get_steps(
                    node=n,
                    node_path=nptemp,
                    twice=twice or (n.islower() and node_path.count(n) == 1)
                )
        return count

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        self.node_dict = {}
        for line in lines:
            line = line.replace("\n", "")
            node1, node2 = line.split("-")
            if node1 not in self.node_dict:
                self.node_dict[node1] = []
            if node2 not in self.node_dict:
                self.node_dict[node2] = []

            if node2 != "start":
                self.node_dict[node1].append(node2)
            if node1 != "start":
                self.node_dict[node2].append(node1)

        steps = self.get_steps(node="start")
        print(f"Solution to 12b: {steps}")


if __name__ == '__main__':
    import time
    problem = Problem12b()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
