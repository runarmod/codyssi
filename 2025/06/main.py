import os
import time


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.data = get_data(test=test).strip()

    def part1(self):
        return sum(1 for c in self.data if c.isalpha())

    def val(self, c):
        if c.islower():
            return ord(c) - ord("a") + 1
        if c.isupper():
            return ord(c) - ord("A") + 27
        assert False, c

    def part2(self):
        s = 0
        for c in self.data:
            if not c.isalpha():
                continue
            s += self.val(c)
        return s

    def part3(self):
        log = []
        for c in self.data:
            if c.isalpha():
                log.append(self.val(c))
            else:
                value = log[-1] * 2 - 5
                value = ((value - 1) % 52) + 1  # 1 to 52 inclusive
                log.append(value)
        return sum(log)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 59 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 1742 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 2708 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
