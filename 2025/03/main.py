import itertools
import os
import re
import time

from more_itertools import collapse


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = list(
            map(
                lambda x: range(x[0], x[1] + 1),
                itertools.batched(
                    map(int, re.findall(r"\d+", get_data(test=test))),
                    2,
                ),
            ),
        )

    def total(self, batch_size: int):
        c = 0
        for b in itertools.batched(self.data, batch_size):
            s = set()
            for r in b:
                s |= set(r)
            c += len(s)
        return c

    def part1(self):
        return self.total(1)

    def part2(self):
        return self.total(2)

    def part3(self):
        m = 0
        batches = itertools.tee(itertools.batched(self.data, 2))
        for boxes in zip(batches[0], itertools.islice(batches[1], 1, None)):
            boxes = collapse(boxes, levels=1)
            s = set()
            for boxs in boxes:
                s |= set(boxs)
            m = max(m, len(s))
        return m


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 43 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 35 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 9 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
