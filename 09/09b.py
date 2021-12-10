import numpy as np
import pandas as pd

from typing import List, Tuple


class Problem09:
    def get_adjacent_not_9(self, x: int, y: int, df: pd.DataFrame) -> List[Tuple[int, int]]:
        adjs = []
        if x - 1 >= 0 and df.iloc[x-1, y] != 9:
            adjs.append((x-1, y))
        if y - 1 >= 0  and df.iloc[x, y-1] != 9:
            adjs.append((x, y-1))
        if x + 1 < df.shape[0] and df.iloc[x+1, y] != 9:
            adjs.append((x+1, y))
        if y + 1 < df.shape[1] and df.iloc[x, y+1] != 9:
            adjs.append((x, y+1))
        return adjs

    def count_cells_in_island(self, x: int, y: int, df: pd.DataFrame):
        counted_cells: List[Tuple[int, int]] = []

        adjs = self.get_adjacent_not_9(x, y, df)
        while len(adjs) > 0:
            new_adjs = []
            for adj in adjs:
                if adj not in counted_cells:
                    counted_cells.append(adj)
                    new_adjs.extend(self.get_adjacent_not_9(adj[0], adj[1], df))
            adjs = new_adjs

        return counted_cells

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        table = []
        for line in lines:
            line = line.replace("\n", "")
            temp = []
            table.append(temp)
            for c in line:
                temp.append(int(c))

        df = pd.DataFrame(table)

        islands = []
        total_counted = []

        for x in range(df.shape[0]):
            for y in range(df.shape[1]):
                if df.iloc[x, y] != 9 and (x, y) not in total_counted:
                    islands.append(self.count_cells_in_island(x, y, df))
                    total_counted.extend(islands[-1])

        lens = [len(island) for island in islands]
        lens.sort(reverse=True)

        print(f"Solution to 9b: {np.product(lens[0:3])}")


if __name__ == '__main__':
    problem = Problem09()
    problem.solve()
