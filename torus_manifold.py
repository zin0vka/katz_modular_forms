from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

theta = np.arange(0, 2*np.pi, np.pi/1000)
phi = np.arange(0, 2*np.pi, np.pi/1000)
theta, phi = np.meshgrid(theta, phi)
R = 2
r = 1
x = (R + r*np.cos(theta))*np.cos(phi)
y = (R + r*np.cos(theta))*np.sin(phi)
z = r*np.sin(theta)
#apparently deprecated now
#ax.hold(True)
ix = 1500
jx = 500
#zorder apparently controls which thing is ``drawn first''
thept = (x[ix,jx],y[ix,jx],z[ix,jx])

#let's make a ball with radius 0.1 and center in ``thept''
theta1 = np.arange(0, np.pi, np.pi/1000)
phi1 = np.arange(0, 2*np.pi, np.pi/1000)
theta1, phi1 = np.meshgrid(theta1,phi1)
r = 0.5
x1 = thept[0] + r*np.sin(theta1)*np.cos(phi1)
y1 = thept[1] + r*np.sin(theta1)*np.sin(phi1)
z1 = thept[2] + r*np.cos(theta1)
ax.plot_surface(x1, y1, z1,
        linewidth=0, antialiased=True,zorder=8)

ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=True)
print("the pt: "+str(thept)+"\n")
ax.plot([x[ix,jx]], [y[ix,jx]], [z[ix,jx]],
        marker='.', c='blue',zorder=10)

xs1 = [x[ix,k] for k in range(0,2000)]
ys1 = [y[ix,k] for k in range(0,2000)]
zs1 = [z[ix,k] for k in range(0,2000)]
ax.plot(xs1, ys1, zs1, c='orange',zorder=9)
xs2 = [x[k,jx] for k in range(0,2000)]
ys2 = [y[k,jx] for k in range(0,2000)]
zs2 = [z[k,jx] for k in range(0,2000)]
ax.plot(xs2, ys2, zs2, c='orange',zorder=9)


# Customize the z axis.
ax.set_zlim(-3.01, 3.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
