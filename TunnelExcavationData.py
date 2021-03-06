# ----------------------------------------------------------------------------------------------------------------
# description
# ----------------------------------------------------------------------------------------------------------------

#!/usr/bin/python
# TunnelExcavationData.py

# Python procedure for TunnelGIS Engineering App
# Author: KK
# Date: 01.04.2017

# Purpose of this procedure:
# 1. Prepare input data ....
# 2.
# 3.
# 4. 
# 5. 

# This python routine is a script, intended to guide the user through the described procedure.
# As a script, the procedure does not generally include data validation and error handling.
# Users are expected to understand and adjust the code as needed for their application.

# Required Input Files:
#   "WORK/swissalti3dgeotifflv03-5m/swissALTI3D_.tif"   -DEM with surface topography
#   "WORK/Felsisohypsen-raster.tif"                     -DEM with rock surface
#   "WORK/OstrohrR2.csv"                                -stationed tunnel alignment#
#   "WORK/Ostroehre.TunnelLayoutData.R2.csv"            -tunnel layout data

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
RockSurface = "WORK/Felsisohypsen-raster.tif"            
AlignmentData = "WORK/Ostroehre.AlignmentData.R2.csv"
LayoutData = "WORK/Ostroehre.TunnelLayoutData.R2.csv"


# ----------------------------------------------------------------------------------------------------------------
# define Bore Classes
#   define Bore Classes as class, to separate definition of methods from execution
#   class method is used as a modifier to the TunnelExcavationData (dataframe) class.
# ----------------------------------------------------------------------------------------------------------------
# better to add mtethods .bc1, .bc2, .bc3 to TunnExcvDf ??

tunn_h =13.0   # define tunnel height
volume_unit='m3'  # unit to be used for volume calculation and reporting

class BoreClass:
    """Determine Bore Class for TBM tunnels"""
    # BC1 - tunnel predominantly in soil
    def bc1(self):
        TunnExcvDF.loc[(TunnExcvDF["ExcavationType"] == "TBM") & 
        (TunnExcvDF["RockSurface"] <= TunnExcvDF["Elevation"] -tunn_h*0.25),"BoreClass"] \
        ="BC1"
    # BC2 - tunnel with mixed face
    def bc2(self):
        TunnExcvDF.loc[(TunnExcvDF["ExcavationType"] == "TBM") & 
        (TunnExcvDF["RockSurface"] > TunnExcvDF["Elevation"] -tunn_h*0.25) & 
        (TunnExcvDF["RockSurface"] < TunnExcvDF["Elevation"] +tunn_h/2.0 +1.5),"BoreClass"] \
        = "BC2"
    # BC3 - tunnel inf rock
    def bc3(self):
        TunnExcvDF.loc[(TunnExcvDF["ExcavationType"] == "TBM") & \
        (TunnExcvDF["RockSurface"] >= TunnExcvDF["Elevation"] +tunn_h/2.0 +1.5),"BoreClass"] \
        = "BC3"


# ----------------------------------------------------------------------------------------------------------------
# define output files
# ----------------------------------------------------------------------------------------------------------------

TunnelExcavationData = "WORK/Ostroehre.TunnelExcavationData.R2.csv"
# headers: Station, Easting, Northing, Elevation, DTM, RockSurface, StationReal, RockCover,
#          WBScode, WorkType, ExcavationType, ProfileType, SectionArea, Description,
#          BoreClass, SupportClass, DisposalClass, StationInterval, ExcavationVolume, DisposalVolume
Alignment_SHP ='WORK/Ostroehre.Alignment.R2.shp'
BoQ = "WORK/Ostroehre.TunnelBoQdata.R2.csv"
# temporary data
Alignment_DTM = "WORK/Ostroehre.Terrain.R2.csv"
Alignment_RockSurface = "WORK/Ostroehre.RockSurface.R2.csv"  # JK ToDo: RockSurface?

# ----------------------------------------------------------------------------------------------------------------
# create alignment_df (dataframe) from .csv
# Important: Before the df is created the data should be checked.
#   E.g. make sure that it does not contain trailing blank lines and that duplicate lines are deleted.
# result: alignment_df
# ----------------------------------------------------------------------------------------------------------------

alignment_df = pd.read_csv(AlignmentData)
#delete row if only NA are present in row
alignment_df = alignment_df.dropna(how = "all")
# round alignment_df to three decimals
alignment_df = alignment_df.round(decimals=3)


# ----------------------------------------------------------------------------------------------------------------
# create layout_df from .csv
# result: layout_df
# ----------------------------------------------------------------------------------------------------------------

layout_df = pd.read_csv(LayoutData)
# round layout_df to three decimals
layout_df = layout_df.round(decimals=3)


# ----------------------------------------------------------------------------------------------------------------
# convert alignment_df["Station"] => alignment_df["StationReal"] and similar for layout_df
# result: alignment_Station_list, layout_Station_list
#         alignment_df["StationReal"], layout_df["StationReal"]
print "creating df header StationReal"
# ----------------------------------------------------------------------------------------------------------------

alignment_Station_list = alignment_df["Station"].tolist()
    # check: len(alignment_Station_list)

alignment_df["StationReal"] = np.nan

for n in range(0, len(alignment_Station_list)):
    station_sel = alignment_df.iloc[n]["Station"]
    station_real_sel = float(station_sel.replace("+",""))
    alignment_df.iloc[n, alignment_df.columns.get_loc("StationReal")] = station_real_sel
    # alignment_df.columns.get_loc("StationReal") = 5

# layout_df["Station"] => layout_df["StationReal"] 
layout_Station_list = layout_df["Station"].tolist()
    # check: len(layout_Station_list)

layout_df["StationReal"] = np.nan

for n in range(0, len(layout_Station_list)):
    station_sel = layout_df.iloc[n]["Station"]
    station_real_sel = float(station_sel.replace("+",""))
    layout_df.iloc[n, layout_df.columns.get_loc("StationReal")] \
        = station_real_sel


# ----------------------------------------------------------------------------------------------------------------
# check if every layout_df["StationReal"] exists in alignment_df["StationReal"]
#   If it does not exist, create a new Station in alignment_df
# result: alignment_StationReal_list, layout_StationReal_list
#         alignment_df with added Stations
print "adding Stations"
# ----------------------------------------------------------------------------------------------------------------

alignment_StationReal_list = alignment_df["StationReal"].tolist()
layout_StationReal_list = layout_df["StationReal"].tolist()

# within this vicinity of a station no new station will be created
vicinity = 0.1

# define new variables
easting_newpoint = []
northing_newpoint = []
elevation_newpoint = []
station = []
station_real = []

# Loop through stations
for n in layout_StationReal_list:
    if n in alignment_StationReal_list:
        pass
    else:
        neighbour1_StationReal = max([i for i in alignment_StationReal_list if i < n]) 
        neighbour2_StationReal = min([i for i in alignment_StationReal_list if i > n])       
        ####if n < neighbour1_StationReal + vicinity or n > neighbour2_StationReal + vicinity:      KLK: check
        if n < neighbour1_StationReal + vicinity or n > neighbour2_StationReal - vicinity:
            pass
        else: 
            neighbour1 = alignment_df.loc[alignment_df["StationReal"]
                                          == neighbour1_StationReal,]
            neighbour2 = alignment_df.loc[alignment_df["StationReal"]
                                          == neighbour2_StationReal,]
            ####delta_x_neighbour1_2 = abs(neighbour2.Easting.tolist()[0] -neighbour1.Easting.tolist()[0])
            ####delta_y_neighbour1_2 = abs(neighbour2.Northing.tolist()[0] -neighbour1.Northing.tolist()[0])
            ####                                                                                  KLK: check
            delta_x_neighbour1_2 = neighbour2.Easting.tolist()[0] -neighbour1.Easting.tolist()[0] #delta x
            delta_y_neighbour1_2 = neighbour2.Northing.tolist()[0] -neighbour1.Northing.tolist()[0] #delta y
            delta_z_neighbour1_2 = neighbour2.Elevation.tolist()[0] -neighbour1.Elevation.tolist()[0] #delta z
            length_neighbour1_2 = (delta_x_neighbour1_2**2 +delta_y_neighbour1_2**2)**(0.5) # L
            length_neighbour1_newpoint = n- neighbour1.StationReal.tolist()[0]
            ####easting_newpoint_sel = neighbour2.Easting.tolist()[0] \
            ####                     +((delta_y_neighbour1_2*length_neighbour1_newpoint)/length_neighbour1_2)
            ####northing_newpoint_sel = neighbour2.Northing.tolist()[0] \
            ####                      +((delta_x_neighbour1_2*length_neighbour1_newpoint)/length_neighbour1_2)
            ####elevation_newpoint_sel = neighbour2.Elevation.tolist()[0] \
            ####                       +((delta_x_neighbour1_2*length_neighbour1_newpoint)/length_neighbour1_2)
            ####                                                                                  KLK: check
            easting_newpoint_sel = neighbour1.Easting.tolist()[0] \
                                 +((delta_x_neighbour1_2*length_neighbour1_newpoint)/length_neighbour1_2)
            northing_newpoint_sel = neighbour1.Northing.tolist()[0] \
                                  +((delta_y_neighbour1_2*length_neighbour1_newpoint)/length_neighbour1_2)
            elevation_newpoint_sel = neighbour1.Elevation.tolist()[0] \
                                   +((delta_z_neighbour1_2*length_neighbour1_newpoint)/length_neighbour1_2)
            easting_newpoint.append(easting_newpoint_sel)
            northing_newpoint.append(northing_newpoint_sel)
            elevation_newpoint.append(elevation_newpoint_sel)
            station_real.append(n)
            print "    ", neighbour1
            print "    ", neighbour2
            print "    station_real", n
            print "    easting_newpoint_sel", easting_newpoint_sel
            print "    northing_newpoint_sel", northing_newpoint_sel
            print "    elevation_newpoint_sel", elevation_newpoint_sel
            # this procedure must be tested for all combinations of ascending/descending
            #   Northing, Easting and Elevation --> should be OK
            #   for descending Stationing --> needs fixing                                          JK ToDo
            Station_sel = layout_df.loc[layout_df['StationReal']
                                                  == n, 'Station'] 
            station.append(Station_sel.tolist()[0])
           
newStation_df = pd.DataFrame({"Easting": easting_newpoint, "Northing": northing_newpoint,
                              "Elevation": elevation_newpoint, "StationReal": station_real,
                              "Station": station})
    # check len(alignment_df)
    # check len(newStation_df)

# Contatenate alignment_df with newStation_df
# result: alignment_df
frames = [alignment_df, newStation_df]
alignment_df = pd.concat(frames)
    # check: len(alignment_df)
    # check: alignment_df.tail()

    
# ----------------------------------------------------------------------------------------------------------------
# create Alignment_spatial from alignment_df
# result: Alignment_SHP
# ----------------------------------------------------------------------------------------------------------------

Alignment_spatial_points = [sp.geometry.Point(row['Easting'], row['Northing'])
                            for key, row in alignment_df.iterrows()]
Alignment_crs = {'init': 'epsg:2056'}  #define crs
Alignment_spatial = gpd.GeoDataFrame(alignment_df, geometry=Alignment_spatial_points, crs = Alignment_crs)
Alignment_spatial.to_file(Alignment_SHP, driver='ESRI Shapefile') 


# ----------------------------------------------------------------------------------------------------------------
# use grass functions to get raster values for points along tunnel axis and write to .csv files
# result: Alignment_DTM, Alignment_RockSurface
print "get raster values"
# ----------------------------------------------------------------------------------------------------------------

# Alignment_DTM
processing.runalg("grass7:r.what.points",DTM,Alignment_SHP,
                  "NA",",",500,True,False,False,False,False,
                  "2603510.0,2624270.0,1260650.0,1274890.0",-1,0.0001,Alignment_DTM)
# Alignment_RockSurface                  
processing.runalg("grass7:r.what.points",RockSurface,Alignment_SHP,
                  "NA",",",500, True,False,False,False,False,
                  "2603510.0,2624270.0,1260650.0,1274890.0",-1,0.0001,Alignment_RockSurface)
## warning: Not all input layers use the same CRS -> data seems OK
    # check:  Alginemnt_spatial.crs


# ----------------------------------------------------------------------------------------------------------------
# create df's
# result: Alignment_DTM_df, Alignment_RockSurface_df
# ----------------------------------------------------------------------------------------------------------------
Alignment_DTM_df  = pd.read_csv(Alignment_DTM)
Alignment_RockSurface_df  = pd.read_csv(Alignment_RockSurface)


# ----------------------------------------------------------------------------------------------------------------
# prepare for join of grass results using pandas
# result: alignment_df, Alignment_DTM_df_sel, Alignment_RockSurface_df_sel
# ----------------------------------------------------------------------------------------------------------------

# prepare alignment_df
    # check:  alignment_df.head()
alignment_df = alignment_df.loc[:,["Station","Easting", "Northing", "Elevation", "StationReal"]]
    # check:  alignment_df.head()

# prepare Alignment_DTM_df_sel
    # check:  Alignment_DTM_df.head()
Alignment_DTM_df_coleqtmp = [col for col in Alignment_DTM_df.columns if 'tmp' in col]
if len(Alignment_DTM_df_coleqtmp) != 1:
    print "Extraction of DTM col=tmp did not work properly. Please check"
    exit()
Alignment_DTM_df_rename = Alignment_DTM_df.rename(
    columns= {Alignment_DTM_df_coleqtmp[0]: "DTM"})
Alignment_DTM_df_sel = Alignment_DTM_df_rename.loc[:,["easting", "northing", "DTM"]]
    # check:  Alignment_RockSurface_df.head()

# prepare Alignment_RockSurface_df_coleqtmp
Alignment_RockSurface_df_coleqtmp = [col for col in Alignment_RockSurface_df.columns if 'tmp' in col]
if len(Alignment_RockSurface_df_coleqtmp) != 1:
    print "Extraction of RockSurface_csv_coleqtmp col=tmp did not work properly. Please check"
    exit()
Alignment_RockSurface_df_rename = Alignment_RockSurface_df.rename(
    columns= {Alignment_RockSurface_df_coleqtmp[0]: "RockSurface"})
Alignment_RockSurface_df_sel = Alignment_RockSurface_df_rename.loc[
    :,["easting", "northing", "RockSurface"]]  
    # check:  Alignment_RockSurface_df_sel.head()


# ----------------------------------------------------------------------------------------------------------------
# join grass results using Panda
#    merge handles floats as keys inconsistently, round df's to three decimals before merge 
# result: merge_final
print 'merge_final'
# ----------------------------------------------------------------------------------------------------------------

alignment_df = alignment_df.round(decimals=3)
Alignment_DTM_df_sel = Alignment_DTM_df_sel.round(decimals=3)
Alignment_RockSurface_df_sel = Alignment_RockSurface_df_sel.round(decimals=3)

# merge DTM to Alignment
merge_Alignment_DTM= pd.merge(left= alignment_df, right = Alignment_DTM_df_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"], how = "left")

# merge RockSurface to Alignment_DTM
merge_final = pd.merge(merge_Alignment_DTM, Alignment_RockSurface_df_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"])
    # check:  merge_final.head()
    # check:  merge_final.columns

    
# ----------------------------------------------------------------------------------------------------------------
# clean up merge_final
# result: TunnExcvDF
print 'cleaning up merge'
# ----------------------------------------------------------------------------------------------------------------

TunnExcvDF = merge_final.loc[:,["Station","Easting", "Northing", "Elevation", "DTM", "RockSurface",
                               "StationReal"]]
    # check:  TunnExcvDF.head()
    # check:  list(TunnExcvDF)
# sort by Station
TunnExcvDF = TunnExcvDF.sort(['StationReal'], ascending=[1])

    
# ----------------------------------------------------------------------------------------------------------------
# calculate difference height rocksurface and tunnel axis
# result: TunnExcvDF['RockCover']
# ----------------------------------------------------------------------------------------------------------------

TunnExcvDF['RockCover'] = TunnExcvDF.RockSurface - TunnExcvDF.Elevation


# ----------------------------------------------------------------------------------------------------------------
# assign WBS, WorkType, Excavation Type, Profile Type, Section Area from TunnelLayoutDarta
# result: TunnExcvDF["WBScode"], TunnExcvDF["WorkType"], TunnExcvDF["ExcavationType"], TunnExcvDF["ProfileType"]
#         TunnExcvDF["SectionArea"], TunnExcvDF["Description"]
print "working on WBS etc"
# ----------------------------------------------------------------------------------------------------------------

TunnExcvDF["WBScode"] = np.nan
TunnExcvDF["WorkType"] = np.nan
TunnExcvDF["ExcavationType"] = np.nan
TunnExcvDF["ProfileType"] = np.nan
TunnExcvDF["SectionArea"] = np.nan
TunnExcvDF["Description"] = np.nan
TunnExcvDF["Unit"] = volume_unit

for n in range(0, len(layout_StationReal_list)):
    nn = n+1 
    if n == len(layout_StationReal_list) -1:
        layout_StationReal_list.append(1e12)
    TunnExcvDF.loc[(TunnExcvDF["StationReal"] >= layout_StationReal_list[n])
        & (TunnExcvDF["StationReal"] < layout_StationReal_list[nn]), "WBScode"] \
        = layout_df["WBScode"].tolist()[n]
    TunnExcvDF.loc[(TunnExcvDF["StationReal"] >= layout_StationReal_list[n])
        & (TunnExcvDF["StationReal"] < layout_StationReal_list[nn]), "WorkType"] \
        = layout_df["WorkType"].tolist()[n]
    TunnExcvDF.loc[(TunnExcvDF["StationReal"] >= layout_StationReal_list[n])
        & (TunnExcvDF["StationReal"] < layout_StationReal_list[nn]), "ExcavationType"] \
        = layout_df["ExcavationType"].tolist()[n]
    TunnExcvDF.loc[(TunnExcvDF["StationReal"] >= layout_StationReal_list[n])
        & (TunnExcvDF["StationReal"] < layout_StationReal_list[nn]), "ProfileType"] \
        = layout_df["ProfileType"].tolist()[n]
    TunnExcvDF.loc[(TunnExcvDF["StationReal"] >= layout_StationReal_list[n])
        & (TunnExcvDF["StationReal"] < layout_StationReal_list[nn]), "SectionArea"] \
        = layout_df["SectionArea"].tolist()[n]
    TunnExcvDF.loc[(TunnExcvDF["StationReal"] >= layout_StationReal_list[n])
        & (TunnExcvDF["StationReal"] < layout_StationReal_list[nn]), "Description"] \
        = layout_df["Description"].tolist()[n]

    
# ----------------------------------------------------------------------------------------------------------------
# calculate "BoreClass", "SupportClass" and "DisposalClass"
# result: TunnExcvDF["BoreClass"], TunnExcvDF["SupportClass"], TunnExcvDF["DisposalClass"]
print 'calculating BoreClass, SupportClass and DisposalClass'
# ----------------------------------------------------------------------------------------------------------------

TunnExcvDF["BoreClass"]= np.nan
TunnExcvDF["SupportClass"]= np.nan
TunnExcvDF["DisposalClass"]= np.nan

# instantiate an instance of BoreClass
bore_class=BoreClass()
# call bore_class methods for BC1, BC2, BC3
bore_class.bc1()
bore_class.bc2()
bore_class.bc3()
print TunnExcvDF["BoreClass"].value_counts()  # equals 805+188+60 for Ostroehre
print TunnExcvDF["ExcavationType"].value_counts() 

# Support Class                                                             # JK ToDo: define SC's as Class
#  SCT
TunnExcvDF.loc[(TunnExcvDF["ExcavationType"] == "TBM"), \
    "SupportClass"] = "SCT"
#  SC5
TunnExcvDF.loc[(TunnExcvDF["ExcavationType"] == "MUL"), \
    "SupportClass"] = "SC5"
# check: TunnExcvDF["SupportClass"].value_counts()
# check: TunnExcvDF["ExcavationType"].value_counts() 

# Disposal Class                                                            # JK ToDo: define MC's as Class
#  MC5
TunnExcvDF.loc[(TunnExcvDF["BoreClass"] ==  "BC1") | (TunnExcvDF["BoreClass"] == "BC2"), \
    "DisposalClass"] = "MC5"
#  MC3
TunnExcvDF.loc[(TunnExcvDF["BoreClass"] ==  "BC3"), \
    "DisposalClass"] = "MC3"
#  MC2
TunnExcvDF.loc[(TunnExcvDF["ExcavationType"] == "MUL"), \
    "DisposalClass"] = "MC2"
# check: TunnExcvDF["DisposalClass"].value_counts()
# check: TunnExcvDF["ExcavationType"].value_counts() # 805+248
# check:
#     print TunnExcvDF.loc[:,["Station","ExcavationType","BoreClass","SupportClass","DisposalClass"]].to_string()


# ----------------------------------------------------------------------------------------------------------------
# calculate excavation volume of tunnel between two axis points
print 'calcuating excavation volume'
# ----------------------------------------------------------------------------------------------------------------

# initialize interval length (StationInterval field)
TunnExcvDF["StationInterval"] = np.nan
TunnExcvDF["ExcavationVolume"] = np.nan

# Calculate "StationInterval", "Area1_mean_dist" and "Area2_mean_dist"
n = 0

# use .iat instead of .iloc to return scalar values (*1000 faster)
# LayoutData must show missing data as NaN (None is read as string value)
for i in range(len(TunnExcvDF.index) -1):
    nn= n+1
    TunnExcvDF["StationInterval"].iat[n] = ((TunnExcvDF["Easting"].iat[nn] -TunnExcvDF["Easting"].iat[n])**2 
        +(TunnExcvDF["Northing"].iat[nn] -TunnExcvDF["Northing"].iat[n])**2 
        +(TunnExcvDF["Elevation"].iat[nn] -TunnExcvDF["Elevation"].iat[n])**2 )**(0.5)
    TunnExcvDF["ExcavationVolume"].iat[n] = TunnExcvDF["SectionArea"].iat[n] * TunnExcvDF["StationInterval"].iat[n]
    n = n+1
# check:
#    print TunnExcvDF.loc[:,["Station","ExcavationType","StationInterval","ExcavationVolume"]]


# ----------------------------------------------------------------------------------------------------------------
# calculate disposal volume of tunnel between two axis points
print 'calcuating disposal volume'
# result: file TunnelExcavationData as .csv)
# ----------------------------------------------------------------------------------------------------------------

# mv to beginning of file                                                        JK ToDo
def disposal_volume(ExcavationVolume, DisposalClass):
    #calculate Disposal Volumes based on Disposal Class
    DisposalVolume=np.nan
    if DisposalClass=="MC2":
        DisposalVolume=1.3*ExcavationVolume
    elif DisposalClass=="MC3":
        DisposalVolume=1.5*ExcavationVolume 
    elif DisposalClass=="MC5":
        DisposalVolume=1.3*ExcavationVolume
    #else:
        #print "unknown disposal class"
    return DisposalVolume

TunnExcvDF["DisposalVolume"] = np.nan
n = 0
for i in range(len(TunnExcvDF.index) -1):
    TunnExcvDF["DisposalVolume"].iat[n] = (
        disposal_volume(TunnExcvDF["ExcavationVolume"].iat[n],TunnExcvDF["DisposalClass"].iat[n]) )
    n = n+1
# check:
#  print TunnExcvDF.loc[:,["Station","DisposalType","ExcavationVolume","DisposalVolume"]]

TunnExcvDF.to_csv(TunnelExcavationData, sep=",", na_rep="NaN")


# ----------------------------------------------------------------------------------------------------------------
# create BoQ and write to file
# results: BoQ_df and BoQ as .csv
print 'creating BoQ'
# ----------------------------------------------------------------------------------------------------------------
# replace print with write to file                                             ToDo JK

# initialize a BoQ_list
BoQ_list_headers= ["WBS","WorkType","ExcavationType","StationFrom","StationTo","PayItem","Quantity","Unit"]
BoQ_list_values=[]

# find combinations of WBScode, ExcavationType and [BoreClass | Support Class | Disposal Class that exist
# calculate excavation volume for each combination
for i in TunnExcvDF["WBScode"].unique():
    for j in TunnExcvDF["ExcavationType"].unique():
        if ((TunnExcvDF["WBScode"] == i)
             & (TunnExcvDF["ExcavationType"] == j)).any():
            work_type = (TunnExcvDF.loc[
                ((TunnExcvDF["WBScode"] == i)
                & (TunnExcvDF["ExcavationType"] == j)),"WorkType"]).unique()[0]
        for k in TunnExcvDF["BoreClass"].unique():
            # if DF record with i, j, k (as Bore Class) exists:
            if ((TunnExcvDF["WBScode"] == i)
                & (TunnExcvDF["ExcavationType"] == j)
                & (TunnExcvDF["BoreClass"] == k)).any():
                start_station = min(TunnExcvDF.loc[
                    ((TunnExcvDF["WBScode"] == i)
                     & (TunnExcvDF["ExcavationType"] == j)),"Station"])
                end_station = max(TunnExcvDF.loc[
                    ((TunnExcvDF["WBScode"] == i)
                     & (TunnExcvDF["ExcavationType"] == j)),"Station"])
                #need 'Station +1' because we are going From: To: along alignment
                #TunnExcvDF.loc[(TunnExcvDF["Station"] == end_station),"Station"].values[0]    ToDo Note JK
                end_station_index=TunnExcvDF.index.get_loc(
                    TunnExcvDF.loc[(TunnExcvDF["Station"] == end_station),"Station"].index[0]) +1
                end_station=TunnExcvDF.iloc[end_station_index,TunnExcvDF.columns.get_loc("Station")]
                volume_sum=TunnExcvDF.loc[
                    ((TunnExcvDF["WBScode"] == i)
                     & (TunnExcvDF["ExcavationType"] == j)
                     & (TunnExcvDF["BoreClass"] == k)),"ExcavationVolume"].sum()
                BoQ_list_values.append((i,work_type,j,start_station,end_station,k,volume_sum,volume_unit))
                print i, work_type, j, start_station, end_station, k, volume_sum, volume_unit
        for k in TunnExcvDF["SupportClass"].unique():
            # if DF record with i, j, k (as Support Class) exists:
            if ((TunnExcvDF["WBScode"] == i)
                & (TunnExcvDF["ExcavationType"] == j)
                & (TunnExcvDF["SupportClass"] == k)).any():                    
                start_station = min(TunnExcvDF.loc[
                    ((TunnExcvDF["WBScode"] == i)
                     & (TunnExcvDF["ExcavationType"] == j)),"Station"])
                end_station = max(TunnExcvDF.loc[
                    ((TunnExcvDF["WBScode"] == i)
                     & (TunnExcvDF["ExcavationType"] == j)),"Station"])
                end_station_index=TunnExcvDF.index.get_loc(
                    TunnExcvDF.loc[(TunnExcvDF["Station"] == end_station),"Station"].index[0]) +1
                end_station=TunnExcvDF.iloc[end_station_index,TunnExcvDF.columns.get_loc("Station")]
                volume_sum=TunnExcvDF.loc[
                    ((TunnExcvDF["WBScode"] == i)
                     & (TunnExcvDF["ExcavationType"] == j)
                     & (TunnExcvDF["SupportClass"] == k)),"ExcavationVolume"].sum()
                BoQ_list_values.append((i,work_type,j,start_station,end_station,k,volume_sum,volume_unit))
                print i, work_type, j, start_station, end_station, k, volume_sum, volume_unit
        for k in TunnExcvDF["DisposalClass"].unique():
            # if DF record with i, j, k (as Support Class) exists:
            if ((TunnExcvDF["WBScode"] == i)
                & (TunnExcvDF["ExcavationType"] == j)
                & (TunnExcvDF["DisposalClass"] == k)).any():                    
                start_station = min(TunnExcvDF.loc[
                    ((TunnExcvDF["WBScode"] == i)
                     & (TunnExcvDF["ExcavationType"] == j)),"Station"])
                end_station = max(TunnExcvDF.loc[
                    ((TunnExcvDF["WBScode"] == i)
                     & (TunnExcvDF["ExcavationType"] == j)),"Station"])
                end_station_index=TunnExcvDF.index.get_loc(
                    TunnExcvDF.loc[(TunnExcvDF["Station"] == end_station),"Station"].index[0]) +1
                end_station=TunnExcvDF.iloc[end_station_index,TunnExcvDF.columns.get_loc("Station")]
                volume_sum=TunnExcvDF.loc[
                    ((TunnExcvDF["WBScode"] == i)
                     & (TunnExcvDF["ExcavationType"] == j)
                     & (TunnExcvDF["DisposalClass"] == k)),"DisposalVolume"].sum()
                BoQ_list_values.append((i,work_type,j,start_station,end_station,k,volume_sum,volume_unit))
                print i, work_type, j, start_station, end_station, k, volume_sum, volume_unit
# check:
#print TunnExcvDF.loc[TunnExcvDF["ExcavationType"] == "TBM", "ExcavationVolume"].sum()
#print TunnExcvDF.loc[TunnExcvDF["ExcavationType"] == "TBM", "DisposalVolume"].sum()

BoQ_df =  pd.DataFrame(BoQ_list_values, columns=BoQ_list_headers).round(decimals=3)
BoQ_df.to_csv(BoQ, sep=",", na_rep="NaN")
