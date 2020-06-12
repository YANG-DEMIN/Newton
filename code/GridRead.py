# -*- coding: utf-8 -*-
"""
This program is used for reading the grid data from a SU2 flie

@Author:DuoGong

@School:NPU

Created on:5.18.2016

"""
"""
@Editor:YangDemin

@School:NPU

Edited on:6.12.2020

"""
#加载科学计算宏包
import numpy as np
import scipy as si
import pylab as pl
import sys
#加载绘图相关宏包
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

print("""
This program is used for reading the grid data from a SU2 flie

""")
#输入网格文件名，并逐行读取网格文件

f=open(r'../mesh/APOLLO.su2')               #打开su2文件
text=f.readlines()                  #读取

#根据关键字，读取网格信息
for i in range (len(text)):
    l=text[i]                           #l represents the data of each lines
    identifier=l.split()[0]             #first str in each lines
    if identifier == '%':
        continue
    if identifier =='NDIME=':           #dimension
        Ndime=int(l.split()[1]) 
        print ('It is a' ,Ndime, 'dimensional grid.')
        continue
    if identifier =='NPOIN=':           #Grid Point number
        Npoin=int(l.split()[1])
        print ('There are',Npoin,'points in this grid.')
        Point_line=i                    #the starting line Number of nodes
        continue
    if identifier =='NMARK=':           #boundary condition
        Nmark=int(l.split()[1])
        print ('There are',Nmark,'boundarys, they are:')
        
        Boundary_line=np.empty((Nmark),int) 
                                        #nmark is the number of kinds of BC
                                            
        j=0
        continue
    if identifier =='MARKER_TAG=':#marker_tag is the type of BC (sym far and W)
        print (j,'--------',l.split()[1])#j denotes the type of BC
                                         #when BC changes, j will +1
        Boundary_line[j]=i#the starting line Number is stored in Boundary_line
        j=j+1
        continue
    
X=np.empty(Npoin,float)#initializing the points by random value
Y=np.empty(Npoin,float)
Z=np.empty(Npoin,float)
#存储所有的坐标点
for i in range(Npoin):
    l=text[Point_line+1+i]
    X[i]=float(l.split()[0])
    Y[i]=float(l.split()[1])
    Z[i]=float(l.split()[2])
    
print ('which boundary is the WALL, please enter the number in 0 to',Nmark-1)


        
wall_number = int (input())

Wall_line=Boundary_line[ wall_number ]    #壁面边界开始行数
l=text[Wall_line+1]
Wall_elements=int(l.split()[1])         #wall_points,the number of wall points
                                        #which is equal to the number of lines

Boundary_point=np.zeros((Wall_elements,3),int)
                                              #initializing the array by
                                              #zero value. The function is the
                                              #the number of lines is wall_ele
                                              #the number of column is 3
                                              #integer type
for i in range (Wall_elements):
    l=text[Wall_line+2+i]
    identifier=int(l.split()[0])
    if identifier == 5:
        J=3
        #print ('三角形网格')
    if identifier == 9:                         # the block of codes is of no 
                                                # use which is not runed
        J=4
        #print('四边形网格')
    if identifier == 3:
        J=2
        #print('直线网格')
    for j in range(J):
        Boundary_point[i,j]=float(l.split()[1+j]) # N lines and 3 columns
        
x=np.empty((Wall_elements,J),float)
y=np.empty((Wall_elements,J),float)
z=np.empty((Wall_elements,J),float)

for i in range(Wall_elements):                    # store the data of points0
    for j in range(J):
        y[i,j]=X[Boundary_point[i,j]]
        x[i,j]=Y[Boundary_point[i,j]]
        z[i,j]=Z[Boundary_point[i,j]]

np.savez("Boundary.npz",x,y,z)
        
print ('ALL the data is sucessfully loaded\n next run MainUse.py to calculate the aerodynamic force')   

    
        

    

