import dataclasses
import functools
import itertools
import os
import re
import time

import networkx


def nums(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"-?\d+", line)))


def numsNested(
    data: str | list[str] | list[list[str]],
) -> tuple[int | tuple[int, ...], ...]:
    if isinstance(data, str):
        return nums(data)
    if not hasattr(data, "__iter__"):
        raise ValueError("Data must be a tuple/list/iterable or a string")
    return tuple(e[0] if len(e) == 1 else e for e in filter(len, map(numsNested, data)))


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{'test' if test else ''}input.txt")
    return open(file).read()


@dataclasses.dataclass
class Stair:
    id_: int
    start: int
    end: int
    from_: int
    to_: int


class Solution:
    def __init__(self, test=False):
        self.test = test
        stair_info, steps = get_data(test=test).strip("\n").split("\n\n")
        self.steps = nums(steps)
        self.first = list(map(int, re.search(r"(\d+) -> (\d+)", stair_info).groups()))

        # No stair with id 0, so we start with stair 1.
        # And stair 1 is a special case, because it has no from_ or to_.
        stairs = [None, Stair(1, *self.first, None, None)] + list(
            itertools.starmap(
                Stair,
                map(
                    numsNested,
                    re.findall(
                        r"S(\d+) : (\d+) -> (\d+) : FROM S(\d+) TO S(\d+)", stair_info
                    ),
                ),
            )
        )

        # It is easier to think of the graph as edges pointing from start to goal...
        G = networkx.DiGraph()
        for stair in stairs[1:]:
            for step in range(stair.start, stair.end):
                G.add_edge((stair.id_, step), (stair.id_, step + 1))
            if stair.from_ and stair.start in range(
                stairs[stair.from_].start, stairs[stair.from_].end + 1
            ):
                G.add_edge((stair.from_, stair.start), (stair.id_, stair.start))
            if stair.to_ and stair.end in range(
                stairs[stair.to_].start, stairs[stair.to_].end + 1
            ):
                G.add_edge((stair.id_, stair.end), (stair.to_, stair.end))

        # ... but easier to work with it reversed.
        # Because then we can easily find the count of paths from nodes to the goal,
        # which is more useful than the count of paths from the start to the nodes.
        # Also: #paths_to_goal_from_start == #paths_from_start_to_goal, so it doesn't matter.
        self.G = G.reverse()

    def part1(self):
        @functools.lru_cache(None)
        def stairs(n):
            if n == 0:
                return 1
            if n < 0:
                return 0
            return sum(stairs(n - step_length) for step_length in self.steps)

        return stairs(self.first[1])

    def predecessors_n_steps_away(self, G, node, n):
        def dfs(current_node, steps_remaining):
            if steps_remaining == 0:
                yield current_node
                return
            for predecessor in G.predecessors(current_node):
                yield from dfs(predecessor, steps_remaining - 1)

        return set(dfs(node, n))

    @functools.lru_cache(None)
    def path_from_node_to_goal(self, stair_id, step_nr):
        assert (stair_id, step_nr) in self.G.nodes
        if step_nr == self.first[1]:
            return 1
        if step_nr > self.first[1]:
            return 0

        predecessors = set()
        for step_length in self.steps:
            predecessors.update(
                self.predecessors_n_steps_away(
                    self.G, (stair_id, step_nr), step_length
                ),
            )

        return sum(itertools.starmap(self.path_from_node_to_goal, predecessors))

    def part2(self):
        assert networkx.is_directed_acyclic_graph(self.G)
        return self.path_from_node_to_goal(1, self.first[0])

    def part3(self):
        assert networkx.is_directed_acyclic_graph(self.G)

        k = min(
            self.path_from_node_to_goal(1, self.first[0]),
            100000000000000000000000000000,
        )

        path = []
        start, end = (1, self.first[0]), (1, self.first[1])
        node = start

        while node != end:
            path.append(node)

            children = set()
            for step_length in self.steps:
                children.update(
                    self.predecessors_n_steps_away(self.G, node, step_length)
                )

            for child in sorted(children):
                paths_to_goal = self.path_from_node_to_goal(*child)
                if paths_to_goal >= k:
                    # This means that this path contains the k-th path; follow it!
                    node = child
                    break
                k -= paths_to_goal
        path.append(end)

        return "-".join(map(lambda node: f"S{node[0]}_{node[1]}", path))


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(
        f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 231843173048269749794 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 113524314072255566781694 else 'wrong :('}"
    )
    print(
        f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 'S1_0-S1_6-S2_11-S2_17-S2_23-S2_29-S9_34-S9_37-S5_42-S5_48-S5_54-S5_60-S5_66-S5_72-S5_73-S5_74-S1_79-S3_84-S8_88-S8_89-S8_90-S3_90-S3_91-S1_96-S1_99' else 'wrong :('}"
    )

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start: .4f} sec")


if __name__ == "__main__":
    main()
