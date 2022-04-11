# This just plots a picture to show what counts as an "intervening" star

from generate_starmap import *

a = (0.25, 0.5)
b = (0.75, 0.5)

points = [(random.random(), random.random()) for _ in range(2000)]

inside = [p for p in points if distance(a, p) < 0.5 and distance(b, p) < 0.5]
outside = [p for p in points if not (distance(a, p) < 0.5 and distance(b, p) < 0.5)]

plt.figure().add_subplot().set_aspect('equal')
plt.scatter(*zip(*inside), color='r', s=1)
plt.scatter(*zip(*outside), color='k', s=1)
plt.scatter(*zip(*[a, b]), color='b')
plt.show()
