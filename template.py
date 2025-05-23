import functools
import heapq
import itertools
import os
import re
import string
import sys
import time
from collections import defaultdict, deque
from pprint import pprint

import networkx
import z3
from more_itertools import (
    collapse,  # flatten all levels of nested iterables
    consume,  # exhaust an iterable
    distinct_combinations,  # distinct combinations of elements from an iterable
    distinct_permutations,  # distinct permutations of elements from an iterable
    islice_extended,  # extended slicing capabilities (islice with [::] and negative indices)
    mark_ends,  # mark the first and last element of an iterable ((is_first, is_last, val), (is_first, is_last, val), ...)
    minmax,  # find the minimum and maximum of an iterable (same as lambda x: (min(x), max(x)))
    peekable,  # peek ahead in an iterable
    sliding_window,  # return a sliding window of an iterable
    time_limited,  # time-limited execution of a function
)


def parseLine(line):
    return line


def parseLines(lines):
    return [parseLine(line) for line in lines]


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def numsNested(
    data: str | list[str] | list[list[str]],
) -> tuple[int | tuple[int, ...], ...]:
    if isinstance(data, str):
        return nums(data)
    if not hasattr(data, "__iter__"):
        raise ValueError("Data must be a tuple/list/iterable or a string")
    return tuple(e[0] if len(e) == 1 else e for e in filter(len, map(numsNested, data)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(test=test).strip("\n").split("\n")

        # self.data = parseLines(data)
        # self.data = list(map(list, self.data))

    def part1(self):
        return None

    def part2(self):
        return None

    def part3(self):
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == None else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == None else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == None else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


def neighbors4(point: tuple[int, ...], jump=1):
    for i in range(len(point)):
        for diff in (-jump, jump):
            yield point[:i] + (point[i] + diff,) + point[i + 1 :]


def neighbors8(point: tuple[int, ...], jump=1):
    for diff in itertools.product((-jump, 0, jump), repeat=len(point)):
        if any(diff):
            yield tuple(point[i] + diff[i] for i in range(len(point)))


def manhattan(p1: tuple[int, ...], p2: tuple[int, ...]):
    return sum(abs(a - b) for a, b in zip(p1, p2))


def get_close_points(
    point: tuple[int, int], max_distance: int, include_self: bool = True
):
    """
    Get all points within a certain manhattan distance from a point
    """
    x, y = point
    if include_self:
        yield x, y
    for distance in range(max_distance + 1):
        for offset in range(distance):
            invOffset = distance - offset
            yield x + offset, y + invOffset
            yield x + invOffset, y - offset
            yield x - offset, y - invOffset
            yield x - invOffset, y + offset


if __name__ == "__main__":
    main()
