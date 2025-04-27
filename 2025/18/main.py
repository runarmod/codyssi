import itertools
import math
import os
import re
import time
from dataclasses import dataclass


@dataclass
class Rule:
    num: int
    x: int
    y: int
    z: int
    a: int
    divide: int
    remainder: int
    vx: int
    vy: int
    vz: int
    va: int


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{'test' if test else ''}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.rules: list[Rule] = list(
            itertools.starmap(
                Rule, map(nums, get_data(test=test).strip("\n").split("\n"))
            )
        )
        dimensions = (10, 15, 60, 3)
        self.X, self.Y, self.Z, self.A = dimensions
        self.ZA = self.A * self.Z
        self.YZA = self.ZA * self.Y
        self.XYZA = self.YZA * self.X

        self.time_steps = math.lcm(*dimensions)
        self.debris = self.precompute_debris()

    def idx(self, x: int, y: int, z: int, a: int):
        return x * self.YZA + y * self.ZA + z * self.A + (a + 1)

    def r_idx(self, xyza: int):
        x, yza = divmod(xyza, self.YZA)
        y, za = divmod(yza, self.ZA)
        z, a = divmod(za, self.A)
        return x, y, z, a - 1

    def precompute_debris(self):
        debris: list[int] = [[0] * self.XYZA for _ in range(self.time_steps)]

        for rule in self.rules:
            for xyza in range(self.XYZA):
                x, y, z, a = self.r_idx(xyza)
                if (
                    rule.x * x + rule.y * y + rule.z * z + rule.a * a
                ) % rule.divide == rule.remainder:
                    debris[0][self.idx(x, y, z, a)] += 1
                    for t in range(1, self.time_steps):
                        x = (x + rule.vx) % self.X
                        y = (y + rule.vy) % self.Y
                        z = (z + rule.vz) % self.Z
                        a = (a + rule.va + 1) % self.A - 1
                        debris[t][self.idx(x, y, z, a)] += 1

        return debris

    def count_debris(self, xyza: int, time: int) -> bool:
        if xyza == self.idx(0, 0, 0, 0):
            return 0
        return self.debris[time % self.time_steps][xyza]

    def part1(self):
        return sum(self.count_debris(xyza, 0) for xyza in range(self.XYZA))

    def calculate(self, allowed_hits: int):
        start = self.idx(0, 0, 0, 0)
        goal = self.idx(self.X - 1, self.Y - 1, self.Z - 1, 0)

        hits = [allowed_hits + 1] * self.XYZA
        hits[start] = 0
        t = 0
        while hits[goal] > allowed_hits:
            t += 1
            new_hits = hits[:]
            for xyza, h in enumerate(hits):
                if h > allowed_hits:
                    continue
                x, y, z, _ = self.r_idx(xyza)  # a is guaranteed 0
                for i, neighbor in neighbors4((x, y, z)):
                    if not 0 <= neighbor[i] < (self.X, self.Y, self.Z)[i]:
                        continue

                    neighbor = self.idx(*neighbor, 0)
                    new_hits[neighbor] = min(new_hits[neighbor], h)

            for xyza, h in enumerate(self.debris[t % self.time_steps]):
                new_hits[xyza] += h

            new_hits[start] = 0
            hits = new_hits

        return t

    def part2(self):
        return self.calculate(0)

    def part3(self):
        return self.calculate(3)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 32545 else 'wrong :('}")
    test2 = test.part2()
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 217 else 'wrong :('}")
    test3 = test.part3()
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 166 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


def neighbors4(point: tuple[int, ...], jump=1):
    for i in range(len(point)):
        for diff in (-jump, jump):
            yield i, point[:i] + (point[i] + diff,) + point[i + 1 :]


if __name__ == "__main__":
    main()
