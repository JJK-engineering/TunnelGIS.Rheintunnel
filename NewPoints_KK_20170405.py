import pandas as pd
import re
import numpy as np

pd.set_option("display.max_columns",7)

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

Alignment_df["ID"] = range(0,len(Alignment_df.index))
Alignment_df["Station_int"] = np.nan
for n in range(0, len(station_list)):
    print n
    station_sel = Alignment_df.iloc[n]["Station"]
    station_sel_int = float(station_sel.replace("+", ""))
    Alignment_df.loc[n == Alignment_df["ID"],'Station_int'] = station_sel_int    
    #Alignment_df.iloc[n]['Station_int'] = station_sel_int
    #Alignment_df.loc[n, 'Station_int'] = int(''.join(re.findall(r'\d+', station_sel)))

Alignment_df
#Alignment_df["Station_int"].tolist()
#len(Alignment_df["Station_int"].tolist())

n =  209508
if n in Alignment_df["Station_int"].tolist() == True:
    print "exit"
else:
    ID_sel = int(Alignment_df.loc[n == Alignment_df["Station_int"],'ID'])
    neighbour1 = Alignment_df.loc[ID_sel-1 == Alignment_df["ID"],]
    neighbour2 = Alignment_df.loc[ID_sel+1 == Alignment_df["ID"],]
