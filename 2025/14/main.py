import os
import re
import time


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        data = re.findall(
            r"\d+ ([a-zA-Z]+) \| Quality : (\d+), Cost : (\d+), Unique Materials : (\d+)",
            get_data(test=test).strip("\n"),
        )
        self.data = [
            (name, int(quality), int(cost), int(unique_materials))
            for name, quality, cost, unique_materials in data
        ]

    def part1(self):
        return sum(
            x[-1] for x in sorted(self.data, key=lambda x: x[1], reverse=True)[:5]
        )

    def budget(self, limit: int = 30, start_index: int = 0):
        for i, item in enumerate(self.data[start_index:], start=start_index):
            if item[2] > limit:
                continue
            yield (item,)
            for sub_item in self.budget(limit - item[2], i + 1):
                yield (item,) + sub_item

    def calculate(self, limit: int):
        possible_combos = self.budget(limit=limit)

        combo = max(
            possible_combos,
            key=lambda x: (sum(item[1] for item in x), -sum(item[3] for item in x)),
        )
        quality = sum(item[1] for item in combo)
        unique_materials = sum(item[3] for item in combo)
        return quality * unique_materials

    def part2(self):
        return self.calculate(30)

    def part3(self):
        return self.calculate(150)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 90 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 8256 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 59388 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
