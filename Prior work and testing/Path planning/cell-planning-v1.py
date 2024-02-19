import matplotlib.pyplot as plt
import numpy as np
import random

# Define the obstacles as arrays of points
obstacles = [np.array([[2.,6.],[8.,5.],[5.,3.]]),np.array([[6.5,7.],[8.5,7.],[9.,9.],[8.,7.5]])]
obstacles.append(np.array([[3,7],[6.75,5.95],[4.5,7],[7,8],[6,9]]))

# Function to plot a polygon given its points
def plot_poly(points,fmt='b-',**kwargs):
    plt.plot(np.append(points[:,0],points[0,0]),np.append(points[:,1],points[0,1]),fmt)

# Plot the obstacles
for ob in obstacles:
    plot_poly(ob,'r-')
# plt.show() 

# Check if two lines, defined by points (a, b) and (c, d), intersect
def lines_cross(a,b,c,d):
    M = np.array([[b[0]-a[0],c[0]-d[0]],[b[1]-a[1],c[1]-d[1]]])
    if np.linalg.det(M)==0.:
        return(False)
    v = np.array([[c[0]-a[0]],[c[1]-a[1]]])
    w = np.linalg.solve(M,v)
    if w[0]<=0:
        return(False)
    elif w[0]>=1:
        return(False)
    elif w[1]<=0:
        return(False)
    elif w[1]>=1:
        return(False)
    else:
        return(True)
    
def line_crosses_obst(a,b,obst):
    # Check if a line segment (a, b) intersects with any of the obstacles
    for ii in range(len(obst)):
        if lines_cross(a,b,obst[ii-1],obst[ii]):
            return(True)
    # extra test in case line is completely inside
    num_crosses = 0
    for ii in range(len(obst)):
        if lines_cross(0.5*(a+b),[max(obst[:,0])+0.01,max(obst[:,1])+0.01],obst[ii-1],obst[ii]):
            num_crosses = num_crosses+1
    if num_crosses%2==1:
        return(True)
    return(False)
            
def is_visible(a,b,obstacles):
    # Check if a line segment (a, b) is visible, i.e., not obstructed by any obstacles
    for ob in obstacles:
        if line_crosses_obst(a,b,ob):
            return(False)
    return(True)

def is_free(xlo,ylo,xhi,yhi,obstacles):
    # Check if a rectangular cell defined by (xlo, ylo) and (xhi, yhi) is free from obstacles
    for ob in obstacles:
        for p in ob[:]:
            if p[0]>xlo and p[0]<xhi:
                if p[1]>ylo and p[1]<yhi:
                    return(False)
    if not is_visible(np.array([xlo,ylo]),np.array([xlo,yhi]),obstacles):
        return(False)
    elif not is_visible(np.array([xlo,yhi]),np.array([xhi,yhi]),obstacles):
        return(False)
    elif not is_visible(np.array([xhi,yhi]),np.array([xhi,ylo]),obstacles):
        return(False)
    elif not is_visible(np.array([xhi,ylo]),np.array([xlo,ylo]),obstacles):
        return(False)
    else:
        return(True)
    
cells = []
tol = 0.6

def quadtree(xlo,ylo,xhi,yhi,obstacles):
    #print(xlo,ylo,xhi,yhi)
    assert(xhi>xlo)
    assert(yhi>ylo)
    #plt.plot([xlo,xlo,xhi,xhi,xlo],[ylo,yhi,yhi,ylo,ylo],'b-')
    if is_free(xlo,ylo,xhi,yhi,obstacles):
        plt.plot([xlo+0.1,xlo+0.1,xhi-0.1,xhi-0.1,xlo+0.1],[ylo+0.1,yhi-0.1,yhi-0.1,ylo+0.1,ylo+0.1],'g-')
        cells.append((xlo,ylo,xhi,yhi))
    elif xhi>xlo+tol:
        quadtree(xlo,ylo,0.5*(xlo+xhi),0.5*(ylo+yhi),obstacles)
        quadtree(0.5*(xlo+xhi),0.5*(ylo+yhi),xhi,yhi,obstacles)
        quadtree(xlo,0.5*(ylo+yhi),0.5*(xlo+xhi),yhi,obstacles)
        quadtree(0.5*(xlo+xhi),ylo,xhi,0.5*(ylo+yhi),obstacles)
    
bl = [0.,0.]
tr = [10.,10.]
quadtree(bl[0],bl[1],tr[0],tr[1],obstacles)

for ob in obstacles:
    plot_poly(ob,'r-')

plt.show()

print(cells)

###########################################

num_cells = len(cells)
nodes = []
cell_nodes = [[] for c in cells]

d = np.inf+np.zeros((4*num_cells,4*num_cells))
from numpy.linalg import norm

for ii in range(num_cells):
    (xlo,ylo,xhi,yhi) = cells[ii]
    #plt.plot([xlo,xlo,xhi,xhi,xlo],[ylo,yhi,yhi,ylo,ylo],'b-')
    for jj in range(num_cells):
        (xlo2,ylo2,xhi2,yhi2) = cells[jj]
        # look for neighbours to the right
        if xlo2==xhi and ylo2<yhi and yhi2>ylo:
            yloi = max((ylo,ylo2))
            yhii = min((yhi,yhi2))
            new_node = np.array([xhi,0.5*(yloi+yhii)])
            #plt.plot(new_node[0],new_node[1],'*c')
            new_node_idx = len(nodes)
            for kk in cell_nodes[ii]:
                #plt.plot([nodes[kk][0],new_node[0]],[nodes[kk][1],new_node[1]],'c')
                d[kk,new_node_idx] = norm(nodes[kk]-new_node)
                d[new_node_idx,kk] = d[kk,new_node_idx]
            for kk in cell_nodes[jj]:
                #plt.plot([nodes[kk][0],new_node[0]],[nodes[kk][1],new_node[1]],'c')
                d[kk,new_node_idx] = norm(nodes[kk]-new_node)
                d[new_node_idx,kk] = d[kk,new_node_idx]
            nodes.append(new_node)
            cell_nodes[ii].append(new_node_idx)
            cell_nodes[jj].append(new_node_idx)
        # and look for neighbours to the top
        if ylo2==yhi and xlo2<xhi and xhi2>xlo:
            xloi = max((xlo,xlo2))
            xhii = min((xhi,xhi2))
            new_node = np.array([0.5*(xloi+xhii),yhi])
            #plt.plot(new_node[0],new_node[1],'*c')
            new_node_idx = len(nodes)
            for kk in cell_nodes[ii]:
                #plt.plot([nodes[kk][0],new_node[0]],[nodes[kk][1],new_node[1]],'c')
                d[kk,new_node_idx] = norm(nodes[kk]-new_node)
                d[new_node_idx,kk] = d[kk,new_node_idx]
            for kk in cell_nodes[jj]:
                #plt.plot([nodes[kk][0],new_node[0]],[nodes[kk][1],new_node[1]],'c')
                d[kk,new_node_idx] = norm(nodes[kk]-new_node)
                d[new_node_idx,kk] = d[kk,new_node_idx]
            nodes.append(new_node)
            cell_nodes[ii].append(new_node_idx)
            cell_nodes[jj].append(new_node_idx)

# plt.show()

d = d[0:len(nodes),0:len(nodes)]
print(d)

start_point = np.array([random.randrange(bl[0],tr[0]), random.randrange(bl[1],tr[1])])
start_list = [ii for ii in range(num_cells) if cells[ii][0]<=start_point[0] and cells[ii][1]<=start_point[1] and cells[ii][2]>=start_point[0] and cells[ii][3]>=start_point[1]]
for rr in range(10):
  if start_list:
    break
  else:
    start_point = np.array([random.randrange(bl[0],tr[0]), random.randrange(bl[1],tr[1])])
    start_list = [ii for ii in range(num_cells) if cells[ii][0]<=start_point[0] and cells[ii][1]<=start_point[1] and cells[ii][2]>=start_point[0] and cells[ii][3]>=start_point[1]]
start_cell = start_list[0]
print(start_cell)

goal_point = np.array([random.randrange(bl[0],tr[0]), random.randrange(bl[1],tr[1])])
goal_list = [ii for ii in range(num_cells) if cells[ii][0]<=goal_point[0] and cells[ii][1]<=goal_point[1] and cells[ii][2]>=goal_point[0] and cells[ii][3]>=goal_point[1]]
for rr in range(10):
  if goal_list:
    break
  else:
    goal_point = np.array([random.randrange(bl[0],tr[0]), random.randrange(bl[1],tr[1])])
    goal_list = [ii for ii in range(num_cells) if cells[ii][0]<=goal_point[0] and cells[ii][1]<=goal_point[1] and cells[ii][2]>=goal_point[0] and cells[ii][3]>=goal_point[1]]
goal_cell = goal_list[0]
print(goal_cell)

for ii in range(num_cells):
    (xlo,ylo,xhi,yhi) = cells[ii]
    #if ii==start_cell:
        #plt.plot([xlo,xlo,xhi,xhi,xlo],[ylo,yhi,yhi,ylo,ylo],'m-')
    #elif ii==goal_cell:
        #plt.plot([xlo,xlo,xhi,xhi,xlo],[ylo,yhi,yhi,ylo,ylo],'g-')
    #else:
        #plt.plot([xlo,xlo,xhi,xhi,xlo],[ylo,yhi,yhi,ylo,ylo],'b-')
#plt.plot(start_point[0],start_point[1],'mo')
#plt.plot(goal_point[0],goal_point[1],'g*')
# plt.show()

def append_dist_matrix(d,n=1):
    (r,c)=d.shape
    d2 = np.vstack((d,np.inf+np.zeros((n,c))))
    d3 = np.hstack((d2,np.inf+np.zeros((r+n,n))))
    return(d3)

nx_points_aug = nodes[:]
d_aug = append_dist_matrix(d,n=2)

start_idx = len(nx_points_aug)
nx_points_aug.append(start_point)
#plt.plot(start_point[0],start_point[1],'go')
for nx in cell_nodes[start_cell]:
    #plt.plot([nx_points_aug[start_idx][0],nx_points_aug[nx][0]],[nx_points_aug[start_idx][1],nx_points_aug[nx][1]],'c-')
    d_aug[start_idx,nx]=norm(nx_points_aug[start_idx]-nx_points_aug[nx])
    d_aug[nx,start_idx]=d_aug[start_idx,nx]

goal_idx = len(nx_points_aug)
nx_points_aug.append(goal_point)
#plt.plot(goal_point[0],goal_point[1],'g*')
for nx in cell_nodes[goal_cell]:
    #plt.plot([nx_points_aug[goal_idx][0],nx_points_aug[nx][0]],[nx_points_aug[goal_idx][1],nx_points_aug[nx][1]],'c-')
    d_aug[goal_idx,nx]=norm(nx_points_aug[goal_idx]-nx_points_aug[nx])
    d_aug[nx,goal_idx]=d_aug[goal_idx,nx]

for ii in range(num_cells):
    (xlo,ylo,xhi,yhi) = cells[ii]
    if ii==start_cell:
        plt.plot([xlo,xlo,xhi,xhi,xlo],[ylo,yhi,yhi,ylo,ylo],'m-')
    elif ii==goal_cell:
        plt.plot([xlo,xlo,xhi,xhi,xlo],[ylo,yhi,yhi,ylo,ylo],'g-')
    else:
        plt.plot([xlo,xlo,xhi,xhi,xlo],[ylo,yhi,yhi,ylo,ylo],'b-')
# plt.show()

from scipy.sparse.csgraph import shortest_path
distance,predecessors = shortest_path(d_aug, return_predecessors=True)
print(distance)
print(predecessors)

curr_node = start_idx
for kk in range(len(nx_points_aug)):
    next_node = predecessors[goal_idx,curr_node]
    plt.plot([nx_points_aug[curr_node][0],nx_points_aug[next_node][0]],[nx_points_aug[curr_node][1],nx_points_aug[next_node][1]],'m-')
    curr_node=next_node
    if curr_node==goal_idx:
        break
        
for ob in obstacles:
    plot_poly(ob,'r-')
    
plt.plot(start_point[0],start_point[1],'go',goal_point[0],goal_point[1],'gx')
plt.show()