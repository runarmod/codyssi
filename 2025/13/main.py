import functools
import os
import re
import time

import networkx


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        data = map(
            lambda line: re.split(r" -> | \| ", line.strip()),
            get_data(test=test).strip("\n").split("\n"),
        )

        self.G = networkx.DiGraph()
        for start, end, weight in data:
            self.G.add_edge(start, end, weight=int(weight))

    def get_product_longest_path(self, **kwargs):
        m = networkx.shortest_path_length(self.G, **kwargs)
        return functools.reduce(
            lambda x, y: x * y, sorted(m.values(), reverse=True)[:3]
        )

    def part1(self):
        return self.get_product_longest_path(source="STT")

    def part2(self):
        return self.get_product_longest_path(source="STT", weight="weight")

    def part3(self):
        cycles = networkx.simple_cycles(self.G)
        best = 0
        for cycle in cycles:
            length = 0
            for i in range(len(cycle) - 1):
                length += self.G[cycle[i]][cycle[i + 1]]["weight"]
            length += self.G[cycle[-1]][cycle[0]]["weight"]
            best = max(best, length)
        return best


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 36 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 44720 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 18 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
