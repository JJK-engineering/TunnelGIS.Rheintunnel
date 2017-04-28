# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:31:27 2017

@author: kzq653
"""
from numpy import *
import pandas as pd
import matplotlib.pyplot as plt

#create Dataframe for all settlement-results, which will be calculated 

DF_all = pd.DataFrame()

# import the DataFrame with calculated Results from GIS
tv_df = pd.read_csv('Ostroehre.TunnelExcavationData.R2.csv',index_col=0)

# create loop to do the calculations for all tunnel-points
len_df = len(tv_df.index) - 1   #how many points are there -> length of loop
for i in range(len_df): #start loop
    a=array([tv_df['Easting'][i], tv_df['Northing'][i], tv_df['Elevation'][i], tv_df['DTM'][i], tv_df['RockCover'][i]] ) # read in the values which are needed for calculation of point i
    b=array([tv_df['Easting'][i+1], tv_df['Northing'][i+1], tv_df['Elevation'][i+1], tv_df['DTM'][i+1], tv_df['RockCover'][i+1]] ) # read in the values which are needed for calculation of point i+1
    z_0=a[3]-a[2]   #overburden in [m]
    if z_0 < 0: #if the overburden is < 1, stop calculation (then the tunnel is not a tunnel)
        continue
    #calculate normalvector for settlement
    ab=array([ a[1]-a[0],b[1]-b[0] ])   #vector between point i and i+1
    n1=1.0  
    n2=(ab[0]*n1) / (ab[1])
    n_length=(n1**2 + n2**2)**0.5   #calculate length of normalvector
    n=array([n1,n2]) / n_length     #normalvector with length 1.0
    resolution=1.0
    x_dir=arange(-40,40,resolution) #direction for vector for calculating settlements 
    
    x_0=n[0]*x_dir   #vector for calculating settlements 
    
    x=a[0]+n[0]*x_dir   #x-coordinates of vector  
    y=a[1]+n[1]*x_dir   #y-coordinates of vector 
    
    i_n=array([x,y])     #x- and y- coordinates of vector 
    
    #Calculate Greenfield-Settlements
    D_t=13.0    #Tunneldiameter in [m]
    K=0.6   #K (nach Fillibeck für nichtbindigen Boden, dicht gelagert)
    i_0=K*z_0   #Wendepunktabstand
    A_t = ((D_t**2.0) * pi) / 4.0
    #V_l= 0.0064*(A_t/z_0)**(-0.75)  #nach Fillibeck,90%-Wahrscheinlichkeit, gilt für h/d>0.3

    if a[4] > 3.0 :
        V_l = 0.0005 #assumed volume loss in rock with rock overburden < 8.0 m
    elif a[4] > 8.0 :
        V_l =0.0 #assumed volume loss in rock with rock overburden > 8.0 m
    else:
        V_l=0.005  #assumed volume loss in gravel 0.5 %
        
    S= -((pi/2)**(0.5)) * (V_l*(D_t**2))/(4*i_0) *exp(-(x_dir**2)/(2*i_0**2))   #calculate Settlement trough with gaussi curve
    beta=zeros((len(S)))    #creates vector for tangentenneigung
    beta[1:]=diff(S)/resolution  #tangentenneigung der setzungen
    
    #classify beta into different damage classes
    dc_beta=chararray((len(S)),itemsize=3)
    dc_beta[abs(beta)<1./500.] = 'DC1'
    dc_beta[(1./500.<abs(beta)) & (abs(beta)<1./250.)] = 'DC2'
    dc_beta[abs(beta)>1./250.] = 'DC3'
    
    #classify settlements into different damage classes
    dc_s=chararray((len(S)),itemsize=3)
    dc_s[abs(S*1000)<10] = 'DC1'
    dc_s[(10<abs(S*1000)) & (abs(S*1000)<30)] = 'DC2'
    dc_s[abs(S*1000)>30] = 'DC3'
    
    #classify settlements and beta into different damage classes
    dc=chararray((len(S)),itemsize=3)
    dc[ (abs(beta)<1./500.) | (abs(S*1000)<10)] = 'DC1'
    dc[ ((1./500.<abs(beta)) & (abs(beta)<1./250.)) | ((10<abs(S*1000)) & (abs(S*1000)<30))] = 'DC2'
    dc[ (abs(beta)>1./250.) | (abs(S*1000)>30)] = 'DC3'
    
    #create dataframe including the calculated settlements etc. 
    D= {'A. Point Coordinates x':a [0],
        'B. Point Coordinates y':a [1],
        'C. Normal Vector x': i_n[0],
        'D. Normal Vector y': i_n[1],
        'E. Settlement [mm]': S*1000,
        'F. Tangentenneigung': beta,
        'G. DC_Beta': dc_beta,
        'H. DC_Settlement': dc_s,
        'I. DamageClass' : dc,
        'J. z_0': z_0,}
    
    DF = pd.DataFrame(D)

    #append the calculated values to the dataframe
    DF_all=DF_all.append(DF)
    
    #when loop is finished, safe dataframe to .csv
DF_all.to_csv('Settlement.csv')


