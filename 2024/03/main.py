import os
import string
import time
from operator import itemgetter


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = list(
            map(
                lambda line: (int(line[0], int(line[1])), int(line[1])),
                map(
                    lambda line: line.split(" "),
                    get_data(test=test).strip("\n").split("\n"),
                ),
            )
        )

    def part1(self):
        return sum(map(itemgetter(1), self.data))

    def part2(self):
        return sum(map(itemgetter(0), self.data))

    def to_base(self, num: int, base: int):
        alphabet = (
            string.digits + string.ascii_uppercase + string.ascii_lowercase + "!@#"
        )
        assert base <= len(alphabet)
        out = ""
        while num:
            num, digit = divmod(num, base)
            out += alphabet[digit]
        return out[::-1]

    def part3(self):
        return self.to_base(sum(map(itemgetter(0), self.data)), 65)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(
        f"(TEST) Part 1: {test1},         {'correct :)' if test1 == 78 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, {'correct :)' if test2 == 3487996082 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 3: {test3},     {'correct :)' if test3 == "30PzDC" else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
