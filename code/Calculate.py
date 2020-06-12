from math import *
import numpy as np
#采用牛顿修正理论计算压强系数
"""
@discription: 计算气动力系数
@author: YangDemin
"""

#定义气动参数计算函数，输入x，y，z的单位为m，alpha为角度制
def Calculate( x , y , z , alphad , Ma ):

    number = x.shape[0]                                                        #边界网格点数目
    alpha = (alphad) / 180.0 * pi                                              #将攻角从角度制化为弧度制
    gamma = 1.4                                                                #空气比热比
    
    
    #对一些参数进行初始化
    Normal_x = np.empty( number , float )                
    Normal_y = np.empty( number , float )
    Normal_z = np.empty( number , float )                                      #面元法向量
    theta = np.empty( number , float )                                         #来流与面元夹角
    cp = np.zeros( number , float )                                            #给予牛顿理论的压力系数
    cx = np.empty( number , float )                                            #轴向力系数
    cy = np.empty( number , float )                                            #法向力系数
    cz = np.empty( number , float )                                            #侧向力系数
    cl = np.empty( number , float )                                            #轴向力系数
    cm = np.empty( number , float )                                            #法向力系数
    cn = np.empty( number , float )
    s = np.empty( number , float )                                             #面元面积
    Coefficient = np.empty( 7 , float )                                        #气动参数矩阵
    
    
    #速度
    vx = sin( alpha )
    vy = cos( alpha )
    vz = 0.0                                                                   #将速度转化到箭体坐标系（单位化）
    
    #计算总体质心位置
    Xc = np.sum(x[:,0])
    Yc = np.sum(y[:,0])
    Zc = np.sum(z[:,0])
    #计算特征长度
    cA = np.max(x) - np.min(x)                  #纵向参考长度
    aA = np.max(y) - np.min(y)
    bA = np.max(z) - np.min(z)                  #横向参考长度
        
    #求解三角形面元的受力
    for i in range( 0 , number , 1 ):
        
        #计算面元质心位置
        xci = np.sum(x[i,:])
        yci = np.sum(y[i,:])
        zci = np.sum(z[i,:])
        deltax = Xc-xci
        deltay = Yc-yci
        deltaz = Zc-zci
        
        t1x = x[ i , 2 ] - x[ i , 0 ]
        t1y = y[ i , 2 ] - y[ i , 0 ]
        t1z = z[ i , 2 ] - z[ i , 0 ]                                          #矢量t1
        
        t2x = x[ i , 1 ] - x[ i , 0 ]
        t2y = y[ i , 1 ] - y[ i , 0 ]
        t2z = z[ i , 1 ] - z[ i , 0 ]                                          #矢量t2
        
        Nx = t1y * t2z - t1z * t2y
        Ny = t1z * t2x - t1x * t2z
        Nz = t1x * t2y - t1y * t2x                                             #面元法向量分解
        
        N = np.sqrt( Nx * Nx + Ny * Ny + Nz * Nz )
        s[i] = 0.5 * N                                                         #三角形面元面积
        Normal_x[i] = Nx / N
        Normal_y[i] = Ny / N
        Normal_z[i] = Nz / N                                                   #面元法向量单位化
        
        nx = Normal_x[i]
        ny = Normal_y[i]
        nz = Normal_z[i]                                                       #法向量存储

        theta[i] = pi / 2.0 - acos( -1.0 * ( nx * vx + ny * vy + nz * vz ) )   #来流与面元的夹角，弧度制

        if theta[i] > 0:                                                       #判断是否为头锥的迎风面
            cp0 = pow( ( gamma + 1 ) * Ma , 2 ) / ( 4 * gamma * pow( Ma , 2 ) - 2 * gamma + 2 )
            cp1 = ( 1 - gamma + 2 * gamma * pow( Ma , 2 ) ) / ( gamma + 1 )
            cp2 = pow( cp0 , ( gamma / ( gamma - 1 ) ) ) * cp1 - 1
            cp[i] = 2.0 / gamma / pow( Ma , 2 ) * cp2 * pow( sin( theta[i] ) , 2 ) 

        cx[i] = cp[i] * Normal_x[i] * s[i]
        cy[i] = cp[i] * Normal_y[i] * s[i]
        cz[i] = -cp[i] * Normal_z[i] * s[i]                                    #三角面元受力分解
        
        #计算力矩系数
        cl[i] = (-cy[i] * deltaz + cz[i] * deltay) / bA
        cm[i] = ( cx[i] * deltaz - cz[i] * deltax) / cA
        cn[i] = (-cx[i] * deltay + cy[i] * deltax) / bA
    #飞船总面积
    S_sum = np.sum(s)
    #求解飞船受力
    Axial_force     = np.sum( cx )                                             #轴向力
    Side_force      = np.sum( cy )                                             #法向力
    Normal_force    = np.sum( cz )                                             #侧向力
    Cl = np.sum(cl)
    Cm = np.sum(cm)
    Cn = np.sum(cn)
    #从箭体坐标系转换为速度坐标系
    Drag        = -(-1.0 * Axial_force * np.sin(alpha) + Side_force * cos(alpha))  #阻力
    Lift        = -(Axial_force * cos( alpha ) + Side_force * sin( alpha ))       #升力
    LD_ratio    = Lift / Drag                                                  #升阻比
    
    Coefficient = [ Lift , Drag , LD_ratio, Cl, Cm, Cn, S_sum]                 #升力、阻力、轴向力、法向力、
                                                                               # 升阻比 滚转偏航俯仰力矩系数
    return Coefficient
           
    
