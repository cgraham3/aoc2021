import csv
import itertools
import heapq
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from typing import List, Tuple, Dict


@dataclass(frozen=True, eq=True)
class GameState:
    p1: int
    p1_score: int
    p2: int
    p2_score: int


class Problem21b:
    ROLLS = [
        (3, 1),
        (4, 3),
        (5, 6),
        (6, 7),
        (7, 6),
        (8, 3),
        (9, 1)
    ]

    def solve(self):
        with open("input.txt", "r") as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines]

        p1_start = int(lines[0].strip().split(" ")[-1])
        p2_start = int(lines[1].strip().split(" ")[-1])

        game_states: Dict[GameState, int] = {GameState(p1=p1_start, p1_score=0, p2=p2_start, p2_score=0): 1}

        p1_wins = 0
        p2_wins = 0

        while len(game_states) > 0:
            next_game_states = {}
            for game_state, count in game_states.items():
                for roll_value, num_rolls in self.ROLLS:
                    p1 = ((game_state.p1 + roll_value - 1) % 10) + 1
                    p1_score = game_state.p1_score + p1
                    if p1_score > 20:
                        p1_wins += count * num_rolls
                    else:
                        gs = GameState(p1=p1, p1_score=p1_score, p2=game_state.p2, p2_score=game_state.p2_score)
                        if gs not in next_game_states:
                            next_game_states[gs] = 0
                        next_game_states[gs] += count * num_rolls
            game_states = next_game_states

            next_game_states = {}
            for game_state, count in game_states.items():
                for roll_value, num_rolls in self.ROLLS:
                    p2 = ((game_state.p2 + roll_value - 1) % 10) + 1
                    p2_score = game_state.p2_score + p2
                    if p2_score > 20:
                        p2_wins += count * num_rolls
                    else:
                        gs = GameState(p1=game_state.p1, p1_score=game_state.p1_score, p2=p2, p2_score=p2_score)
                        if gs not in next_game_states:
                            next_game_states[gs] = 0
                        next_game_states[gs] += count * num_rolls
            game_states = next_game_states

        print(f"Solution to 21b: {max(p1_wins, p2_wins)}")
        pass


if __name__ == '__main__':
    import time
    problem = Problem21b()
    start_time = time.time()
    problem.solve()
    print("--- %s seconds ---" % (time.time() - start_time))
