#主函数
"""
@discription: 主程序
@author: YangDemin
"""
import numpy as np
import math
import Calculate
#import Su2_Read
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False


#设置头锥初始参数
number = 20                                                  #设置绘图坐标点个数
alpha = np.linspace( -5 , 35 , number )                      #攻角范围
Ma = 10                                                      #来流马赫数


#计算气动参数
r=np.load('Boundary.npz')
x=r["arr_0"]
y=r["arr_1"]
z=r["arr_2"]
#x , y , z = Su2_Read.Su2_Read ( r'../mesh/SOYUZ.su2' )      #调用网格读取函数
#气动参数初始化
result  = np.empty( 7 , float ) 
C_lift  = np.empty( number , np.float )
C_drag  = np.empty( number , np.float )
LD      = np.empty( number , np.float ) 
Cl      = np.empty( number , np.float )
Cm      = np.empty( number , np.float )
Cn      = np.empty( number , np.float )
S_sum   = np.empty( number , np.float )
                                                                               
print('网格边界：','\n',np.min(y),np.max(y), '\n',np.min(x), np.max(x),'\n',
          np.min(z),np.max(z))

for i in range( 0 , number , 1 ):
    
    result = Calculate.Calculate( x , y , z , alpha[i] , Ma )
    
    S_sum[i]    = result[6]                     #参考面积
    C_lift[i]   = result[0] / S_sum[i]          #升力系数
    C_drag[i]   = result[1] / S_sum[i]          #阻力系数
    LD[i]       = result[2]                     #升阻比
    Cl[i]       = result[3] / S_sum[i]          #滚转力矩系数
    Cm[i]       = result[4] / S_sum[i]          #偏航力矩系数
    Cn[i]       = result[5] / S_sum[i]          #俯仰力矩系数
    
   
#绘图函数
plt.figure(10)
plt.plot( alpha, C_lift,'bo',alpha,C_lift,'k')
plt.xlabel('攻角/度')
plt.ylabel('升力系数')
plt.title('升力系数曲线')
plt.grid(True)
plt.show
plt.savefig('../jpg/升力系数曲线.jpg',dpi=1080)

plt.figure(20)
plt.plot(alpha, C_drag,'bo',alpha,C_drag,'k')
plt.xlabel('攻角/度')
plt.ylabel('阻力系数')
plt.title('阻力系数曲线')
plt.grid(True)
plt.show
plt.savefig('../jpg/阻力系数曲线.jpg',dpi=1080)

plt.figure(30)
plt.plot(alpha, LD,'bo',alpha,LD,'k')
plt.xlabel('攻角/度')
plt.ylabel('升阻比')
plt.title('升阻比曲线')
plt.grid(True)
plt.show
plt.savefig('../jpg/升阻比曲线.jpg',dpi=1080)

plt.figure(40)
plt.plot(alpha, Cl,'bo',alpha,Cl,'k')
plt.xlabel('攻角/度')
plt.ylabel('滚转力矩系数')
plt.title('滚转力矩系数曲线')
plt.grid(True)
plt.show
plt.savefig('../jpg/滚转力矩系数曲线.jpg',dpi=1080)

plt.figure(50)
plt.plot(alpha, Cm,'bo',alpha,Cm,'k')
plt.xlabel('攻角/度')
plt.ylabel('偏航力矩系数')
plt.title('偏航力矩系数曲线')
plt.grid(True)
plt.show
plt.savefig('../jpg/偏航力矩系数曲线.jpg',dpi=1080)

plt.figure(60)
plt.plot(alpha, Cn,'bo',alpha,Cn,'k')
plt.xlabel('攻角/度')
plt.ylabel('俯仰力矩系数')
plt.title('俯仰力矩系数曲线')
plt.grid(True)
plt.show
plt.savefig('../jpg/俯仰力矩系数曲线.jpg',dpi=1080)

plt.figure(70)
plt.plot(alpha, S_sum,'bo',alpha,S_sum,'k')
plt.xlabel('攻角/度')
plt.ylabel('总面积')
plt.title('总面积')
plt.grid(True)
plt.show
plt.savefig('../jpg/总面积.jpg',dpi=1080)


fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')
 
ax.scatter(x[:,0], y[:,0], z[:,0],
   marker='x', color='blue', s=40, label='class 1')
ax.scatter(x[:,1], y[:,1], z[:,1],
   marker='x', color='blue', s=40, label='class 1')
ax.scatter(x[:,2], y[:,2], z[:,2],
   marker='x', color='blue', s=40, label='class 1')

ax.set_xlabel('variable X')
ax.set_ylabel('variable Y')
ax.set_zlabel('variable Z')
print("!!! Plot Succeed !!!")