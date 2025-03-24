(
    lambda reduce, data: list(
        map(
            print,
            (
                sum(c.isalpha() for line in data for c in line),
                sum(map(lambda x: len(reduce(x, r"[a-zA-Z\-]")), data)),
                sum(map(lambda x: len(reduce(x, r"[a-zA-Z]")), data)),
            ),
        ),
    )
)(
    lambda line, alphaString: next(
        x
        for x, y in (
            lambda more_itertools: more_itertools.pairwise(
                more_itertools.iterate(
                    lambda line2: __import__("re").sub(
                        f"\\d{alphaString}|{alphaString}\\d", "", line2
                    ),
                    line,
                )
            )
        )(__import__("more_itertools"))
        if len(x) == len(y)
    ),
    open("input.txt").read().strip().split("\n"),
)
