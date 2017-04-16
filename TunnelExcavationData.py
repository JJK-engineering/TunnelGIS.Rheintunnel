# ----------------------------------------------------------------------------------------------------------------
# description
# ----------------------------------------------------------------------------------------------------------------

#!/usr/bin/python
# TunnelExcavationData.py

# Python procedure for TunnelGIS Engineering App
# Author: KK
# Date: 01.04.2017

# Aims of this procedure:
# 1. Prepare input data ....
# 2.
# 3.
# 4. 
# 5. 

# This python routine is a script, intended to guide the user through the described procedure.
# As a script, the procedure does not generally include data validation and error handling.
# Users are expected to understand and adjust the code as needed for their application.

# Required Input Files:
# "WORK/swissalti3dgeotifflv03-5m/swissALTI3D_.tif"   -DEM with surface topography
# "WORK/Felsisohypsen-raster.tif"                     -DEM with rock surfac
# "WORK/OstrohrR2.csv"                                -stationed tunnel alignment#
# "WORK/Ostroehre.TunnelLayoutData.R2.csv"            -tunnel layout data

# References:
# http://gis.stackexchange.com/questions/197825/how-to-convert-multiple-csv-files-to-shp-using-python-and-no-arcpy
# to get grass help:   processing.alghelp("grass7:r.what.points")

# IMPORTANT: requires qgis setup before running this procedure
# run ./pyqgis.sh from command line before starting python (or set up IDE accordingly)


# ----------------------------------------------------------------------------------------------------------------
# import required libraries
# ----------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import geopandas as gpd
import shapely as sp
import os 


# ----------------------------------------------------------------------------------------------------------------
# set wd for this procedure 
# ----------------------------------------------------------------------------------------------------------------
os.chdir("/home/kaelin_joseph/TunnelGIS.Rheintunnel/")


# ----------------------------------------------------------------------------------------------------------------
# define input files
# ----------------------------------------------------------------------------------------------------------------

DTM = "WORK/swissalti3dgeotifflv03-5m/swissALTI3D_.tif"
Bedrock_surface = "WORK/Felsisohypsen-raster.tif"
Alignment_csv = "WORK/Ostroehre.AlignmentData.R2.csv"
TunnelLayoutData = "WORK/Ostroehre.TunnelLayoutData.R2.csv"


# ----------------------------------------------------------------------------------------------------------------
# define output files
# ----------------------------------------------------------------------------------------------------------------

Alignment_shp ='WORK/Ostrohr.Alignment.R2.shp'
Alignment_DTM = "WORK/Ostrohr.DTM.R2.csv"
Alignment_Bedrock_surface = "WORK/Ostrohr.Bedrock_surface.R2.csv"  # JK ToDo: Bedrock_surface?
Alignment_Tunnel_variables = "WORK/Ostroehre.TunnelExcavationData.R2.csv"  # JK ToDo: cleanup 
TunnelExcavationData = "WORK/Ostroehre.TunnelExcavationData.R2.csv"


# ----------------------------------------------------------------------------------------------------------------
# create Alignment_df from .csv (dataframe)
# Important: Before the df is created the data should be checked.
#   E.g. make sure that it does not contain trailing blank lines and that duplicates are deleted.
# result: Alignment_df
# ----------------------------------------------------------------------------------------------------------------

Alignment_df = pd.read_csv(Alignment_csv)
Alignment_df = Alignment_df.dropna(how = "all")  #delete row if only NA are present in row


# ----------------------------------------------------------------------------------------------------------------
# create TunnelLayoutData_df from .csv
# result: TunnelLayoutData_df
# ----------------------------------------------------------------------------------------------------------------

TunnelLayoutData_df = pd.read_csv(TunnelLayoutData)


# ----------------------------------------------------------------------------------------------------------------
# convert Alignment_df["Station"] => Alignment_df["Alignment_Station_real"] 
# result: Alignment_df["Alignment_Station_real"], TunnelLayoutData_Station_list,
#         TunnelLayoutData_df["TunnelLayoutData_Station_real"]
print "df Alignment_Station_real"
# ----------------------------------------------------------------------------------------------------------------

Alignment_Station_list = Alignment_df["Station"].tolist()
    # check: len(Alignment_Station_list)

Alignment_df["Alignment_Station_real"] = np.nan

for n in range(0, len(Alignment_Station_list)):
    station_sel = Alignment_df.iloc[n]["Station"]
    station_sel_int = float(station_sel.replace("+", ""))
    Alignment_df.iloc[n, Alignment_df.columns.get_loc("Alignment_Station_real")] = station_sel_int
    # Alignment_df.columns.get_loc("Alignment_Station_real") = 5

# TunnelLayoutData_df["Station"] => TunnelLayoutData_df["TunnelLayoutData_Station_real"] 
TunnelLayoutData_Station_list = TunnelLayoutData_df["Station"].tolist()
# check: len(TunnelLayoutData_Station_list)

TunnelLayoutData_df["TunnelLayoutData_Station_real"] = np.nan

for n in range(0, len(TunnelLayoutData_Station_list)):
    station_sel = TunnelLayoutData_df.iloc[n]["Station"]
    station_sel_int = float(station_sel.replace("+", ""))
    TunnelLayoutData_df.iloc[n, TunnelLayoutData_df.columns.get_loc("TunnelLayoutData_Station_real")] \
        = station_sel_int
    # Alignment_df.columns.get_loc("Alignment_Station_real") = 5


# ----------------------------------------------------------------------------------------------------------------
# check if TunnelLayoutData_df["TunnelLayoutData_Station_real"] exists in Alignment_df["Alignment_Station_real"]
#   If it does not exist create a new Station in Alignment_df
# result: Alignment_df with added Stations
print "adding Stations"
# ----------------------------------------------------------------------------------------------------------------

# list stations in Alignment_df and TunnelLayoutData_df
# result: Alignment_Station_real_list and TunnelLayoutData_Station_real_list
Alignment_Station_real_list = Alignment_df["Alignment_Station_real"].tolist()
TunnelLayoutData_Station_real_list = TunnelLayoutData_df["TunnelLayoutData_Station_real"].tolist()

# within this vicinity of a station no new station will be created
vicinity = 0.1

# define new variables
Easting_NewPoint = []
Northing_NewPoint = []
Elevation_NewPoint = []
Station = []
Station_real = []

# Loop through stations
for n in TunnelLayoutData_Station_real_list:
    if n in Alignment_Station_real_list:
        pass
    else:
        neighbour1_Alignment_Station_real = max([i for i in Alignment_Station_real_list if i < n]) 
        neighbour2_Alignment_Station_real = min([i for i in Alignment_Station_real_list if i > n])       
        if n < neighbour1_Alignment_Station_real + vicinity or n > neighbour2_Alignment_Station_real + vicinity:
            pass
        else: 
            neighbour1 = Alignment_df.loc[Alignment_df["Alignment_Station_real"]
                                          == neighbour1_Alignment_Station_real,]
            neighbour2 = Alignment_df.loc[Alignment_df["Alignment_Station_real"]
                                          == neighbour2_Alignment_Station_real,]
            delta_x_neighbour1and2 = abs(neighbour2.Easting.tolist()[0]-neighbour1.Easting.tolist()[0]) #delta x
            delta_y_neighbour1and2 = abs(neighbour2.Northing.tolist()[0]-neighbour1.Northing.tolist()[0]) #delta y
            length_neighbour1and2 = (delta_x_neighbour1and2**2 +delta_y_neighbour1and2**2)**(0.5) # L
            length_neighbour1andNewPoint = n-neighbour1.Alignment_Station_real.tolist()[0]
            Easting_NewPoint_sel = neighbour2.Easting.tolist()[0] \
                                 + ((delta_y_neighbour1and2*length_neighbour1andNewPoint)/length_neighbour1and2)
            Northing_NewPoint_sel = neighbour2.Northing.tolist()[0] \
                                  + ((delta_x_neighbour1and2*length_neighbour1andNewPoint)/length_neighbour1and2)
            Elevation_NewPoint_sel = neighbour2.Elevation.tolist()[0] \
                                   + ((delta_x_neighbour1and2*length_neighbour1andNewPoint)/length_neighbour1and2)
            Easting_NewPoint.append(Easting_NewPoint_sel)
            Northing_NewPoint.append(Northing_NewPoint_sel)
            Elevation_NewPoint.append(Elevation_NewPoint_sel)
            Station_real.append(n)
            Station_sel = TunnelLayoutData_df.loc[TunnelLayoutData_df['TunnelLayoutData_Station_real']
                                                  == n, 'Station'] 
            Station.append(Station_sel.tolist()[0])
           
NewStation_df = pd.DataFrame({"Easting": Easting_NewPoint, "Northing": Northing_NewPoint,
                              "Elevation": Elevation_NewPoint, "Alignment_Station_real": Station_real,
                              "Station": Station})
    # check len(Alignment_df)
    # check len(NewStation_df)

# Contatenate Alignment_df with NewStation_df
# result: Alignment_df
frames = [Alignment_df, NewStation_df]
Alignment_df = pd.concat(frames)
    # check: len(Alignment_df)
    # check: Alignment_df.tail()

    
# ----------------------------------------------------------------------------------------------------------------
# create Alignment_spatial from Alignment_df
# result: Alignment_shp
# ----------------------------------------------------------------------------------------------------------------

Alignment_spatial_points = [sp.geometry.Point(row['Easting'], row['Northing'])
                            for key, row in Alignment_df.iterrows()]
Alignment_crs = {'init': 'epsg:2056'}  #define crs
Alignment_spatial = gpd.GeoDataFrame(Alignment_df, geometry=Alignment_spatial_points, crs = Alignment_crs)
Alignment_spatial.to_file(Alignment_shp, driver='ESRI Shapefile') 


# ----------------------------------------------------------------------------------------------------------------
# use grass functions to get raster values for points along tunnel axis and write to .csv files
# result: Alignment_DTM, Alignment_Bedrock_surface
print "get raster values"
# ----------------------------------------------------------------------------------------------------------------

# Alignment_DTM
processing.runalg("grass7:r.what.points",DTM,Alignment_shp,
                  "NA",",",500,True,False,False,False,False,
                  "2603510.0,2624270.0,1260650.0,1274890.0",-1,0.0001,Alignment_DTM)
# Alignment_Bedrock_surface                  
processing.runalg("grass7:r.what.points",Bedrock_surface,Alignment_shp,
                  "NA",",",500, True,False,False,False,False,
                  "2603510.0,2624270.0,1260650.0,1274890.0",-1,0.0001,Alignment_Bedrock_surface)
## warning: Not all input layers use the same CRS -> data seems OK
    # check:  Alginemnt_spatial.crs


# ----------------------------------------------------------------------------------------------------------------
# create df's
# result: Alignment_DTM_df, Alignment_Bedrock_surface_df
# ----------------------------------------------------------------------------------------------------------------
Alignment_DTM_df  = pd.read_csv(Alignment_DTM)
Alignment_Bedrock_surface_df  = pd.read_csv(Alignment_Bedrock_surface)


# ----------------------------------------------------------------------------------------------------------------
# prepare for join of grass results using pandas
# result: Alignment_df, Alignment_DTM_df_sel, Alignment_Bedrock_surface_df_sel
# ----------------------------------------------------------------------------------------------------------------

# prepare Alignment_df
    # check:  Alignment_df.head()
Alignment_df = Alignment_df.loc[:,["Station","Easting", "Northing", "Elevation", "Alignment_Station_real"]]
    # check:  Alignment_df.head()

# prepare Alignment_DTM_df_sel
    # check:  Alignment_DTM_df.head()
Alignment_DTM_df_coleqtmp = [col for col in Alignment_DTM_df.columns if 'tmp' in col]
if len(Alignment_DTM_df_coleqtmp) != 1:
    print "Extraction of DTM col=tmp did not work properly. Please check"
    exit()
Alignment_DTM_df_rename = Alignment_DTM_df.rename(
    columns= {Alignment_DTM_df_coleqtmp[0]: "DTM"})
Alignment_DTM_df_sel = Alignment_DTM_df_rename.loc[:,["easting", "northing", "DTM"]]
    # check:  Alignment_Bedrock_surface_df.head()

# prepare Alignment_Bedrock_surface_df_coleqtmp
Alignment_Bedrock_surface_df_coleqtmp = [col for col in Alignment_Bedrock_surface_df.columns if 'tmp' in col]
if len(Alignment_Bedrock_surface_df_coleqtmp) != 1:
    print "Extraction of Bedrock_surface_csv_coleqtmp col=tmp did not work properly. Please check"
    exit()
Alignment_Bedrock_surface_df_rename = Alignment_Bedrock_surface_df.rename(
    columns= {Alignment_Bedrock_surface_df_coleqtmp[0]: "Rocksurface"})
Alignment_Bedrock_surface_df_sel = Alignment_Bedrock_surface_df_rename.loc[
    :,["easting", "northing", "Rocksurface"]]  
    # check:  Alignment_Bedrock_surface_df_sel.head()


# ----------------------------------------------------------------------------------------------------------------
# join grass results using Panda
#    merge handles floats as keys inconsistently, truncate df's to three decimals before merge 
# result: merge_final
print 'merge_final'
# ----------------------------------------------------------------------------------------------------------------

Alignment_df = Alignment_df.round(decimals=3)
Alignment_DTM_df_sel = Alignment_DTM_df_sel.round(decimals=3)
Alignment_Bedrock_surface_df_sel = Alignment_Bedrock_surface_df_sel.round(decimals=3)

# merge DTM to Alignment
merge_Alignment_DTM= pd.merge(left= Alignment_df, right = Alignment_DTM_df_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"], how = "left")

# merge Rocksurface to Alignment_DTM
merge_final = pd.merge(merge_Alignment_DTM, Alignment_Bedrock_surface_df_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"])
    # check:  merge_final.head()
    # check:  merge_final.columns

    
# ----------------------------------------------------------------------------------------------------------------
# clean up merge_final
# result: merge_sel
print 'cleaning up merge'
# ----------------------------------------------------------------------------------------------------------------

merge_sel = merge_final.loc[:,["Station","Easting", "Northing", "Elevation", "DTM", "Rocksurface",
                               "Alignment_Station_real"]]
    # check:  merge_sel.head()
    # check:  list(merge_sel)
# sort by Station
merge_sel = merge_sel.sort(['Alignment_Station_real'], ascending=[1])

    
# ----------------------------------------------------------------------------------------------------------------
# calculate "delta_rocksurface_tunnelaxis"
# result: merge_sel['delta_rocksurface_tunnelaxis']
# ----------------------------------------------------------------------------------------------------------------

merge_sel['delta_rocksurface_tunnelaxis'] = merge_sel.Rocksurface - merge_sel.Elevation


# ----------------------------------------------------------------------------------------------------------------
# assign WBS, WorkType, Excavation Type, Profile Type, Section Area from TunnelLayoutDarta
# result: merge_sel["WBScode"], merge_sel["WorkType"], merge_sel["ExcavationType"], merge_sel["ProfileType"]
#         merge_sel["SectionArea"], merge_sel["Description"]
print "working on WBS etc"
# ----------------------------------------------------------------------------------------------------------------

merge_sel["WBScode"] = np.nan
merge_sel["WorkType"] = np.nan
merge_sel["ExcavationType"] = np.nan
merge_sel["ProfileType"] = np.nan
merge_sel["SectionArea"] = np.nan
merge_sel["Description"] = np.nan

for n in range(0, len(TunnelLayoutData_Station_real_list)):
    nn = n+1 
    if n == len(TunnelLayoutData_Station_real_list) -1:
        TunnelLayoutData_Station_real_list.append(1e12)
    merge_sel.loc[(merge_sel["Alignment_Station_real"] >= TunnelLayoutData_Station_real_list[n])
        & (merge_sel["Alignment_Station_real"] < TunnelLayoutData_Station_real_list[nn]), "WBScode"] \
        = TunnelLayoutData_df["WBScode"].tolist()[n]
    merge_sel.loc[(merge_sel["Alignment_Station_real"] >= TunnelLayoutData_Station_real_list[n])
        & (merge_sel["Alignment_Station_real"] < TunnelLayoutData_Station_real_list[nn]), "WorkType"] \
        = TunnelLayoutData_df["WorkType"].tolist()[n]
    merge_sel.loc[(merge_sel["Alignment_Station_real"] >= TunnelLayoutData_Station_real_list[n])
        & (merge_sel["Alignment_Station_real"] < TunnelLayoutData_Station_real_list[nn]), "ExcavationType"] \
        = TunnelLayoutData_df["ExcavationType"].tolist()[n]
    merge_sel.loc[(merge_sel["Alignment_Station_real"] >= TunnelLayoutData_Station_real_list[n])
        & (merge_sel["Alignment_Station_real"] < TunnelLayoutData_Station_real_list[nn]), "ProfileType"] \
        = TunnelLayoutData_df["ProfileType"].tolist()[n]
    merge_sel.loc[(merge_sel["Alignment_Station_real"] >= TunnelLayoutData_Station_real_list[n])
        & (merge_sel["Alignment_Station_real"] < TunnelLayoutData_Station_real_list[nn]), "SectionArea"] \
        = TunnelLayoutData_df["SectionArea"].tolist()[n]
    merge_sel.loc[(merge_sel["Alignment_Station_real"] >= TunnelLayoutData_Station_real_list[n])
        & (merge_sel["Alignment_Station_real"] < TunnelLayoutData_Station_real_list[nn]), "Description"] \
        = TunnelLayoutData_df["Description"].tolist()[n]

    
# ----------------------------------------------------------------------------------------------------------------
# calculate "BoreClass", "SupportClass" and "DisposalClass"
#   define Tunnel height and BoreClass rules at start of procedure, for easy modification        JK ToDo 
# result: merge_sel["BoreClass"], merge_sel["SupportClass"], merge_sel["DisposalClass"]
print 'calculating BoreClass, SupportClass and DisposalClass'
# ----------------------------------------------------------------------------------------------------------------

merge_sel["BoreClass"]= np.nan
merge_sel["SupportClass"]= np.nan
merge_sel["DisposalClass"]= np.nan

tunn_h =13.0   #Tunnel height
TunnelExcavationData = merge_sel  # JK -temporary until variable name merge_sel replaced with TunnelExcavationData

# define BoreClass as class, to separate definition of methods from execution
#   This makes it possible to define the BoreClass methods outside of this routine (e.g. at start of script).
#   Class method is used as a modifier to the TunnelExcavationData (dataframe) class.
class BoreClass:
    """Determine Bore Class for TBM tunnels"""
    # BC1 - tunnel predominantly in soil
    def bc1(self):
        TunnelExcavationData.loc[(TunnelExcavationData["ExcavationType"] == "TBM") & 
        (TunnelExcavationData["Rocksurface"] <= TunnelExcavationData["Elevation"] -tunn_h*0.25),"BoreClass"] \
        ="BC1"
    # BC2 - tunnel with mixed face
    def bc2(self):
        TunnelExcavationData.loc[(TunnelExcavationData["ExcavationType"] == "TBM") & 
        (TunnelExcavationData["Rocksurface"] > TunnelExcavationData["Elevation"] -tunn_h*0.25) & 
        (TunnelExcavationData["Rocksurface"] < TunnelExcavationData["Elevation"] +tunn_h/2.0 +1.5),"BoreClass"] \
        = "BC2"
    # BC3 - tunnel inf rock
    def bc3(self):
        TunnelExcavationData.loc[(TunnelExcavationData["ExcavationType"] == "TBM") & \
        (TunnelExcavationData["Rocksurface"] >= TunnelExcavationData["Elevation"] +tunn_h/2.0 +1.5),"BoreClass"] \
        = "BC3"

# instantiate an instance of BoreClass
bore_class=BoreClass()
# call bore_class methods for BC1, BC2, BC3
bore_class.bc1()
bore_class.bc2()
bore_class.bc3()
# check: merge_sel["BoreClass"].value_counts()  # equals 805+188+60 for Ostroehre
# check: merge_sel["ExcavationType"].value_counts() 

##th =13.0   #Tunnel height
##  BC1
##merge_sel.loc[(merge_sel["ExcavationType"] == "TBM") & \
##    (merge_sel["Rocksurface"] <= merge_sel["Elevation"] -th*0.25),"BoreClass"] ="BC1"     
#  BC2   
##merge_sel.loc[(merge_sel["ExcavationType"] == "TBM") & \
##    (merge_sel["Rocksurface"] > merge_sel["Elevation"] -th*0.25) & 
##    (merge_sel["Rocksurface"] < merge_sel["Elevation"]+ th/2.0 +1.5), "BoreClass"] = "BC2"     
#  BC3        
##merge_sel.loc[(merge_sel["ExcavationType"] == "TBM") & \
##    (merge_sel["Rocksurface"] >= merge_sel["Elevation"]+ th/2.0 +1.5), "BoreClass"] = "BC3"

# Support Class                                                             # JK ToDo: define SC's as Class
#  SCT
merge_sel.loc[(merge_sel["ExcavationType"] == "TBM"), \
    "SupportClass"] = "SCT"
#  SC5
merge_sel.loc[(merge_sel["ExcavationType"] == "MUL"), \
    "SupportClass"] = "SC5"
# check: merge_sel["SupportClass"].value_counts()
# check: merge_sel["ExcavationType"].value_counts() 

# Disposal Class                                                            # JK ToDo: define MC's as Class
#  MC5
merge_sel.loc[(merge_sel["BoreClass"] ==  "BC1") | (merge_sel["BoreClass"] == "BC2"), \
    "DisposalClass"] = "MC5"
#  MC3
merge_sel.loc[(merge_sel["BoreClass"] ==  "BC3"), \
    "DisposalClass"] = "MC3"
#  MC2
merge_sel.loc[(merge_sel["ExcavationType"] == "MUL"), \
    "DisposalClass"] = "MC2"
# check: merge_sel["DisposalClass"].value_counts()
# check: merge_sel["ExcavationType"].value_counts() # 805+248
# check:
#     print merge_sel.loc[:,["Station","ExcavationType","BoreClass","SupportClass","DisposalClass"]].to_string()


# ----------------------------------------------------------------------------------------------------------------
# calculate volume of tunnel between two axis points
print 'calcuating volume'
# ----------------------------------------------------------------------------------------------------------------

# initialize interval length (Distance field)
merge_sel["Distance"] = np.nan
merge_sel["Volume"] = np.nan

# Calculate "Distance", "Area1_mean_dist" and "Area2_mean_dist"
n = 0

# use .iat instead of .iloc to return scalar values (*1000 faster)
# TunnelLayoutData must show missing data as NaN (None is read as string value)
for i in range(len(merge_sel.index) -1):
    nn= n+1
    merge_sel["Distance"].iat[n] = ((merge_sel["Easting"].iat[nn] -merge_sel["Easting"].iat[n])**2 
        +(merge_sel["Northing"].iat[nn] -merge_sel["Northing"].iat[n])**2 
        +(merge_sel["Elevation"].iat[nn] -merge_sel["Elevation"].iat[n])**2 )**(0.5)
    merge_sel["Volume"].iat[n] = merge_sel["SectionArea"].iat[n] * merge_sel["Distance"].iat[n]
    n = n+1
# check:
#     print merge_sel.loc[:,["Station","ExcavationType","Distance","SectionArea","Volume"]].to_string()

merge_sel.to_csv("WORK/Ostroehre.TunnelExcavationData.R2.csv", sep=",")
