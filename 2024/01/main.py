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
        self.data = nums(get_data(test=test).strip("\n"))

    def part1(self):
        return sum(self.data)

    def part2(self):
        return sum(sorted(self.data)[: -(20 if not self.test else 2)])

    def part3(self):
        return sum(self.data[::2]) - sum(self.data[1::2])


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 2895391 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 1261624 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 960705 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
