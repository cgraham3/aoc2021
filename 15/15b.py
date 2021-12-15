import csv
import itertools
import heapq
import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


class PriorityQueue:
    """https://docs.python.org/3/library/heapq.html"""
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def add_task(self, task, priority=0):
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)
        pass

    def remove_task(self, task):
        entry = self.entry_finder.pop(task)
        entry[-1] = "REMOVED"
        pass

    def pop_task(self):
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task != "REMOVED":
                del self.entry_finder[task]
                return task, priority
        return None, None


class Problem15b:

    def dijkstra(self, grid):
        """https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm"""
        prev = {(i, j): np.nan for i in range(grid.shape[0]) for j in range(grid.shape[1])}
        pq = PriorityQueue()
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                pq.add_task((i, j), priority=int(10e6))
        pq.remove_task((0,0))
        pq.add_task((0,0), priority=0)
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while True:
            u, u_prio = pq.pop_task()
            if u is None:
                break

            for neighbor in neighbors:
                v = (u[0] + neighbor[0], u[1] + neighbor[1])
                if v not in pq.entry_finder or pq.entry_finder[v] == "REMOVED":
                    continue
                if 0 <= v[0] < grid.shape[0] and 0 <= v[1] < grid.shape[1]:
                    entry = pq.entry_finder[v]
                    alt = u_prio + grid[v]
                    if alt < entry[0]:
                        pq.remove_task(v)
                        pq.add_task(v, priority=alt)
                        prev[v] = u

        S = []
        u = (grid.shape[0]-1, grid.shape[1]-1)
        while True:
            S.insert(0, u)
            u = prev[u]
            if u == (0, 0) or u == np.nan:
                break

        total = 0
        for node in S:
            total += grid[node]

        return total

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        input = []
        for line in lines:
            input.append([int(c) for c in list(line.strip())])

        expanded_multiple = 5

        grid = np.array(input)
        grid_expanded = np.zeros(shape=np.multiply(grid.shape, expanded_multiple))
        for i in range(grid.shape[1]):
            for j in range(grid.shape[0]):
                for k in range(expanded_multiple):
                    for m in range(expanded_multiple):
                        val = grid[i, j] + (k+m)
                        if val > 9:
                            val %= 10
                            val += 1
                        grid_expanded[i + k*grid.shape[1], j + m*grid.shape[0]] = val

        soln = self.dijkstra(grid_expanded)

        print(f"Solution to 15b: {soln}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem15b()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
