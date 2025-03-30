import functools
import os
import re
import time
from collections import defaultdict, namedtuple
from operator import itemgetter


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Point:
    def __init__(self, *coords):
        self.coords = coords

    def __add__(self, other):
        return Point(*(a + b for a, b in zip(self.coords, other.coords)))

    def __lt__(self, other):
        return self.coords < other.coords

    def multiply_coords(self):
        return functools.reduce(lambda x, y: x * y, self.coords)


Item = namedtuple("Item", ["name", "quality", "cost", "unique_materials"])


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = re.findall(
            r"\d+ ([a-zA-Z]+) \| Quality : (\d+), Cost : (\d+), Unique Materials : (\d+)",
            get_data(test=test).strip("\n"),
        )
        self.data = [
            Item(name, int(quality), int(cost), int(unique_materials))
            for name, quality, cost, unique_materials in data
        ]
        self.w = list(map(itemgetter(2), self.data))
        self.v = list(map(lambda x: Point(x.quality, -x.unique_materials), self.data))

    def part1(self):
        return sum(
            x.unique_materials
            for x in sorted(self.data, key=lambda x: x.quality, reverse=True)[:5]
        )

    def find_items(self, total_limit: int):
        dp = defaultdict(lambda: Point(0, 0))

        for item in range(len(self.data)):
            for limit in range(1, total_limit + 1):
                if self.w[item] > limit:
                    dp[item, limit] = dp[item - 1, limit]
                else:
                    dp[item, limit] = max(
                        dp[item - 1, limit - self.w[item]] + self.v[item],
                        dp[item - 1, limit],
                    )
        return dp

    def calculate(self, limit: int):
        dp = self.find_items(limit)
        # Negative, since we here use negative materials to get correct (based on the task) comparison of points
        return -max(dp.values()).multiply_coords()

    def part2(self):
        return self.calculate(30)

    def part3(self):
        return self.calculate(150 if self.test else 300)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 90 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 8256 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 59388 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
