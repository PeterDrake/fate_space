import matplotlib.pyplot as plt
from utils import *
import pandas as pd


class Starmap:
    def __init__(self, *, filename=None, n=100, minimum_distance=5):
        if filename:
            self.data = pd.read_csv(filename)
            self.data['ID'] = [int(i) for i in self.data['ID']]
            self.data['Coordinates'] = [eval(c) for c in self.data['Coordinates']]
            self.data['Links'] = [eval(c) for c in self.data['Links']]
            print(self.data['Coordinates'])
        else:
            self.data = pd.DataFrame(range(n), columns=['ID'])
            self.data['Name'] = [str(i) for i in self.data['ID']]
            self.__generate_coordinates(n, minimum_distance)
            self.__generate_links()
            # self.data.set_index('ID', inplace=True)
            # print(self.data)

    def __generate_coordinates(self, n, minimum_distance):
        def f():
            result = []
            while len(result) < n:
                s = (int(random.random() * 100), int(random.random() * 100))
                if any(distance(s, t) < minimum_distance for t in result):
                    continue
                result.append(s)
            return result
        self.data['Coordinates'] = f()

    def __generate_links(self):
        d = self.data

        def any_intervening_stars(a, b):
            dist = distance(a, b)
            return any(c for c in d['Coordinates'] if c != a and distance(a, c) < dist and distance(b, c) < dist)

        def links(a):
            return tuple(i for i, b in zip(d['ID'], d['Coordinates']) if not any_intervening_stars(a, b))
        d['Links'] = [links(a) for a in d['Coordinates']]

    def plot(self, filename):
        d = self.data
        plt.figure(figsize=(6, 6), dpi=200).add_subplot().set_aspect('equal')
        plt.xlim([-5, 105])
        plt.ylim([-5, 105])
        plt.grid()
        for a in d['ID']:
            for b in d.iloc[a]['Links']:
                plt.plot(*zip(d.iloc[a]['Coordinates'], d.iloc[b]['Coordinates']), 'r')
        for n, c in zip(d['Name'], d['Coordinates']):
            plt.annotate(n, c, textcoords='offset points', xytext=(0, 5), ha='center', size='4', zorder=3)
        plt.scatter(*zip(*d['Coordinates']), color='k', zorder=2)
        plt.savefig(filename, bbox_inches='tight')
        plt.show()

    def save(self, filename):
        print('Saving to ' + filename)
        self.data.to_csv(filename)

# def generate_starmap(n):
#     stars = generate_stars(n)
#     links = generate_links(stars)
#     return stars, links
#
#

#
#
# TECH_LEVELS = ('Nigh magical', 'Advanced whipdrive', 'Primitive whipdrive', 'Sublight', 'Orbital', 'Industrial',
#                'Medieval', 'Iron age', 'Stone age')
# ENVIRONS = ('Garden', 'Forest', 'Swamp', 'Water', 'Desert', 'Ice', 'Volcano', 'Vacuum', 'Asteroid')
#
#
# # This all needs to updated to use a dataframe
# def print_starmap(stars, names, links, techs, environs):
#     print('Index,Name,X,Y,Whiplines,Tech,Environment')
#     for i in range(len(stars)):
#         print(f'{i},"{i}",{stars[i][0]},{stars[i][1]},"{links[i]}",{techs[i]},{environs[i]}')
#
#
# def read_starmap(file):
#     import csv
#     with open(file) as f:
#         reader = tuple(csv.DictReader(f))
#     stars = tuple((int(r['X']), int(r['Y'])) for r in reader)
#     names = tuple(r['Name'] for r in reader)
#     links = {i: eval(r['Whiplines']) for i, r in enumerate(reader)}
#     techs = tuple(r['Tech'] for r in reader)
#     environs = tuple(r['Environment'] for r in reader)
#     print(stars)
#     print(links)
#     return stars, names, links, techs, environs
#
#
# def main():
#     # stars, links = generate_starmap(100)
#     # names = tuple(range(len(stars)))
#     # techs = tuple(TECH_LEVELS[roll_df(4) + 4] for _ in stars)
#     # environs = tuple(ENVIRONS[roll_df(4) + 4] for _ in stars)
#     stars, names, links, techs, environs = read_starmap('systems.csv')
#     print_starmap(stars, names, links, techs, environs)
#     plot_starmap(stars, names, links)  # Could we show tech and environ as color and shape?


if __name__ == '__main__':
    m = Starmap(filename='starmap.csv')
    m.plot('starmap.png')
    # m.save('starmap.csv')

