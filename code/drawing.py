# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:47:20 2016

@author: GONG
"""
#加载科学计算宏包
import numpy as np
import scipy as si
import pylab as pl
#加载绘图相关宏包
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

##############################################################
#       此程序一切数据处理都非常多余且没道理。。                 
#       所有目的只是为了满足进行三角绘图trisurf的输入格式        
#       暂时没有发现其他方法。。                                
##############################################################

r=np.load("Boundary.npz")
x=r["arr_0"]
y=r["arr_1"]
z=r["arr_2"]

tri=np.empty(x.shape,int)
a=x.shape[0]
x1=x.reshape(1,-1)
y1=y.reshape(1,-1)
z1=z.reshape(1,-1)

b=x1.shape[1]

x=np.arange(b,dtype=float)
y=np.arange(b,dtype=float)
z=np.arange(b,dtype=float)



n=0
for i in range(a):
    for j in range(3):
        tri[i,j]=n
        n=n+1

for i in range(b):
    x[i]=x1[0,i]
    y[i]=y1[0,i]
    z[i]=z1[0,i]
    

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot_trisurf(x, y, z, triangles=tri,cmap=cm.jet, linewidth=0.5)
ax.view_init(elev=30,azim=20)
#ax.view_init(elev=0,azim=45)
#ax.view_init(elev=45,azim=0)
ax.set_xlabel('X AXIS')
ax.set_ylabel('Y AXIS')
ax.set_zlabel('Z AXIS')
ax.set_title('SHAPE OF APOLLO')
plt.ylim(-1000,4000)
plt.grid(True)

plt.savefig('HopeX.jpg',dpi=720)
plt.savefig('HopeX.eps')
plt.show()


