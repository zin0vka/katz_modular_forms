from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

def sphere(rows, cols, radius=1.0, offset=True):
    """
    Return a MeshData instance with vertexes and faces computed
    for a spherical surface.
    """
    verts = np.empty((rows+1, cols, 3), dtype=float)
    
    ## comute vertexes
    phi = (np.arange(rows+1) * np.pi / rows).reshape(rows+1, 1)
    s = radius * np.sin(phi)
    verts[...,2] = radius * np.cos(phi)
    th = ((np.arange(cols) * 2 * np.pi / cols).reshape(1, cols)) 
    if offset:
        th = th + ((np.pi / cols) * np.arange(rows+1).reshape(rows+1,1))  ## rotate each row by 1/2 column
    verts[...,0] = s * np.cos(th)
    verts[...,1] = s * np.sin(th)
    verts = verts.reshape((rows+1)*cols, 3)[cols-1:-(cols-1)]  ## remove redundant vertexes from top and bottom
    
    ## compute faces
    faces = np.empty((rows*cols*2, 3), dtype=np.uint)
    rowtemplate1 = ((np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 0]])) % cols) + np.array([[0, 0, cols]])
    rowtemplate2 = ((np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 1]])) % cols) + np.array([[cols, 0, cols]])
    for row in range(rows):
        start = row * cols * 2 
        faces[start:start+cols] = rowtemplate1 + row * cols
        faces[start+cols:start+(cols*2)] = rowtemplate2 + row * cols
    faces = faces[cols:-cols]  ## cut off zero-area triangles at top and bottom
    
    ## adjust for redundant vertexes that were removed from top and bottom
    vmin = cols-1
    faces[faces<vmin] = vmin
    faces -= vmin  
    vmax = verts.shape[0]-1
    faces[faces>vmax] = vmax
    
    return gl.MeshData(vertexes=verts, faces=faces)

#Based on this formula
#x = (R + r*np.cos(theta))*np.cos(phi)
#y = (R + r*np.cos(theta))*np.sin(phi)
#z = r*np.sin(theta)

def torus(rows, cols, r=1.0, R=2.0, offset=True):
    verts = np.empty((rows+1, cols, 3), dtype=float)
    
    ## compute vertexes
    phi = (np.arange(rows+1) * 2 * np.pi / rows).reshape(rows+1, 1)
    th = ((np.arange(cols) * 2 * np.pi / cols).reshape(1, cols)) 
    verts[...,2] = r * np.sin(th)
    s = R + r*np.cos(th)
    if offset:
        th = th + ((np.pi / cols) * np.arange(rows+1).reshape(rows+1,1))  ## rotate each row by 1/2 column
    verts[...,0] = s * np.cos(phi)
    verts[...,1] = s * np.sin(phi)
    verts = verts.reshape((rows+1)*cols, 3)#[cols-1:-(cols-1)]  ## remove redundant vertexes from top and bottom
    
    ## compute faces
    faces = np.empty((rows*cols*2, 3), dtype=np.uint)
    rowtemplate1 = ((np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 0]])) % cols) + np.array([[0, 0, cols]])
    rowtemplate2 = ((np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 1]])) % cols) + np.array([[cols, 0, cols]])
    for row in range(rows):
        start = row * cols * 2 
        faces[start:start+cols] = rowtemplate1 + row * cols
        faces[start+cols:start+(cols*2)] = rowtemplate2 + row * cols
    
    return gl.MeshData(vertexes=verts, faces=faces)


app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLMeshItem')
w.setCameraPosition(distance=40)

g = gl.GLGridItem()
g.scale(2,2,1)
w.addItem(g)

r=2
R=6

row_RES = 600
col_RES = 600
md = torus(rows=row_RES, cols=col_RES, R=R, r=r)
verts = md.vertexes()
faces = md.faces()
#this should be the same number of vertices as in the torus
close_verts = []
nbr_verts,_ = verts.shape
nbr_faces,_ = faces.shape
#finding vertices to give a special color
for ix in range(0,nbr_verts):
    if (verts[ix,0]-R)**2+verts[ix,1]**2+(verts[ix,2]-r)**2 <= 1.0:
        close_verts.append(ix)

vcolors =np.empty((nbr_verts, 4), dtype=float)
for ix in range(0,nbr_verts):
    if not ix in close_verts:
        vcolors[ix] = (1, 0, 0, 1)
    else:
        vcolors[ix] = (0, 1, 0, 1)

#fcolors = np.empty((nbr_faces,4), dtype=float)
#for ix in range(0,nbr_faces):
#    if not all([v in close_verts for v in faces[ix]]):
#        fcolors[ix] = (1, 0, 0, 1)
#    else:
#        fcolors[ix] = (0, 1, 0, 1)

md.setVertexColors(vcolors)
#md.setFaceColors(fcolors)
m3 = gl.GLMeshItem(meshdata=md, smooth=True, shader='shaded', glOptions='opaque')
w.addItem(m3)

#now we add some scatter plotted pts
pos = np.empty((1, 3))
size = np.empty((1))
color = np.empty((1, 4))
pos[0] = (R,0,r); size[0] = 0.25;   color[0] = (1.0, 1.0, 0.0, 1)
sp1 = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
w.addItem(sp1)


md1 = sphere(rows=100, cols=200, radius=1)
m4 = gl.GLMeshItem(meshdata=md1, smooth=True, shader='shaded', glOptions='translucent',
    color=(0, 0, 1, 0.4))
m4.translate(R,0,r)
w.addItem(m4)

#line plots for the ``local axes''
RES = 500
th = np.linspace(0,2*np.pi,RES)
xzpos = np.empty((RES,3))
for ix in range(0,RES):
    xzpos[ix] = (r*np.cos(th[ix])+R,0,r*np.sin(th[ix]))

xypos = np.empty((RES,3))
for ix in range(0,RES):
    xypos[ix] = (R*np.cos(th[ix]),R*np.sin(th[ix]),2)

xz_circ = gl.GLLinePlotItem(pos=xzpos, color=(1,1,0,1), width=2, antialias=True)
xy_circ = gl.GLLinePlotItem(pos=xypos, color=(1,1,0,1), width=2, antialias=True)
w.addItem(xz_circ) 
w.addItem(xy_circ)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
