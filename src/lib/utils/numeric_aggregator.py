from statistics import mean, median


def aggregate(vals: list):
    """Takes in a Iterable of numeric values and returns a tuple `(min, max, avg, median)`."""
    if len(vals) == 0:
        return (0, 0, 0, 0)

    return (min(vals), max(vals), mean(vals), median(vals))
