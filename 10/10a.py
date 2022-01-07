import numpy as np
import pandas as pd

from typing import List, Tuple


class Problem10:
    def get_score(self, c):
        if c == ")":
            return 3
        if c == "]":
            return 57
        if c == "}":
            return 1197
        if c == ">":
            return 25137
        return 0

    def parse_line(self, line) -> str:
        while True:
            line = line.replace("[]", "")
            line = line.replace("{}", "")
            line = line.replace("<>", "")
            line = line.replace("()", "")
            if not any(t in line for t in ["[]", "{}", "<>", "()"]):
                break
        idxs = [(b, line.index(b)) for b in ["]", ")", "}", ">"] if b in line]
        if len(idxs) == 0:
            return ""
        idxs.sort(key=lambda x: x[1])
        return idxs[0][0]

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        for ix, line in enumerate(lines):
            lines[ix] = line.replace("\n", "")
        score = sum([self.get_score(self.parse_line(line)) for line in lines])
        print(f"Solution to 10a: {score}")


if __name__ == '__main__':

    test = "[{[{({}]{}}([{[{{{}}([]"
    problem = Problem10()
    x = problem.parse_line(test)
    problem.solve()
