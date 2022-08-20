import matplotlib.pyplot as plt
from utils import *
import pandas as pd

TECH_LEVELS = ('-4 Stone age',
               '-3 Iron age',
               '-2 Medieval',
               '-1 Industrial',
               '0 Orbital',
               '+1 Sublight',
               '+2 Primitive whipdrive',
               '+3 Advanced whipdrive',
               '+4 Nigh magical')

ENVIRONMENTS = ('Asteroid',
                'Vacuum',
                'Volcano',
                'Ice',
                'Desert',
                'Water',
                'Swamp',
                'Forest',
                'Garden')


class Starmap:
    def __init__(self, *, filename=None, n=100, minimum_distance=5):
        if filename:
            self.data = pd.read_csv(filename)
            # Some columns have to be converted from strings to tuples
            self.data['Coordinates'] = [eval(c) for c in self.data['Coordinates']]
            self.data['Whiplines'] = [eval(c) for c in self.data['Whiplines']]
        else:
            self.data = pd.DataFrame(range(n), columns=['ID'])
            self.data['Name'] = [str(i) for i in self.data['ID']]
            self.__generate_coordinates(n, minimum_distance)
            self.__generate_links()
            self.__generate_tech_levels()
            self.__generate_environments()
        print(self.data)

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

        d['Whiplines'] = [links(a) for a in d['Coordinates']]

    def __generate_tech_levels(self):
        d = self.data
        d['Tech level'] = [TECH_LEVELS[roll_df(4) + 4] for _ in d['ID']]

    def __generate_environments(self):
        d = self.data
        d['Environment'] = [ENVIRONMENTS[roll_df(4) + 4] for _ in d['ID']]

    def plot(self, filename):
        d = self.data
        ax = plt.figure(figsize=(6, 6), dpi=200).add_subplot()
        ax.set_aspect('equal')
        # Entire map
        plt.xlim([-5, 105])
        plt.ylim([-5, 105])
        # Specific region
        # plt.xlim([35, 90])
        # plt.ylim([-5, 50])
        plt.grid()
        # Plot whiplines
        for a in d['ID']:
            for b in d.iloc[a]['Whiplines']:
                plt.plot(*zip(d.iloc[a]['Coordinates'], d.iloc[b]['Coordinates']), 'b', linewidth=0.5)
        # Plot names of systems
        for n, c in zip(d['Name'], d['Coordinates']):  # Size 4 works if you want the entire map
            plt.annotate(n, c, textcoords='offset points', xytext=(0, 5), ha='center', size='4', zorder=3)
        # Plot systems, with size based on tech level and color on environment
        sizes = [1 + 5 * TECH_LEVELS.index(t) for t in d['Tech level']]
        colors = [ENVIRONMENTS.index(e) for e in d['Environment']]
        scatter = plt.scatter(*zip(*d['Coordinates']), c=colors, s=sizes, zorder=2)
        tech_labels = [t for t in TECH_LEVELS if any(d['Tech level'] == t)]
        legend1 = ax.legend(scatter.legend_elements(prop='sizes')[0], tech_labels,
                            loc='upper left', title="Tech level", bbox_to_anchor=(0, -0.1))
        ax.add_artist(legend1)
        env_labels = (e for e in ENVIRONMENTS if any(d['Environment'] == e))
        legend2 = ax.legend(scatter.legend_elements(prop='colors')[0], env_labels,
                            loc='upper right', title="Environment", bbox_to_anchor=(1, -0.1))
        ax.add_artist(legend2)
        plt.savefig(filename, bbox_inches='tight')
        plt.show()

    def save(self, filename):
        print('Saving to ' + filename)
        self.data.to_csv(filename, index=False)


if __name__ == '__main__':
    # One of the two lines below should be uncommented
    # m = Starmap(n=100)  # Generate a new starmap
    m = Starmap(filename='starmap.csv')  # Read a saved starmap
    m.plot('starmap.png')
    # m.save('starmap.csv')
