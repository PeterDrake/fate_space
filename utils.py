import random


def roll_df(n):
    return sum(random.choice((-1, 0, 1)) for _ in range(n))
