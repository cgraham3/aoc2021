import numpy as np
import pandas as pd

from typing import List, Tuple


class Problem10:
    def get_char_score(self, c):
        if c == "(":
            return 1
        if c == "[":
            return 2
        if c == "{":
            return 3
        if c == "<":
            return 4
        return 0

    def parse_line(self, line) -> int:
        score = 0
        while len(line) > 0:
            line = line.replace("[]", "")
            line = line.replace("{}", "")
            line = line.replace("<>", "")
            line = line.replace("()", "")
            if not any(t in line for t in ["[]", "{}", "<>", "()"]):
                idxs = [(b, line.rfind(b)) for b in ["[", "(", "{", "<"] if b in line]
                if len(idxs) == 0:
                    return 0
                idxs.sort(key=lambda x: x[1])
                score *= 5
                c = idxs[-1][0]
                score += self.get_char_score(c)
                line_idx = line.rfind(c)
                if line[-1] != c:
                    return 0
                line = line[:line_idx] + line[line_idx+1:]
        return score

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        for ix, line in enumerate(lines):
            lines[ix] = line.replace("\n", "")

        scores = [score for score in [self.parse_line(line) for line in lines] if score != 0]
        scores.sort()
        print(f"Solution to 10b: {scores[len(scores)//2]}")


if __name__ == '__main__':
    problem = Problem10()
    problem.solve()
