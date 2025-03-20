(
    lambda calculate, data: __import__("collections").deque(
        map(
            print,
            (
                sum(map(calculate, data)),
                sum(
                    calculate(
                        f"{line[:len(line) // 10]}{len(line) - len(line) // 10 * 2}{line[-(len(line) // 10):]}"
                    )
                    for line in data
                ),
                sum(
                    sum(
                        calculate(
                            f"{__import__("more_itertools").ilen(grouper)}{char}"
                        )
                        for char, grouper in __import__("itertools").groupby(line)
                    )
                    for line in data
                ),
            ),
        ),
        maxlen=0,
    )
)(
    lambda line: sum(
        (
            (ord(char) - ord("A") + 1)
            if char in __import__("string").ascii_uppercase
            else int(char)
        )
        for char in line
    ),
    open("input.txt").read().strip().split("\n"),
)
