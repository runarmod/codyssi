import itertools
import os
import re
import time


def nums(line: str) -> list[int]:
    return list(map(int, re.findall(r"\d+", line)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        data = get_data(test=test).strip().split("\n\n")
        self.tracks = nums(data[0])
        self.swaps = list(itertools.batched(nums(data[1]), 2))
        self.test_track = int(data[2])

        swaps2 = self.swaps[:]
        self.swaps2 = []
        for i, (x, y) in enumerate(swaps2):
            self.swaps2.append((x, y, swaps2[(i + 1) % len(swaps2)][0]))

    def part1(self):
        tracks = self.tracks[:]
        for x, y in self.swaps:
            tracks[x - 1], tracks[y - 1] = tracks[y - 1], tracks[x - 1]
        return tracks[self.test_track - 1]

    def part2(self):
        tracks = self.tracks[:]
        for x, y, z in self.swaps2:
            tracks[z - 1], tracks[y - 1], tracks[x - 1] = (
                tracks[y - 1],
                tracks[x - 1],
                tracks[z - 1],
            )
        return tracks[self.test_track - 1]

    def part3(self):
        tracks = self.tracks[:]
        for x, y in self.swaps:
            block_length = min(abs(x - y), len(self.tracks) - max(x, y) + 1)
            (
                tracks[x - 1 : x + block_length - 1],
                tracks[y - 1 : y + block_length - 1],
            ) = (
                tracks[y - 1 : y + block_length - 1],
                tracks[x - 1 : x + block_length - 1],
            )
        return tracks[self.test_track - 1]


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 45 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 796 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 827 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
