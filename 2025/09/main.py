import os
import re
import time
from collections import defaultdict
from copy import copy


def get_data(test: bool = False) -> str:
    directory = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(directory, f"{"test" if test else ""}input.txt")
    return open(file).read()


class Solution:
    def __init__(self, test=False):
        balance, transactions = get_data(test=test).strip("\n").split("\n\n")
        self.balance = dict(
            map(
                lambda x: (x[0], int(x[1])),
                (line.split(" HAS ") for line in balance.split("\n")),
            )
        )

        self.transactions = list(
            map(
                lambda x: (x[0], x[1], int(x[2])),
                (
                    re.split(r" TO | AMT ", line[5:])
                    for line in transactions.split("\n")
                ),
            )
        )

    def part1(self):
        balance = copy(self.balance)
        for sender, reciever, amount in self.transactions:
            balance[sender] -= amount
            balance[reciever] += amount
        return sum(sorted(balance.values(), reverse=True)[:3])

    def part2(self):
        balance = copy(self.balance)
        for sender, reciever, amount in self.transactions:
            send_amount = min(balance[sender], amount)
            balance[sender] -= send_amount
            balance[reciever] += send_amount
        return sum(sorted(balance.values(), reverse=True)[:3])

    def part3(self):
        balance = copy(self.balance)
        debt_dict = defaultdict(list)
        for sender, reciever, amount in self.transactions:
            # Exchange money
            send_amount = min(balance[sender], amount)
            debt = amount - send_amount
            balance[sender] -= send_amount
            balance[reciever] += send_amount

            # Log the debt
            if debt > 0:
                debt_dict[sender].append((reciever, debt))

            # Pay off all debts
            while any(
                len(debt_dict[sender]) and balance[sender] > 0 for sender in balance
            ):
                sender = next(
                    sender
                    for sender in debt_dict
                    if len(debt_dict[sender]) and balance[sender] > 0
                )
                reciever, owe_amount = debt_dict[sender][0]
                possible_send_amount = min(balance[sender], owe_amount)
                debt_dict[sender][0] = (reciever, owe_amount - possible_send_amount)
                if debt_dict[sender][0][1] == 0:
                    debt_dict[sender].pop(0)
                balance[sender] -= possible_send_amount
                balance[reciever] += possible_send_amount
                if len(debt_dict[sender]) == 0:
                    del debt_dict[sender]

        return sum(sorted(balance.values(), reverse=True)[:3])


def main():
    start = time.perf_counter()

    test = Solution(test=True)
    test1 = test.part1()
    test2 = test.part2()
    test3 = test.part3()
    print(f"(TEST) Part 1: {test1}, \t{'correct :)' if test1 == 2870 else 'wrong :('}")
    print(f"(TEST) Part 2: {test2}, \t{'correct :)' if test2 == 2542 else 'wrong :('}")
    print(f"(TEST) Part 3: {test3}, \t{'correct :)' if test3 == 2511 else 'wrong :('}")

    solution = Solution()
    print(f"Part 1: {solution.part1()}")
    print(f"Part 2: {solution.part2()}")
    print(f"Part 3: {solution.part3()}")

    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")


if __name__ == "__main__":
    main()
