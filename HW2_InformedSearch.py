# -*- coding: utf-8 -*-
"""
Filename: HW2_InformedSearch.py
Author: Donnel Garner
Date: 2/12/2026
Description: CS480 - Module 3: Informed Search (24-Puzzle)

This program solves the 24-puzzle (5x5 sliding puzzle) using A* search.
The user may choose between two admissible heuristics:

1) h1(x): Number of misplaced tiles
2) h2(x): Sum of Manhattan distances

The program:
- Accepts puzzle input from user
- Checks solvability
- Runs A* search
- Prevents revisiting states
- Includes a timeout safeguard
- Reports performance statistics
"""

import heapq
import time
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Optional, Callable

# ===============================
# Global Constants
# ===============================

N = 5  # 5x5 board
SIZE = N * N

# Goal state configuration - Tuple best for optimization
GOAL = tuple(list(range(1, SIZE)) + [0])

# Precompute goal positions for Manhattan distance
GOAL_POS = {tile: (i // N, i % N) for i, tile in enumerate(GOAL)}


# ===============================
# Input Handling
# ===============================

def parse_input(raw: str) -> Tuple[int]:
    """
    Converts comma-separated string into tuple state.
    Ensures correct formatting and validity.
    """
    nums = [int(x.strip()) for x in raw.split(",")]

    if len(nums) != SIZE:
        raise ValueError("Must enter exactly 25 numbers.")

    if set(nums) != set(range(SIZE)):
        raise ValueError("Numbers must include 0 through 24 exactly once.")

    return tuple(nums)


# ===============================
# Solvability Check
# ===============================

def inversion_count(state):
    """Counts inversions (ignoring blank tile)."""
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv


def is_solvable(state):
    """
    For odd board width (5):
    Puzzle is solvable if inversion count is even.
    """
    return inversion_count(state) % 2 == 0


# ===============================
# Heuristics
# ===============================

def h1_misplaced(state):
    """Counts tiles not in correct position (excluding blank)."""
    return sum(1 for i in range(SIZE)
               if state[i] != 0 and state[i] != GOAL[i])


def h2_manhattan(state):
    """Sum of Manhattan distances for each tile."""
    total = 0
    for index, tile in enumerate(state):
        if tile == 0:
            continue
        r, c = index // N, index % N
        gr, gc = GOAL_POS[tile]
        total += abs(r - gr) + abs(c - gc)
    return total


# ===============================
# Node Structure
# ===============================

@dataclass(order=True)
class PriorityNode:
    f: int
    counter: int
    node: "Node" = field(compare=False)


@dataclass
class Node:
    state: Tuple[int]
    blank_index: int
    g: int
    h: int
    parent: Optional["Node"] = None
    move: Optional[str] = None

    @property
    def f(self):
        return self.g + self.h


# ===============================
# Successor Generation
# ===============================

def generate_successors(state, blank_index):
    """
    Generates valid moves (U, D, L, R).
    """
    moves = []
    r, c = blank_index // N, blank_index % N

    def swap(nr, nc, direction):
        new_index = nr * N + nc
        new_state = list(state)
        new_state[blank_index], new_state[new_index] = \
            new_state[new_index], new_state[blank_index]
        return tuple(new_state), new_index, direction

    if r > 0:
        moves.append(swap(r - 1, c, "U"))
    if r < N - 1:
        moves.append(swap(r + 1, c, "D"))
    if c > 0:
        moves.append(swap(r, c - 1, "L"))
    if c < N - 1:
        moves.append(swap(r, c + 1, "R"))

    return moves


# ===============================
# A* Algorithm with Timeout
# ===============================

def astar(start, heuristic: Callable, timeout_seconds: float):
    """
    Runs A* search with timeout protection.
    """

    start_time = time.perf_counter()

    start_node = Node(
        state=start,
        blank_index=start.index(0),
        g=0,
        h=heuristic(start)
    )

    open_list = []
    heapq.heappush(open_list, PriorityNode(start_node.f, 0, start_node))

    best_g = {start: 0}

    expanded = 0
    generated = 1
    max_frontier = 1
    counter = 1

    while open_list:

        # Timeout check
        if time.perf_counter() - start_time > timeout_seconds:
            return None, {
                "status": "timeout",
                "expanded": expanded,
                "generated": generated,
                "max_frontier": max_frontier
            }

        current = heapq.heappop(open_list).node

        if current.state == GOAL:
            return current, {
                "status": "success",
                "expanded": expanded,
                "generated": generated,
                "max_frontier": max_frontier
            }

        expanded += 1

        for new_state, new_blank, move in generate_successors(
                current.state, current.blank_index):

            new_g = current.g + 1

            # Skip if we have a better path already
            if new_state in best_g and best_g[new_state] <= new_g:
                continue

            best_g[new_state] = new_g
            new_node = Node(
                state=new_state,
                blank_index=new_blank,
                g=new_g,
                h=heuristic(new_state),
                parent=current,
                move=move
            )

            heapq.heappush(open_list,
                           PriorityNode(new_node.f, counter, new_node))
            counter += 1
            generated += 1

        max_frontier = max(max_frontier, len(open_list))

    return None, {
        "status": "failure",
        "expanded": expanded,
        "generated": generated,
        "max_frontier": max_frontier
    }


# ===============================
# Path Reconstruction
# ===============================

def reconstruct_path(node):
    moves = []
    while node.parent:
        moves.append(node.move)
        node = node.parent
    return moves[::-1]


# ===============================
# Main Execution
# ===============================

def main():
    print("24-Puzzle Solver (A* Search)")
    print("Choose heuristic:")
    print("1 - Misplaced Tiles")
    print("2 - Manhattan Distance")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        heuristic = h1_misplaced
    elif choice == "2":
        heuristic = h2_manhattan
    else:
        print("Invalid choice.")
        return

    timeout = float(input("Enter timeout in seconds (e.g., 30): "))

    raw = input("Enter puzzle (comma separated): ")

    try:
        start_state = parse_input(raw)
    except ValueError as e:
        print("Input Error:", e)
        return

    if not is_solvable(start_state):
        print("This puzzle is NOT solvable.")
        return

    print("\nRunning A* search...\n")

    goal_node, stats = astar(start_state, heuristic, timeout)

    if goal_node is None:
        print("Search ended:", stats["status"])
        print("Nodes Expanded:", stats["expanded"])
        print("Nodes Generated:", stats["generated"])
        print("Max Frontier Size:", stats["max_frontier"])
        return

    moves = reconstruct_path(goal_node)

    print("Solution Found!")
    print("Moves:", moves)
    print("Total Moves:", len(moves))
    print("Nodes Expanded:", stats["expanded"])
    print("Nodes Generated:", stats["generated"])
    print("Max Frontier Size:", stats["max_frontier"])


if __name__ == "__main__":
    main()
