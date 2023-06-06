import matplotlib.pyplot as plt
#matplotlib inline
import numpy as np
from math import cos,sin

x0 = np.array([0,0,-np.pi/4.])
xG = np.array([6.,4.,-np.pi/4])


def plot_pose(x,col):
  # small length just for plotting
  d = np.array([0,0.2])
  # plot a dot with a pointing line
  plt.plot(x[0]+d*cos(x[2]),x[1]+d*sin(x[2]),col)
  plt.plot(x[0],x[1],col+'o')

plot_pose(x0,'m')
plot_pose(xG,'g')

#plt.show()

def f(x,u):
    return(np.array([u[0]*cos(x[2]),u[0]*sin(x[2]),u[0]*u[1]]))

# define decision variable as vector of [time,curv,time,curv,time,curv]
# here: turn with curvature 1. for 1.5 seconds, than 0. (straight) for 3. seconds, and finally turn with curvature -1. for 1.5 seconds. 
z = np.array([1.5,1.,3.,0.,1.5,-2.])

from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

def path(z,x0):
    # make sure it has even number of elements
    nz = len(z)
    assert(nz%2==0)
    # curvature values
    kv = z[range(1,nz,2)]
    # time intervals
    dv = z[range(0,nz,2)]
    # if given a negative time intervals, make it zero
    dv = [max(v,0) for v in dv]
    # now construct function to interpolate commands over time
    nv = len(kv)
    uv = np.vstack((np.ones((1,nv+1)),np.hstack((kv,0.))))
    tv = np.cumsum(np.append(0,dv))
    te=np.linspace(0.,max(tv),100)
    ut = interp1d(tv,uv,axis=1,kind='previous',bounds_error=False,fill_value='extrapolate')
    # use this to define the uncontrolled dynamics: x-dot=fc(x,t)
    def fc(t,x):
        u = ut(t)
        return(f(x,u))
    # and do the integration
    r = solve_ivp(fc,(min(te),max(te)),x0,t_eval=te)
    return(r.y)

p = path(z,x0)

plt.plot(p[0,:],p[1,:])
plot_pose(x0,'m')
plot_pose(xG,'g')
plt.axis('equal')
#plt.show()


from scipy.linalg import norm
curvature_limit = 1.5

def path_cost(z):
    p = path(z,x0)
    goal_miss_distance = norm(p[0:3,-1]-xG)
    total_time_flown = sum(z[range(0,len(z),2)])
    curvature_excess = [max(abs(c)-curvature_limit,0.) for c in z[range(1,len(z),2)]]
    J = total_time_flown + 1000.*goal_miss_distance + 10000.*sum(curvature_excess)
    return(J)

print(path_cost(z))
from scipy.optimize import minimize

r = minimize(path_cost,z,method='Powell')
print(r)

popt = path(r.x,x0)
plt.plot(p[0,:],p[1,:],'m')
plt.plot(popt[0,:],popt[1,:])
plot_pose(x0,'m')
plot_pose(xG,'g')
plt.axis('equal')
plt.show()