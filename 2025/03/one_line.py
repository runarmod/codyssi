(
    lambda itertools, more_itertools: (
        lambda data: list(
            map(
                print,
                (
                    sum(map(len, map(set, data))),
                    sum(
                        len(set(more_itertools.collapse(b)))
                        for b in itertools.batched(data, 2)
                    ),
                    max(
                        len(set(more_itertools.collapse(boxes)))
                        for boxes in zip(
                            itertools.batched(data, 2),
                            itertools.islice(itertools.batched(data, 2), 1, None),
                        )
                    ),
                ),
            )
        )
    )(
        list(
            map(
                lambda x: range(x[0], x[1] + 1),
                itertools.batched(
                    map(
                        int, __import__("re").findall(r"\d+", open("input.txt").read())
                    ),
                    2,
                ),
            ),
        )
    )
)(
    __import__("itertools"),
    __import__("more_itertools"),
)
