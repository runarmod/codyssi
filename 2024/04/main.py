import itertools
import os
import re
import time
from collections import defaultdict, deque
from operator import itemgetter

from more_itertools import ilen


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        data = itertools.batched(re.findall(r"\w+", get_data(test=test).strip("\n")), 2)

        self.G = defaultdict(set)
        for start, end in data:
            self.G[start].add(end)
            self.G[end].add(start)

        self.start = "STT"

    def part1(self):
        return len(self.G)

    def reachable(self, node, maxlen=float("inf")):
        stack = deque([[node]])
        seen = set()

        while stack:
            path = stack.popleft()
            node = path[-1]

            if len(path) > maxlen + 1:
                break
            if node in seen:
                continue
            seen.add(node)

            yield path, len(path) - 1  # -1 because first element is start-node

            for node2 in self.G[node]:
                stack.append((path + [node2]))

    def part2(self):
        return ilen(self.reachable(self.start, 3))

    def part3(self):
        return sum(map(itemgetter(1), self.reachable(self.start)))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 7 else 'wrong :('}")
    test2 = test.part2()
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 6 else 'wrong :('}")
    test3 = test.part3()
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 15 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
