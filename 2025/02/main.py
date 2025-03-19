import itertools
import os
import re
import time

import more_itertools
import numpy as np


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(test=test).strip("\n").split("\n\n")
        self.nums = nums(data[-1])

        func_nums = list(map(lambda x: int(x.split(" ")[-1]), data[0].split("\n")))
        a = lambda x: x + func_nums[0]  # noqa: E731
        b = lambda x: x * func_nums[1]  # noqa: E731
        c = lambda x: x ** func_nums[2]  # noqa: E731
        self.cba = lambda x: a(b(c(x)))

    def part1(self):
        return self.cba(round(np.median(np.array(self.nums))))

    def part2(self):
        return self.cba(sum(filter(lambda x: x % 2 == 0, self.nums)))

    def part3(self):
        return more_itertools.last(
            itertools.takewhile(
                lambda x: self.cba(x) < 15000000000000,
                sorted(self.nums),
            )
        )


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 9130674516975 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 1000986169836015 else 'wrong :('}"
    )
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 5496 else 'wrong :('}")

    solution = Solution()
    part1 = solution.part1()
    part2 = solution.part2()
    part3 = solution.part3()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Part 3: {part3}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
