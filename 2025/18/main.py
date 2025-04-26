import heapq
import itertools
import os
import re
import time
from dataclasses import dataclass

from more_itertools import zip_equal


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
        self.dimensions = (10, 15, 60, 3)
        self.ranges = list(map(range, self.dimensions[:-1])) + [range(-1, 2)]

    def count_debris(
        self,
        coord: tuple[int, int, int, int],
        time: int,
        allowed_hits: int = 9999999,
    ) -> bool:
        count = 0
        if coord == (0, 0, 0, 0):
            return count
        for rule in self.rules:
            time_aware_coord = [
                coord[0] - rule.vx * time,
                coord[1] - rule.vy * time,
                coord[2] - rule.vz * time,
                coord[3] - rule.va * time,
            ]
            time_aware_coord = [
                *(
                    custom_mod(c, 0, self.dimensions[i] - 1)
                    for i, c in enumerate(time_aware_coord[:-1])
                ),
                custom_mod(time_aware_coord[-1], -1, 1),
            ]
            if (
                rule.x * time_aware_coord[0]
                + rule.y * time_aware_coord[1]
                + rule.z * time_aware_coord[2]
                + rule.a * time_aware_coord[3]
            ) % rule.divide == rule.remainder:
                count += 1
                if count > allowed_hits:
                    return count
        return count

    def part1(self):
        return sum(
            self.count_debris(coord, 0) for coord in itertools.product(*self.ranges)
        )

    def A_star(self, start_lives: int):
        start = (0, 0, 0, 0)
        goal = tuple([*(x - 1 for x in self.dimensions[:-1]), 0])
        q = [(0, 0, start_lives, start)]  # (estimate, time_used, lives, coord)
        visited = {}  # (time, coord): lives
        while q:
            _, time, lives, coord = heapq.heappop(q)
            if coord == goal:
                return time

            if visited.get((time, coord), 0) >= lives:
                continue  # We have been in this state before, or better (in regards to lives)
            visited[time, coord] = lives

            new_time = time + 1
            # Do not include the last dimension (only debris can use it)
            for neighbor in neighbors4(coord[:-1]):
                neighbor = tuple((*neighbor, 0))
                if not all(0 <= n < d for n, d in zip_equal(neighbor, self.dimensions)):
                    continue
                new_lives = lives - self.count_debris(neighbor, new_time, lives)
                if new_lives <= 0:  # Dead
                    continue
                estimate = manhattan(neighbor, goal) + new_time
                heapq.heappush(q, (estimate, new_time, new_lives, neighbor))

            # Maybe do not move
            new_lives = lives - self.count_debris(coord, new_time, lives)
            if new_lives > 0:  # Still alive
                estimate = manhattan(neighbor, goal) + new_time
                heapq.heappush(q, (estimate, new_time, new_lives, coord))
        return None

    def part2(self):
        return self.A_star(1)

    def part3(self):
        return self.A_star(4)


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


def custom_mod(num: int, low: int, high: int) -> int:
    range_size = high - low + 1
    while num < low:
        num += range_size
    while num > high:
        num -= range_size
    return num


def neighbors4(point: tuple[int, ...], jump=1):
    for i in range(len(point)):
        for diff in (-jump, jump):
            yield point[:i] + (point[i] + diff,) + point[i + 1 :]


def manhattan(p1: tuple[int, ...], p2: tuple[int, ...]):
    return sum(abs(a - b) for a, b in zip_equal(p1, p2))


if __name__ == "__main__":
    main()
