import itertools
import os
import string
import time


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


def from_base(num: str, base: int) -> int:
    alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase
    out = 0
    for digit in num:
        out = out * base + alphabet.index(digit)
    return out


def to_base(num: int, base: int) -> str:
    alphabet = (
        string.digits + string.ascii_uppercase + string.ascii_lowercase + "!@#$%^"
    )
    if num == 0:
        return "0"
    out = ""
    while num:
        num, rem = divmod(num, base)
        out = alphabet[rem] + out
    return out


class Solution:
    def __init__(self, test=False):
        data = (line.split(" ") for line in get_data(test=test).strip("\n").split("\n"))
        self.parsed = list(map(lambda x: (from_base(x[0], int(x[1])), int(x[1])), data))

    def part1(self):
        return max(self.parsed, key=lambda x: x[0])[0]

    def part2(self):
        return to_base(sum(x[0] for x in self.parsed), 68)

    def part3(self):
        s = sum(x[0] for x in self.parsed)
        for i in itertools.count():
            if i**4 > s:
                return i


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 9047685997827 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == '4iWAbo%6' else 'wrong :('}"
    )
    print(f"(TEST) Part 3: {test3}, \t\t{'correct :)' if test3 == 2366 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
