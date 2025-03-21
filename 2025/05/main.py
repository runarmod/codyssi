import os
import re
import time
from itertools import batched

from more_itertools import minmax


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


def manhattan(p1: tuple[int, ...], p2: tuple[int, ...]):
    return sum(abs(a - b) for a, b in zip(p1, p2))


class Solution:
    def __init__(self, test=False):
        self.data = list(batched(nums(get_data(test=test)), 2))

    def part1(self):
        _min = _max = manhattan((0, 0), self.data[0])
        for pos in self.data[1:]:
            _min, _max = minmax(_min, _max, manhattan((0, 0), pos))

        return _max - _min

    def part2(self):
        minn = float("inf")
        shortest = (0, 0)
        for x, y in self.data:
            d = manhattan((0, 0), (x, y))
            if d < minn:
                minn = d
                shortest = (x, y)

        best = float("inf")
        for x, y in self.data:
            if shortest == (x, y):
                continue
            best = min(best, manhattan(shortest, (x, y)))

        return best

    def part3(self):
        def find_closest(pos, lst):
            best = {"d": float("inf"), "pos": (0, 0)}
            for p in lst:
                d = manhattan(pos, p)
                if d < best["d"]:
                    best = {"d": d, "pos": p}
                elif d == best["d"] and pos[0] < best["pos"][0]:
                    best = {"d": d, "pos": p}
            return best

        lst = self.data[:]
        s = 0
        prev = (0, 0)
        while lst:
            best = find_closest(prev, lst)
            prev = best["pos"]
            lst.remove(best["pos"])
            s += best["d"]
        return s


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 226 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 114 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 1384 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
