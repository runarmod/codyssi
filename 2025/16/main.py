import os
import re
import time
from collections import defaultdict
from enum import Enum, auto
from functools import reduce
from itertools import chain
from operator import mul

import numpy as np
from more_itertools import interleave_longest


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class CubeFace(Enum):
    # The actual values and order of the faces does not matter
    CURRENT = auto()
    BACK = auto()
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


class Face:
    def __init__(self, grid: np.ndarray):
        self.grid = grid

    def add_row(self, row: int, value: int):
        self.grid[row, :] += value

    def add_col(self, col: int, value: int):
        self.grid[:, col] += value

    def add_face(self, value: int):
        self.grid += value

    def bound(self):
        # Keep between 1 and 100 (1-indexing makes this weird)
        self.grid = (self.grid - 1) % 100 + 1

    def __repr__(self):
        return self.grid.__repr__()


def rotate(
    cube: dict[CubeFace, Face],
    direction: str,
) -> dict[CubeFace, Face]:
    if direction == "L":
        new_to_old = {
            CubeFace.CURRENT: CubeFace.LEFT,
            CubeFace.LEFT: CubeFace.BACK,
            CubeFace.BACK: CubeFace.RIGHT,
            CubeFace.RIGHT: CubeFace.CURRENT,
            CubeFace.BOTTOM: CubeFace.BOTTOM,
            CubeFace.TOP: CubeFace.TOP,
        }
        cube = {f: cube[new_to_old[f]] for f in CubeFace}
        # Top and bottom rotates when turning cube sideways
        cube[CubeFace.BOTTOM].grid = np.rot90(cube[CubeFace.BOTTOM].grid, -1)
        cube[CubeFace.TOP].grid = np.rot90(cube[CubeFace.TOP].grid, 1)

        # Flip faces going in and out of the back side
        # (important for when rotating sideways, then up/down)
        cube[CubeFace.BACK].grid = np.rot90(cube[CubeFace.BACK].grid, 2)
        cube[CubeFace.LEFT].grid = np.rot90(cube[CubeFace.LEFT].grid, 2)

    elif direction == "R":
        new_to_old = {
            CubeFace.CURRENT: CubeFace.RIGHT,
            CubeFace.RIGHT: CubeFace.BACK,
            CubeFace.BACK: CubeFace.LEFT,
            CubeFace.LEFT: CubeFace.CURRENT,
            CubeFace.BOTTOM: CubeFace.BOTTOM,
            CubeFace.TOP: CubeFace.TOP,
        }
        cube = {f: cube[new_to_old[f]] for f in CubeFace}
        # Top and bottom rotates when turning cube sideways
        cube[CubeFace.TOP].grid = np.rot90(cube[CubeFace.TOP].grid, -1)
        cube[CubeFace.BOTTOM].grid = np.rot90(cube[CubeFace.BOTTOM].grid, 1)

        # Flip faces going in and out of the back side
        # (important for when rotating sideways, then up/down)
        cube[CubeFace.BACK].grid = np.rot90(cube[CubeFace.BACK].grid, 2)
        cube[CubeFace.RIGHT].grid = np.rot90(cube[CubeFace.RIGHT].grid, 2)

    elif direction == "U":
        new_to_old = {
            CubeFace.CURRENT: CubeFace.TOP,
            CubeFace.TOP: CubeFace.BACK,
            CubeFace.BACK: CubeFace.BOTTOM,
            CubeFace.BOTTOM: CubeFace.CURRENT,
            CubeFace.LEFT: CubeFace.LEFT,
            CubeFace.RIGHT: CubeFace.RIGHT,
        }
        cube = {f: cube[new_to_old[f]] for f in CubeFace}
        # Left and right rotates when turning cube up/down
        cube[CubeFace.LEFT].grid = np.rot90(cube[CubeFace.LEFT].grid, -1)
        cube[CubeFace.RIGHT].grid = np.rot90(cube[CubeFace.RIGHT].grid, 1)

    elif direction == "D":
        new_to_old = {
            CubeFace.CURRENT: CubeFace.BOTTOM,
            CubeFace.BOTTOM: CubeFace.BACK,
            CubeFace.BACK: CubeFace.TOP,
            CubeFace.TOP: CubeFace.CURRENT,
            CubeFace.LEFT: CubeFace.LEFT,
            CubeFace.RIGHT: CubeFace.RIGHT,
        }
        cube = {f: cube[new_to_old[f]] for f in CubeFace}
        # Left and right rotates when turning cube up/down
        cube[CubeFace.RIGHT].grid = np.rot90(cube[CubeFace.RIGHT].grid, -1)
        cube[CubeFace.LEFT].grid = np.rot90(cube[CubeFace.LEFT].grid, 1)
    else:
        raise ValueError(f"Invalid direction: {direction}")

    return cube


class Solution:
    def __init__(self, test=False):
        self.test = test
        self.a, self.b = get_data(test=test).strip("\n").split("\n\n")
        self.a = re.findall(r"(?:(?:(ROW|COL) (\d+))|(FACE)) - VALUE (\d+)", self.a)
        self.n = 80

    def get_fresh_cube(self):
        return {f: Face(np.ones((self.n, self.n), dtype=int)) for f in CubeFace}

    def part1(self):
        absorptions = defaultdict(int)
        cube = self.get_fresh_cube()
        for i, thing in enumerate(interleave_longest(self.a, self.b)):
            if i % 2 == 1:
                cube = rotate(cube, direction=thing)
            else:
                instruction = thing
                power = int(instruction[3]) * self.n
                if instruction[2] == "FACE":
                    power *= self.n
                absorptions[cube[CubeFace.CURRENT]] += power

        _sorted = sorted(absorptions.values(), reverse=True)[:2]
        return _sorted[0] * _sorted[1]

    def dominant_sum_product(self, cube):
        sums = []
        for face in cube.values():
            sums.append(
                int(
                    max(
                        map(
                            sum,
                            chain(face.grid, face.grid.T),
                        )
                    )
                )
            )
        return reduce(mul, sums, 1)

    def part2(self):
        cube = self.get_fresh_cube()
        for i, thing in enumerate(interleave_longest(self.a, self.b)):
            if i % 2 == 1:
                cube = rotate(cube, direction=thing)
            else:
                instruction = thing
                value = int(instruction[3])
                face = cube[CubeFace.CURRENT]

                if instruction[2] == "FACE":
                    face.add_face(value)
                elif instruction[0] == "ROW":
                    face.add_row(int(instruction[1]) - 1, value)
                elif instruction[0] == "COL":
                    face.add_col(int(instruction[1]) - 1, value)
                face.bound()

        return self.dominant_sum_product(cube)

    def part3(self):
        cube = self.get_fresh_cube()

        for i, thing in enumerate(interleave_longest(self.a, self.b)):
            if i % 2 == 1:
                cube = rotate(cube, direction=thing)
            else:
                instruction = thing
                value = int(instruction[3])
                face = cube[CubeFace.CURRENT]

                if instruction[2] == "FACE":
                    face.add_face(value)
                elif instruction[0] == "ROW":
                    # Rows are the same around the cube, except for the back face which is flipped
                    for f in (CubeFace.CURRENT, CubeFace.LEFT, CubeFace.RIGHT):
                        cube[f].add_row(int(instruction[1]) - 1, value)
                    cube[CubeFace.BACK].add_row(self.n - int(instruction[1]), value)

                elif instruction[0] == "COL":
                    # Columns are the same around the cube
                    for f in (
                        CubeFace.CURRENT,
                        CubeFace.TOP,
                        CubeFace.BOTTOM,
                        CubeFace.BACK,
                    ):
                        cube[f].add_col(int(instruction[1]) - 1, value)

                for f in cube.values():
                    f.bound()

        return self.dominant_sum_product(cube)


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(
        f"(TEST) Part 1: {test1}, \t\t\t{'correct :)' if test1 == 6902016000 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t\t{'correct :)' if test2 == 369594451623936000000 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 118479211258970523303936 else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    p2 = solution.part2()
    assert p2 == 56338692227049056670720
    print(f"Part 2: {p2}")

    p3 = solution.part3()
    assert p3 == 9521942308330552450560
    print(f"Part 3: {p3}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
