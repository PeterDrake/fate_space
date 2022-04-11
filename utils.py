import random


def distance(a, b):
    """
    Returns the Euclidean distance between pairs a and b.
    """
    x1, y1 = a
    x2, y2 = b
    return ((x1-x2)**2 + (y1-y2)**2) ** 0.5


def roll_df(n):
    """Roll n FATE dice and return their sum."""
    return sum(random.choice((-1, 0, 1)) for _ in range(n))
