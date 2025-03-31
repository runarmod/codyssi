import itertools
import operator
import os
import re
import time
from collections import namedtuple
from copy import deepcopy

import numpy as np


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


shift_line = namedtuple("shift_line", ["rowcol", "index", "amount"])
modify_line = namedtuple("modify_line", ["operation", "amount", "rowcol", "index"])
modify_all = namedtuple("modify_all", ["operation", "amount"])


def map_keep_on_error(func, iterable, *exceptions):
    for item in iterable:
        try:
            yield func(item)
        except exceptions:
            yield item


def parse_operation(operation_list):
    if len(operation_list[0]):
        return shift_line(*map_keep_on_error(int, operation_list[:3], ValueError))
    elif len(operation_list[3]):
        return modify_line(*map_keep_on_error(int, operation_list[3:7], ValueError))
    elif len(operation_list[7]):
        return modify_all(*map_keep_on_error(int, operation_list[7:], ValueError))
    else:
        raise ValueError("Invalid operation list")


class Solution:
    def __init__(self, test=False):
        numbers, operations, actions = get_data(test=test).strip("\n").split("\n\n")
        self.numbers = np.array(list(map(nums, numbers.split("\n"))))
        self.operations = re.findall(
            r"SHIFT (ROW|COL) (\d+) BY (\d+)|(ADD|SUB|MULTIPLY) (\d+) (ROW|COL) (\d+)|(ADD|SUB|MULTIPLY) (\d+) ALL",
            operations,
        )
        self.operations = list(map(parse_operation, self.operations))
        self.actions = actions.split("\n")
        self.mod = 1073741824

    def shft_line(self, numbers, op: shift_line):
        _slice = (
            slice(None, op.index - 1) if op.rowcol == "COL" else slice(op.index - 1)
        )
        numbers[_slice] = np.concatenate(
            (numbers[_slice][-op.amount :], numbers[_slice][: -op.amount])
        )
        return numbers

    def mod_line(self, numbers, op: modify_line):
        assert (
            1 <= op.index <= len(numbers)
        ), f"Index {op.index} out of range, must be between 1 and {len(numbers)}"

        if op.rowcol == "COL":
            numbers = numbers.T

        operation = (
            operator.add
            if op.operation == "ADD"
            else operator.sub if op.operation == "SUB" else operator.mul
        )
        numbers[op.index - 1] = operation(numbers[op.index - 1], op.amount) % self.mod

        if op.rowcol == "COL":
            return numbers.T

        return numbers

    def mod_all(self, numbers, op: modify_all):
        operation = (
            operator.add
            if op.operation == "ADD"
            else operator.sub if op.operation == "SUB" else operator.mul
        )
        return operation(numbers, op.amount) % self.mod

    def execute_operation(
        self, numbers, operation: shift_line | modify_line | modify_all
    ):
        func = (
            self.shft_line
            if isinstance(operation, shift_line)
            else self.mod_line if isinstance(operation, modify_line) else self.mod_all
        )
        return func(numbers, operation)

    def calculate_max_sum(self, numbers):
        return max(map(sum, itertools.chain(numbers, numbers.T)))

    def part1(self):
        numbers = np.copy(self.numbers)
        for operation in self.operations:
            numbers = self.execute_operation(numbers, operation)
        return self.calculate_max_sum(numbers)

    def execute_actions(self, actions):
        operations = deepcopy(self.operations)
        numbers = np.copy(self.numbers)
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
