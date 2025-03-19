import os
import re
import time


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(test=test).strip("\n").split("\n")
        num = data[:-1]
        stuff = data[-1]

        self.nums = list(map(int, num))
        self.corrections = stuff

    def part1(self):
        c = self.nums[0]
        for n, s in zip(self.nums[1:], self.corrections, strict=True):
            c += n * (-1 if s == "-" else 1)
        return c

    def part2(self):
        c = self.nums[0]
        for n, s in zip(self.nums[1:], self.corrections[::-1], strict=True):
            c += n * (-1 if s == "-" else 1)
        return c

    def part3(self):
        c = self.nums[0] * 10 + self.nums[1]
        for i in range(2, len(self.nums), 2):
            num = self.nums[i] * 10 + self.nums[i + 1]
            thing = -1 if self.corrections[::-1][i // 2 - 1] == "-" else 1
            c += thing * num
        return c


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 21 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 23 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 189 else 'wrong :('}")

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
