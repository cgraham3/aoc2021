import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class Problem12a:
    def __init__(self):
        self.node_dict: Dict[str, str] = {}
        self.count = 0

    def get_steps(self, node="start", node_path=[]):
        nptemp = node_path.copy() + [node]
        if node == "end":
            return 1

        nodes: str = self.node_dict[node]
        count = 0
        for n in nodes:
            if n.isupper() or n not in node_path:
                count += self.get_steps(node=n, node_path=nptemp)
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

            self.node_dict[node1].append(node2)
            self.node_dict[node2].append(node1)

        steps = self.get_steps(node="start")

        print(f"Solution to 12a: {steps}")


if __name__ == '__main__':
    problem = Problem12a()
    problem.solve()
