from operator import eq
import os
import re
import time
from itertools import count, takewhile
from operator import itemgetter

from more_itertools import last


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class TreeNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.left = None
        self.right = None


class Solution:
    def __init__(self, test=False):
        artifacts = list(
            map(
                lambda x: (x[0], int(x[1])),
                re.findall(r"(.*?) \| (\d+)", get_data(test=test).strip("\n")),
            )
        )
        self.a, self.b = artifacts[:-2], artifacts[-2:]

        self.tree = TreeNode(*self.a[0])
        root = self.tree
        for node, value in self.a[1:]:
            tmp_tree = root
            while True:
                if value < tmp_tree.value:
                    if tmp_tree.left is None:
                        tmp_tree.left = TreeNode(node, value)
                        break
                    tmp_tree = tmp_tree.left
                else:
                    if tmp_tree.right is None:
                        tmp_tree.right = TreeNode(node, value)
                        break
                    tmp_tree = tmp_tree.right

    def values(self, tree, layer: int):
        if tree is None:
            return set()
        if layer == 0:
            return {tree.value}
        return self.values(tree.left, layer - 1) | self.values(tree.right, layer - 1)

    def part1(self):
        best = 0
        for i in count():
            values = self.values(self.tree, i)
            if values == set():
                break
            best = max(best, sum(values))
        return i * best

    def get_parents(self, ID: int):
        nodes = []
        node = self.tree
        while True:
            if node is None:
                break
            nodes.append(node)
            if ID < node.value:
                node = node.left
            else:
                node = node.right
        return nodes

    def part2(self):
        return "-".join(map(lambda x: x.name, self.get_parents(500000)))

    def part3(self):
        return last(
            takewhile(
                lambda x: eq(*x),
                zip(*map(self.get_parents, map(itemgetter(1), self.b))),
            )
        )[0].name


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 12645822 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 'ozNxANO-pYNonIG-MUantNm-lOSlxki-SDJtdpa-JSXfNAJ' else 'wrong :('}"
    )
    print(
        f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 'pYNonIG' else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
