import itertools
import operator
import os
import time


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = tuple(
            map(lambda x: x == "TRUE", get_data(test=test).strip("\n").split("\n"))
        )

    def part1(self):
        return sum(itertools.compress(*zip(*enumerate(self.data, start=1))))

    def part2(self):
        iterator = iter(self.data)
        s = 0
        for i, (g1, g2) in enumerate(zip(iterator, iterator)):
            s += operator.and_(g1, g2) if i % 2 == 0 else operator.or_(g1, g2)
        return s

    def part3(self):
        data = self.data
        s = sum(self.data)
        while len(data):
            new_data = []
            iterator = iter(data)
            for i, (g1, g2) in enumerate(zip(iterator, iterator)):
                res = operator.and_(g1, g2) if i % 2 == 0 else operator.or_(g1, g2)
                s += res
                new_data.append(res)
            data = new_data
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 19 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 2 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 7 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
