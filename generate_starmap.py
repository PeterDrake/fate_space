import matplotlib.pyplot as plt
import random
from collections import defaultdict
from utils import *


def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return ((x1-x2)**2 + (y1-y2)**2) ** 0.5


def generate_stars(n):
    threshold = 5
    result = []
    while len(result) < n:
        s = (int(random.random() * 100), int(random.random() * 100))
        if any(distance(s, t) < threshold for t in result):
            continue
        result.append(s)
    return tuple(result)


def generate_links(stars):
    def any_intervening_stars():
        for c in stars:
            if c != stars[a] and c != stars[b]:
                d = distance(stars[a], stars[b])
                if distance(stars[a], c) < d and distance(stars[b], c) < d:
                    return True
        return False
    links = defaultdict(tuple)
    for a in range(len(stars)):
        for b in range(len(stars)):
            if a != b and not any_intervening_stars():
                links[a] += (b,)
    return links


def generate_starmap(n):
    stars = generate_stars(n)
    links = generate_links(stars)
    return stars, links


def plot_starmap(stars, names, links):
    plt.figure(figsize=(6, 6), dpi=200).add_subplot().set_aspect('equal')
    plt.xlim([-5, 105])
    plt.ylim([-5, 105])
    plt.grid()
    for s, n in zip(stars, names):
        plt.annotate(n, s, textcoords='offset points', xytext=(0, 5), ha='center', size='4')
    for a in links:
        for b in links[a]:
            plt.plot(*zip(stars[a], stars[b]), 'r')
    plt.scatter(*zip(*stars), color='k', zorder=2)
    plt.savefig('starmap.png', bbox_inches='tight')
    plt.show()


TECH_LEVELS = ('Nigh magical', 'Advanced whipdrive', 'Primitive whipdrive', 'Sublight', 'Orbital', 'Industrial',
               'Medieval', 'Iron age', 'Stone age')
ENVIRONS = ('Garden', 'Forest', 'Swamp', 'Water', 'Desert', 'Ice', 'Volcano', 'Vacuum', 'Asteroid')


# This all needs to updated to use a dataframe
def print_starmap(stars, names, links, techs, environs):
    print('Index,Name,X,Y,Whiplines,Tech,Environment')
    for i in range(len(stars)):
        print(f'{i},"{i}",{stars[i][0]},{stars[i][1]},"{links[i]}",{techs[i]},{environs[i]}')


def read_starmap(file):
    import csv
    with open(file) as f:
        reader = tuple(csv.DictReader(f))
    stars = tuple((int(r['X']), int(r['Y'])) for r in reader)
    names = tuple(r['Name'] for r in reader)
    links = {i: eval(r['Whiplines']) for i, r in enumerate(reader)}
    techs = tuple(r['Tech'] for r in reader)
    environs = tuple(r['Environment'] for r in reader)
    print(stars)
    print(links)
    return stars, names, links, techs, environs


def main():
    # stars, links = generate_starmap(100)
    # names = tuple(range(len(stars)))
    # techs = tuple(TECH_LEVELS[roll_df(4) + 4] for _ in stars)
    # environs = tuple(ENVIRONS[roll_df(4) + 4] for _ in stars)
    stars, names, links, techs, environs = read_starmap('systems.csv')
    print_starmap(stars, names, links, techs, environs)
    plot_starmap(stars, names, links)  # Could we show tech and environ as color and shape?


if __name__ == '__main__':
    main()
