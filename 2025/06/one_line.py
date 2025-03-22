(
    lambda data, val: list(
        map(
            lambda func_x: print(sum(map(*func_x))),
            (
                (str.isalpha, data),
                (val, filter(str.isalpha, data)),
                (
                    lambda x: (
                        val(x) if isinstance(x, str) else x
                    ),  # The first value from accumulate is the first element (char) in data
                    __import__("itertools").accumulate(
                        data,
                        lambda prev, new: (
                            val(new) if new.isalpha() else ((prev * 2 - 5 - 1) % 52) + 1
                        ),
                    ),
                ),
            ),
        )
    )
)(
    open("input.txt").read().strip(),
    lambda c: (ord(c) - (ord("a") - 1 if c.islower() else ord("A") - 27)),
)
