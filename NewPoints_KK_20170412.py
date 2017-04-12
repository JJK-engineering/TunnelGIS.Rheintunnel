import pandas as pd
import numpy as np
import os 


os.chdir("/home/kaelin_joseph/")

# import TunnelLayoutData
TunnelLayoutData = "TunnelGIS.Rheintunnel/WORK/Ostroehre.TunnelLayoutData.R2.csv"
TunnelLayoutData_df = pd.read_csv(TunnelLayoutData)

# import Alignment_csv
Alignment_csv = "TunnelGIS.Rheintunnel/WORK/Ostroehre.AlignmentData.R2.csv"
Alignment_df = pd.read_csv(Alignment_csv)
Alignment_df = Alignment_df.dropna(how = "all")  #delete row if only NA are present in row
Alignment_df = Alignment_df.drop(Alignment_df.index[len(Alignment_df)-1])  #delete trailing blank line
Alignment_df = Alignment_df.loc[:,["Station","Easting", "Northing", "Elevation"]]
len(Alignment_df.index)

#------------------------

# Alignment_df["Station"] => Alignment_df["Alignment_Station_int"] 
Alignment_Station_list = Alignment_df["Station"].tolist()
Alignment_Station_list
len(Alignment_Station_list)

Alignment_df["Alignment_Station_int"] = np.nan

for n in range(0, len(Alignment_Station_list)):
    print n
    station_sel = Alignment_df.iloc[n]["Station"]
    station_sel_int = float(station_sel.replace("+", ""))
    Alignment_df.iloc[n, Alignment_df.columns.get_loc("Alignment_Station_int")] = station_sel_int # Alignment_df.columns.get_loc("Alignment_Station_int") = 5

# TunnelLayoutData_df["Station"] => TunnelLayoutData_df["TunnelLayoutData_Station_int"] 
TunnelLayoutData_Station_list = TunnelLayoutData_df["Station"].tolist()
TunnelLayoutData_Station_list
len(TunnelLayoutData_Station_list)
TunnelLayoutData_df["TunnelLayoutData_Station_int"] = np.nan

for n in range(0, len(TunnelLayoutData_Station_list)):
    print n
    station_sel = TunnelLayoutData_df.iloc[n]["Station"]
    station_sel_int = float(station_sel.replace("+", ""))
    TunnelLayoutData_df.iloc[n, TunnelLayoutData_df.columns.get_loc("TunnelLayoutData_Station_int")] = station_sel_int # Alignment_df.columns.get_loc("Alignment_Station_int") = 5

# Check if TunnelLayoutData_df["TunnelLayoutData_Station_int"]  exists in  Alignment_df["Alignment_Station_int"] 
# If it does not exist create a new station in Alignment_df

TunnelLayoutData_Station_int_list = TunnelLayoutData_df["TunnelLayoutData_Station_int"].tolist()
Alignment_Station_int_list = Alignment_df["Alignment_Station_int"].tolist()

# within this vicinity of a station no new station will be created
vicinity = 0.1

# new variables
Easting_NewPoint = []
Northing_NewPoint = []
Elevation_NewPoint = []
Station = []
Station_int = []

for n in TunnelLayoutData_Station_int_list:
    if n in Alignment_Station_int_list:
        print "exit1"
    else:
        print "smile"
        neighbour1_Alignment_Station_int = max([i for i in Alignment_Station_int_list if i < n]) 
        neighbour2_Alignment_Station_int = min([i for i in Alignment_Station_int_list if i > n])       
        if n < neighbour1_Alignment_Station_int + vicinity or n > neighbour2_Alignment_Station_int + vicinity:
            print "exit2"    
        else: 
            print "smile2"
            neighbour1 = Alignment_df.loc[Alignment_df["Alignment_Station_int"] == neighbour1_Alignment_Station_int,]
            neighbour2 = Alignment_df.loc[Alignment_df["Alignment_Station_int"] == neighbour2_Alignment_Station_int,]
            delta_x_neighbour1and2 = abs(neighbour2.Easting.tolist()[0]-neighbour1.Easting.tolist()[0]) # delta x
            delta_y_neighbour1and2 = abs(neighbour2.Northing.tolist()[0]-neighbour1.Northing.tolist()[0]) # delta y
            length_neighbour1and2 = (delta_x_neighbour1and2**2 +delta_y_neighbour1and2**2)**(0.5) # L
            length_neighbour1andNewPoint = n-neighbour1.Alignment_Station_int.tolist()[0]
            Easting_NewPoint_sel = neighbour2.Easting.tolist()[0] + ((delta_y_neighbour1and2*length_neighbour1andNewPoint)/length_neighbour1and2)
            Northing_NewPoint_sel = neighbour2.Northing.tolist()[0] + ((delta_x_neighbour1and2*length_neighbour1andNewPoint)/length_neighbour1and2)
            Elevation_NewPoint_sel = neighbour2.Elevation.tolist()[0] + ((delta_x_neighbour1and2*length_neighbour1andNewPoint)/length_neighbour1and2)
            Easting_NewPoint.append(Easting_NewPoint_sel)
            Northing_NewPoint.append(Northing_NewPoint_sel)
            Elevation_NewPoint.append(Elevation_NewPoint_sel)
            Station_int.append(n)
            Station_sel = TunnelLayoutData_df.loc[TunnelLayoutData_df['TunnelLayoutData_Station_int'] == n, 'Station'] 
            Station.append(Station_sel.tolist()[0])
            

NewStation_df = pd.DataFrame({"Easting": Easting_NewPoint, "Northing": Northing_NewPoint, "Elevation": Elevation_NewPoint, "Alignment_Station_int": Station_int, "Station": Station})

frames = [Alignment_df, NewStation_df]
result = pd.concat(frames)
result.tail()





