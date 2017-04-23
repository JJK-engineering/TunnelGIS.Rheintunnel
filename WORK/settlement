# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:31:27 2017

@author: kzq653
"""
from numpy import *
import pandas as pd
import matplotlib.pyplot as plt


DF_all = pd.DataFrame()

tv_df = pd.read_csv('Ostroehre.TunnelExcavationData.R2.csv',index_col=0)
len_df = len(tv_df.index) - 1
for i in range(len_df):
    a=array([tv_df['Easting'][i], tv_df['Northing'][i], tv_df['Elevation'][i], tv_df['DTM'][i]]) #Punkt A mit Koordinaten x1=2,y1=3 --> i
    b=array([tv_df['Easting'][i+1], tv_df['Northing'][i+1], tv_df['Elevation'][i+1], tv_df['DTM'][i+1]])
    z_0=a[3]-a[2]
    #if z_0 < 0:
     #   continue
    #z_0=5
    ab=array([ b[0]-a[0],b[1]-a[1] ])
    n1=1.0
    n2=(ab[0]*n1) / (ab[1])
    n_length=(n1**2 + n2**2)**0.5
    n=array([n1,n2]) / n_length
    resolution=1.0
    x_dir=arange(-40,40,resolution)
    
    x_0=n[0]*x_dir
    
    x=a[0]+n[0]*x_dir
    y=a[1]+n[1]*x_dir
    
    i_n=array([x,y])     #Koordinaten der Gerade Normal zum Punkt A
    
    #Calculate Greenfield-Settlements
    #D_exc=13. #Ausbruchdurchmesser in [m]
    D_t=13.0    #Tunneldurchmesser in [m]
    K=0.6   #K nach Fillibeck, nichtbindiger Boden, dicht gelagert
    #z=15
    #z_0=z+D_t/2  # DTM - z Koordinate für Tunnel
    i_0=K*z_0
    #A_exc = ((D_exc**2.0) * pi) / 4.0
    A_t = ((D_t**2.0) * pi) / 4.0
    #V_l= (A_exc - A_t) / A_exc
    #V_l= 0.0064*(A_t/z_0)**(-0.75)  #nach Fillibeck,90%-Wahrscheinlichkeit, gilt für h/d>0.3
    V_l=0.01
    S= -((pi/2)**(0.5)) * (V_l*(D_t**2))/(4*i_0) *exp(-(x_dir**2)/(2*i_0**2))
    beta=zeros((len(S)))
    beta[1:]=diff(S)/resolution
    
    dc_beta=chararray((len(S)),itemsize=3)
    dc_beta[abs(beta)<1./500.] = 'DC1'
    dc_beta[(1./500.<abs(beta)) & (abs(beta)<1./250.)] = 'DC2'
    dc_beta[abs(beta)>1./250.] = 'DC3'
    
    dc_s=chararray((len(S)),itemsize=3)
    dc_s[abs(S*1000)<10] = 'DC1'
    dc_s[(10<abs(S*1000)) & (abs(S*1000)<30)] = 'DC2'
    dc_s[abs(S*1000)>30] = 'DC3'
    
    dc=chararray((len(S)),itemsize=3)
    dc[ (abs(beta)<1./500.) | (abs(S*1000)<10)] = 'DC1'
    dc[ ((1./500.<abs(beta)) & (abs(beta)<1./250.)) | ((10<abs(S*1000)) & (abs(S*1000)<30))] = 'DC2'
    dc[ (abs(beta)>1./250.) | (abs(S*1000)>30)] = 'DC3'
    
    D= {'A. Point Coordinates x':a [0],
        'B. Point Coordinates y':a [1],
        #'Point Coordinates z':z,
        #'DTM' : dtm,
        'z_0': z_0,
        'C. Normal Vector x': i_n[0],
        'D. Normal Vector y': i_n[1],
        'E. Settlement [mm]': S*1000,
        'F. Tangentenneigung': beta,
        'G. DC_Beta': dc_beta,
        'H. DC_Settlement': dc_s,
        'I. DamageClass' : dc}
    
    DF = pd.DataFrame(D)

    DF_all=DF_all.append(DF)
    
DF_all.to_csv('Settlement.csv')

'''
fig=plt.figure()
p1 = plt.plot(x_dir, S*1000, label='Greenfield-Settlement') 
#plt.xticks(y_pos+width, objects)
#plt.ylim((0,110))
plt.ylabel('Setzungen [mm]')
titleA=('Greenfield-Settlements')
plt.title(titleA)
plt.legend()
plt.show()
fig.savefig('C:\Users\kzq653\Documents\geopython\_' + str(titleA) +'.png', dpi=300)
'''

