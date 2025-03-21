(
    lambda d: list(
        map(
            print,
            (sum(d), sum(sorted(d)[:-20]), sum(d[::2]) - sum(d[1::2])),
        )
    )
)(tuple(map(int, __import__("re").findall(r"-?\d+", open("input.txt").read()))))
