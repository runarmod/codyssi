(
    lambda d: list(
        map(
            print,
            (
                sum(__import__("itertools").compress(*zip(*enumerate(d, start=1)))),
                (
                    lambda it, op: sum(
                        op.and_(g1, g2) if i % 2 == 0 else op.or_(g1, g2)
                        for i, (g1, g2) in enumerate(zip(it, it))
                    )
                )(iter(d), __import__("operator")),
                "TODO: Part 3",
            ),
        )
    )
)(tuple(map(lambda x: x == "TRUE", open("input.txt").read().strip().split("\n"))))
