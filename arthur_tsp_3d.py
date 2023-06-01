import matplotlib.pyplot as plt
import numpy as np
import random
from pulp import *

visit_points = np.array([[random.randrange(0, 10), random.randrange(0, 10), random.randrange(0, 10)] for _ in range(20)])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(visit_points[:, 0], visit_points[:, 1], visit_points[:, 2], c='g')

distance = np.zeros((20, 20))
for i in range(20):
    for j in range(i, 20):
        distance[i, j] = np.linalg.norm(visit_points[i] - visit_points[j])
        distance[j, i] = distance[i, j]

n = len(visit_points)
links = [(i, j) for i in range(n) for j in range(n) if j != i]

prob = LpProblem('tsp', LpMinimize)
x = LpVariable.dicts("x", links, 0, 1, LpInteger)

prob.setObjective(sum([distance[i, j] * x[i, j] for (i, j) in links]))

for i in range(n):
    prob += (sum(x[ic, j] for (ic, j) in links if ic == i) == 1)
for j in range(n):
    prob += (sum(x[i, jc] for (i, jc) in links if jc == j) == 1)

v = LpVariable.dicts("v", range(n), 0, n)
for (i, j) in links:
    if j != 0:
        prob += (v[j] >= v[i] + 1 - n * (1 - x[i, j]))

prob.solve()
print("Status:", LpStatus[prob.status])
[(i, j, x[i, j].value()) for (i, j) in links]

for (ii, jj) in links:
    if x[ii, jj].value() == 1.:
        ax.plot(
            [visit_points[ii, 0], visit_points[jj, 0]],
            [visit_points[ii, 1], visit_points[jj, 1]],
            [visit_points[ii, 2], visit_points[jj, 2]],
            'm-'
        )

ax.scatter(visit_points[:, 0], visit_points[:, 1], visit_points[:, 2], c='g')
plt.show()
