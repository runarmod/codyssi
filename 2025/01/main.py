import os
import time
from itertools import batched


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = get_data(test=test).strip("\n").split("\n")

        self.nums = list(map(int, data[:-1]))
        self.signs = data[-1]

    def run(self, nums: list[int], signs: str, strict=True):
        c = next(nums)
        for n, s in zip(nums, signs, strict=strict):
            c += n * (-1 if s == "-" else 1)
        return c

    def part1(self):
        return self.run(iter(self.nums), self.signs)

    def part2(self):
        return self.run(iter(self.nums), self.signs[::-1])

    def part3(self):
        return self.run(
            map(lambda x: x[0] * 10 + x[1], batched(self.nums, 2)),
            self.signs[::-1],
            strict=False,
        )


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
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
