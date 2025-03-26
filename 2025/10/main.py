import heapq
import itertools
import os
import re
import time


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def numsNested(
    data: str | list[str] | list[list[str]],
) -> tuple[int | tuple[int, ...], ...]:
    if isinstance(data, str):
        return nums(data)
    if not hasattr(data, "__iter__"):
        raise ValueError("Data must be a tuple/list/iterable or a string")
    return tuple(e[0] if len(e) == 1 else e for e in filter(len, map(numsNested, data)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.rows = numsNested(
            map(str.split, get_data(test=test).strip("\n").split("\n"))
        )

    def part1(self):
        return min(*(map(sum, itertools.chain(self.rows, zip(*self.rows)))))

    def part2(self):
        return self.dijkstra((0, 0), (14, 14))

    def part3(self):
        return self.dijkstra((0, 0), (len(self.rows) - 1, len(self.rows[0]) - 1))

    def dijkstra(self, start: tuple[int, int], end: tuple[int, int]):
        q = [(self.rows[start[1]][start[0]], *start)]  # (danger, x, y)
        visited = set()  # (x, y)

        while q:
            danger, x, y = heapq.heappop(q)
            if (x, y) == end:
                return danger
            visited.add((x, y))
            for nx, ny in neighbors4(
                (x, y), bounds=[range(0, len(self.rows)), range(0, len(self.rows[0]))]
            ):
                if (nx, ny) not in visited:
                    heapq.heappush(q, (danger + self.rows[ny][nx], nx, ny))
        return None


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 73 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 94 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 120 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


def neighbors4(
    point: tuple[int, ...], jump=1, bounds: range | list[range] | None = None
):
    for i in range(len(point)):
        for diff in (-jump, jump):
            nc = point[i] + diff
            if (
                bounds is None
                or (isinstance(bounds, range) and nc in bounds)
                or nc in bounds[i]
            ):
                yield point[:i] + (nc,) + point[i + 1 :]


if __name__ == "__main__":
    main()
