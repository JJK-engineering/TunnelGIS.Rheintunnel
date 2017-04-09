import pandas as pd
import re
import numpy as np
import os 


os.chdir("/home/kaelin_joseph/")

#pd.set_option("display.max_columns",7)

Alignment_csv = "TunnelGIS.Rheintunnel/WORK/OstrohrR2.csv"
Alignment_df = pd.read_csv(Alignment_csv)
# Alignment_df.shape
Alignment_df = Alignment_df.dropna(how = "all")  #delete row if only NA are present in row
#Alignment_df.shape
Alignment_df = Alignment_df.drop(Alignment_df.index[len(Alignment_df)-1])  #delete trailing blank line
Alignment_df = Alignment_df.loc[:,["Station","Easting", "Northing", "Elevation"]]
#Alignment_df.shape
len(Alignment_df.index)

station_list = Alignment_df["Station"].tolist()
station_list
len(station_list)

#Alignment_df["ID"] = range(0,len(Alignment_df.index))
#Alignment_df["ID"].head()


Alignment_df["Station_int"] = np.nan

for n in range(0, len(station_list)):
    print n
    station_sel = Alignment_df.iloc[n]["Station"]
    station_sel_int = float(station_sel.replace("+", ""))
    #Alignment_df.loc[n == Alignment_df["ID"],'Station_int'] = station_sel_int    
    Alignment_df.iloc[n, Alignment_df.columns.get_loc("Station_int")] = station_sel_int # Alignment_df.columns.get_loc("Station_int") = 5
    #Alignment_df.loc[n, 'Station_int'] = int(''.join(re.findall(r'\d+', station_sel)))



#Alignment_df["Station_int"].tolist()
#len(Alignment_df["Station_int"].tolist())

n = 209510 # value does not exist in Alignment # value lies between 209508 abd 209511
#n = 209526 # value exists in Alignment

vicinity = 0.1

station_int_list = Alignment_df["Station_int"].tolist()

if n in station_int_list:
    print "exit"
else:
    print "smile"
    neighbour1_station_int = max([i for i in station_int_list if i < n]) 
    neighbour2_station_int = min([i for i in station_int_list if i > n])       
    if n < neighbour1_station_int + vicinity OR n > neighbour2_station_int + vicinity
         print "exit"
    
    else:
    
    neighbour1 = Alignment_df.loc[Alignment_df["Station_int"] == neighbour1_station_int,]
    neighbour2 = Alignment_df.loc[Alignment_df["Station_int"] == neighbour2_station_int,]

    