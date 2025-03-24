import os
import time
from functools import partial


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = get_data(test=test).strip().split("\n")

    def part1(self):
        return sum(c.isalpha() for line in self.data for c in line)

    def reduce(self, line, reduceHyphen=True):
        cont = True
        while cont:
            cont = False
            for i in range(len(line)):
                try:
                    if line[i].isdigit() and (
                        line[i + 1].isalpha() or (line[i + 1] == "-" and reduceHyphen)
                    ):
                        line = line[:i] + line[i + 2 :]
                        cont = True
                        break
                    if line[i + 1].isdigit() and (
                        line[i].isalpha() or (line[i] == "-" and reduceHyphen)
                    ):
                        line = line[:i] + line[i + 2 :]
                        cont = True
                        break
                except IndexError:
                    pass
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
