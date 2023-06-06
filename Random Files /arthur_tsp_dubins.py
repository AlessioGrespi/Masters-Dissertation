import matplotlib.pyplot as plt
import numpy as np
import random
from pulp import *

visit_points = np.array([[random.randrange(0,10), random.randrange(0,10)] for ii in range(20)])

plt.plot(visit_points[:,0], visit_points[:,1],'g.')

from math import sqrt
distance = np.zeros((20,20))
for ii in range(20):
    for jj in range(ii,20):
        distance[ii,jj] = sqrt(sum((visit_points[ii,:]-visit_points[jj,:])**2))
        distance[jj,ii] = distance[ii,jj]

n = len(visit_points)
links = [(i,j) for i in range(n) for j in range(n) if j != i]

prob = LpProblem('tsp', LpMinimize)
x = LpVariable.dicts("x", links, 0, 1, LpInteger)

prob.setObjective(sum([distance[i,j]*x[i,j] for (i,j) in links]))

for i in range(n):
    prob += (sum(x[ic,j] for (ic,j) in links if ic == i) == 1)
for j in range(n):
    prob += (sum(x[i,jc] for (i,jc) in links if jc == j) == 1)

v = LpVariable.dicts("v", range(n), -n, n)

curvature_limit = 1.5

for (i,j) in links:
    if j != 0:
        prob += (v[j] >= v[i] + 1 - n * (1 - x[i,j]))
        prob += (v[j] - v[i] <= curvature_limit * x[i,j])
        prob += (v[i] - v[j] <= curvature_limit * (1 - x[i,j]))

prob.solve()
print("Status:", LpStatus[prob.status])
[(i,j,x[i,j].value()) for (i,j) in links]

for (ii,jj) in links:
    if x[ii,jj].value() == 1.:
        plt.plot([visit_points[ii,0],visit_points[jj,0]], [visit_points[ii,1],visit_points[jj,1]],'m-')
plt.plot(visit_points[:,0], visit_points[:,1],'g.')
plt.show()
