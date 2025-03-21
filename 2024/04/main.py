import itertools
import os
import re
import time

import networkx
from more_itertools import ilen


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.G = networkx.Graph(
            itertools.batched(re.findall(r"[A-Z]+", get_data(test=test).strip("\n")), 2)
        )
        self.start = "STT"

    def part1(self):
        return self.G.number_of_nodes()

    def part2(self):
        return ilen(
            filter(
                lambda path: len(path) <= 3 + 1,
                networkx.shortest_path(self.G, self.start).values(),
            )
        )

    def part3(self):
        return sum(
            map(
                lambda path: len(path) - 1,
                networkx.shortest_path(self.G, self.start).values(),
            )
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 7 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 6 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 15 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
