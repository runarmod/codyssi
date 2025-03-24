import os
import re
import time
from functools import partial

from more_itertools import flatten


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = get_data(test=test).strip().split("\n")

    def part1(self):
        return sum(map(str.isalpha, flatten(self.data)))

    def reduce(self, line, reduceHyphen=True):
        alph = r"[a-zA-Z\-]" if reduceHyphen else r"[a-zA-Z]"
        while True:
            length = len(line)
            line = re.sub(f"\\d{alph}|{alph}\\d", "", line, count=1)
            if length == len(line):
                return line

    def part2(self):
        return sum(map(len, map(partial(self.reduce, reduceHyphen=True), self.data)))

    def part3(self):
        return sum(map(len, map(partial(self.reduce, reduceHyphen=False), self.data)))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 52 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 18 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 26 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
