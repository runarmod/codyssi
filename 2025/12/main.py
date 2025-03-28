import itertools
import os
import re
import time
from copy import deepcopy


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        self.test = test
        numbers, operations, actions = get_data(test=test).strip("\n").split("\n\n")
        self.numbers = list(map(nums, numbers.split("\n")))
        self.operations = re.findall(
            r"SHIFT (ROW|COL) (\d+) BY (\d+)|(ADD|SUB|MULTIPLY) (\d+) (ROW|COL) (\d+)|(ADD|SUB|MULTIPLY) (\d+) ALL",
            operations,
        )
        self.actions = actions.split("\n")

    def shift(self, numbers, rowcol, index, amount):
        if rowcol == "ROW":
            numbers[index] = numbers[index][-amount:] + numbers[index][:-amount]
        elif rowcol == "COL":
            numbers = list(zip(*numbers))
            numbers[index] = numbers[index][-amount:] + numbers[index][:-amount]
            numbers = list(zip(*numbers))
        return numbers

    def modify(self, numbers, operation, amount, rowcol, index):
        assert (
            0 <= index < len(numbers)
        ), f"Index {index} out of range, must be between 0 and {len(numbers)-1}"
        if rowcol == "COL":
            numbers = list(zip(*numbers))
        if operation == "ADD":
            numbers[index] = [(n + amount) % 1073741824 for n in numbers[index]]
        elif operation == "SUB":
            numbers[index] = [n - amount for n in numbers[index]]
        elif operation == "MULTIPLY":
            numbers[index] = [(n * amount) % 1073741824 for n in numbers[index]]
        if rowcol == "COL":
            numbers = list(zip(*numbers))
        return numbers

    def modify_all(self, numbers, operation, amount):
        if operation == "ADD":
            numbers = [[(n + amount) % 1073741824 for n in row] for row in numbers]
        elif operation == "SUB":
            numbers = [[(n - amount) % 1073741824 for n in row] for row in numbers]
        elif operation == "MULTIPLY":
            numbers = [[(n * amount) % 1073741824 for n in row] for row in numbers]
        return numbers

    def execute_operation(self, numbers, operation_list):
        if len(operation_list[0]):
            rowcol, index, amount, *_ = operation_list
            numbers = self.shift(numbers, rowcol, int(index) - 1, int(amount))
        elif len(operation_list[3]):
            _, _, _, operation, amount, rowcol, index, *_ = operation_list
            numbers = self.modify(
                numbers, operation, int(amount), rowcol, int(index) - 1
            )
        elif len(operation_list[7]):
            _, _, _, _, _, _, _, operation, amount = operation_list
            numbers = self.modify_all(numbers, operation, int(amount))
        return numbers

    def part1(self):
        numbers = list(map(list, self.numbers))
        for operation_list in self.operations:
            numbers = self.execute_operation(numbers, operation_list)

        max_row = max(map(sum, numbers))
        max_col = max(map(sum, zip(*numbers)))
        return max(max_row, max_col)

    def calculate_max_sum(self, numbers):
        max_row = max(map(sum, numbers))
        max_col = max(map(sum, zip(*numbers)))
        return max(max_row, max_col)

    def execute_actions(self, actions):
        operations = deepcopy(self.operations)
        numbers = deepcopy(self.numbers)
        buffer = None
        for action in actions:
            match action:
                case "TAKE":
                    assert buffer is None, "Buffer is not empty"
                    if len(operations) == 0:
                        break
                    buffer = operations.pop(0)
                case "CYCLE":
                    assert buffer is not None, "Buffer is empty"
                    operations.append(buffer)
                    buffer = None
                case "ACT":
                    assert buffer is not None, "Buffer is empty"
                    numbers = self.execute_operation(numbers, buffer)
                    buffer = None

        return self.calculate_max_sum(numbers)

    def part2(self):
        return self.execute_actions(self.actions)

    def part3(self):
        return self.execute_actions(itertools.cycle(self.actions))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 18938 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 11496 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 19022 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
