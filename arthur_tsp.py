import matplotlib.pyplot as plt
import numpy as np
import random
from pulp import *

# Generate random coordinates for visiting points
visit_points = np.array([[random.randrange(0,10), random.randrange(0,10)] for ii in range(20)])

# Plot the visit points on a graph
plt.plot(visit_points[:,0], visit_points[:,1],'g.')

# Calculate the distance between each pair of visit points
from math import sqrt
distance = np.zeros((20,20))
for ii in range(20):
    for jj in range(ii,20):
        distance[ii,jj] = sqrt(sum((visit_points[ii,:]-visit_points[jj,:])**2))
        distance[jj,ii]=distance[ii,jj]

# Define the number of visit points
n = len(visit_points)

# Create all possible links between visit points
links = [(i,j) for i in range(n) for j in range(n) if j!=i]

# Create a linear programming problem
prob = LpProblem('tsp',LpMinimize)

# Create binary decision variables for each link
x = LpVariable.dicts("x",links,0,1,LpInteger)

# Set the objective function of the problem
prob.setObjective(sum([distance[i,j]*x[i,j] for (i,j) in links]))

# Add constraints to ensure that each visit point is visited exactly once
for i in range(n):
    prob += (sum(x[ic,j] for (ic,j) in links if ic==i)==1)

# Add constraints to ensure that each visit point is left exactly once
for j in range(n):
    prob += (sum(x[i,jc] for (i,jc) in links if jc==j)==1)

# Add constraints to eliminate subtours by using Miller-Tucker-Zemlin (MTZ) formulation
v = LpVariable.dicts("v",range(n),0,n)
for (i,j) in links:
    if j!=0:
        prob += (v[j] >= v[i] + 1 - n*(1-x[i,j]))

# Solve the problem
prob.solve()

# Print the status of the problem solution
print("Status:", LpStatus[prob.status])

# Print the selected links in the optimal solution
[(i,j,x[i,j].value()) for (i,j) in links]

# Plot the optimal tour on the graph
for (ii,jj) in links:
    if x[ii,jj].value()==1.:
        plt.plot([visit_points[ii,0],visit_points[jj,0]],[visit_points[ii,1],visit_points[jj,1]],'m-')
plt.plot(visit_points[:,0], visit_points[:,1],'g.')
plt.show()
