import itertools
import os
import string
import time

from more_itertools import ilen


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.data = get_data(test=test).strip().split("\n")

    def calc(self, line: str):
        s = 0
        for char in line:
            if char in string.ascii_uppercase:
                s += ord(char) - ord("A") + 1
            elif char in string.digits:
                s += int(char)
            else:
                assert False
        return s

    def part1(self):
        return sum(map(self.calc, self.data))

    def part2(self):
        s = 0
        for line in self.data:
            line_length = len(line)
            side_count = line_length // 10
            middle = line_length - side_count * 2
            s += self.calc(f"{line[:side_count]}{middle}{line[-side_count:]}")
        return s

    def part3(self):
        s = 0
        for line in self.data:
            for char, grouper in itertools.groupby(line):
                s += self.calc(f"{ilen(grouper)}{char}")
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 1247 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 219 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 539 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
