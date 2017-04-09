#!/usr/bin/python
# TunnelVariables.JK.py

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
# "TunnelGIS.Rheintunnel/WORK/swissalti3dgeotifflv03-5m/swissALTI3D_.tif"   -DEM with surface topography
# "TunnelGIS.Rheintunnel/WORK/Felsisohypsen-raster.tif"                     -DEM with rock surfac
# "TunnelGIS.Rheintunnel/WORK/OstrohrR2.csv"                                -stationed tunnel alignment#

# References:
# http://gis.stackexchange.com/questions/197825/how-to-convert-multiple-csv-files-to-shp-using-python-and-no-arcpy
# to get grass help:   processing.alghelp("grass7:r.what.points")

# IMPORTANT: requires qgis setup before running this procedure
# run ./pyqgis.sh from command line before starting python (or set up IDE accordingly)

# import required libraries
import pandas as pd
import numpy as np
import geopandas as gpd
import shapely as sp
import os 

# set wd for this procedure                                                      #awkward: fix  ToDo JK
os.chdir("/home/kaelin_joseph/")

# define input files
DTM = "TunnelGIS.Rheintunnel/WORK/swissalti3dgeotifflv03-5m/swissALTI3D_.tif"
Bedrock_surface = "TunnelGIS.Rheintunnel/WORK/Felsisohypsen-raster.tif"
Alignment_csv = "TunnelGIS.Rheintunnel/WORK/Ostroehre.AlignmentData.R2.csv"

# define output files
Alignment_shp ='TunnelGIS.Rheintunnel/WORK/OstrohrR2.shp'
Alignment_DTM = "TunnelGIS.Rheintunnel/WORK/OstrohrR2_DTM.csv"
Alignment_Bedrock_surface = "TunnelGIS.Rheintunnel/WORK/OstrohrR2_Bedrock_surface.csv"
Alignment_Tunnel_variables = "TunnelGIS.Rheintunnel/WORK/OstrohrR2_Tunnel_variables.csv"


# create Alignment_spatial from Alignment_csv
# result: Alignment_shp
Alignment_df = pd.read_csv(Alignment_csv)
Alignment_df = Alignment_df.dropna(how = "all")  #delete row if only NA are present in row
Alignment_df = Alignment_df.drop(Alignment_df.index[len(Alignment_df)-1])  #delete trailing blank line
Alignment_spatial_points = [sp.geometry.Point(row['Easting'], row['Northing'])
                            for key, row in Alignment_df.iterrows()]
Alignment_crs = {'init': 'epsg:2056'}  #define crs
Alignment_spatial = gpd.GeoDataFrame(Alignment_df, geometry=Alignment_spatial_points, crs = Alignment_crs)
Alignment_spatial.to_file(Alignment_shp, driver='ESRI Shapefile') 


# use grass functions to get raster values for points along tunnel axis and write to .csv files
# result: Alignment_DTM & Alignment_Bedrock_surface
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


# prepare for join of grass results using pandas
Alignment_DTM_df  = pd.read_csv(Alignment_DTM)
Alignment_Bedrock_surface_df  = pd.read_csv(Alignment_Bedrock_surface)
# result: Alignment_DTM_df, Alignment_Bedrock_surface_df                
# result: Alignment_df, Alignment_DTM_df_sel, Alignment_Bedrock_surface_df_sel
# check with:  Alignment_df.head()
Alignment_df = Alignment_df.loc[:,["Station","Easting", "Northing", "Elevation"]]
# check:  Alignment_df.head()
# check:  Alignment_DTM_df.head()
Alignment_DTM_df_coleqtmp = [col for col in Alignment_DTM_df.columns if 'tmp' in col]
if len(Alignment_DTM_df_coleqtmp) != 1:
    print "Extraction of DTM col=tmp did not work properly. Please check"
    exit()
Alignment_DTM_df_rename = Alignment_DTM_df.rename(
    columns= {Alignment_DTM_df_coleqtmp[0]: "DTM"})
Alignment_DTM_df_sel = Alignment_DTM_df_rename.loc[:,["easting", "northing", "DTM"]]
# check:  Alignment_DTM_df_sel.head()
# check:  Alignment_Bedrock_surface_df.head()
Alignment_Bedrock_surface_df_coleqtmp = [col for col in Alignment_Bedrock_surface_df.columns if 'tmp' in col]
if len(Alignment_Bedrock_surface_df_coleqtmp) != 1:
    print "Extraction of Bedrock_surface_csv_coleqtmp col=tmp did not work properly. Please check"
    exit()
Alignment_Bedrock_surface_df_rename = Alignment_Bedrock_surface_df.rename(
    columns= {Alignment_Bedrock_surface_df_coleqtmp[0]: "Rocksurface"})
Alignment_Bedrock_surface_df_sel = Alignment_Bedrock_surface_df_rename.loc[
    :,["easting", "northing", "Rocksurface"]]
# check:  Alignment_Bedrock_surface_df_sel.head()


# join grass results using Panda
# result: merge_final
# join DTM to Alignment_df
merge_Alignment_DTM= pd.merge(Alignment_df, Alignment_DTM_df_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"])
# check:  merge_Alignment_DTM.head()
# chekc:  merge_Alignment_DTM.columns
# join Rocksurface to merge_Alignment_DTM
merge_final = pd.merge(merge_Alignment_DTM, Alignment_Bedrock_surface_df_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"])
# check:  merge_final.head()
# check:  merge_final.columns
# clean up join of grass results using panda: define columns that should be kept for following analysis
# result: merge_sel
merge_sel = merge_final.loc[:,["Easting", "Northing", "Elevation", "DTM", "Rocksurface"]]
# check:  merge_sel.head()


# calculate "delta_rocksurface_tunnelaxis"
# result: 
# check:  merge_sel.head()
merge_sel['delta_rocksurface_tunnelaxis'] = merge_sel.Rocksurface - merge_sel.Elevation


# calculate "BoreClass"
## define Tunnel height and BoreClass rules at start of procedure, for easy modification          !ToDo JK
# result: 
th =13.0   #Tunnel height
# BoreClass BC1
merge_sel.loc[merge_sel['Rocksurface'] <= merge_sel['Elevation'] -th*0.25, 'BoreClass'] ='BC1'
# BoreClass BC2
merge_sel.loc[(merge_sel['Rocksurface'] > merge_sel['Elevation'] -th*0.25) & 
              (merge_sel['Rocksurface'] < merge_sel['Elevation']+ th/2.0 +1.5), 'BoreClass'] = 'BC2'
# BoreClassBC3
merge_sel.loc[merge_sel['Rocksurface'] >= merge_sel['Elevation']+ th/2.0 +1.5, 'BoreClass'] = 'BC3'
# check:  merge_sel.head()
# check:  merge_sel.tail()
# check:  merge_sel.loc[:,["delta_rocksurface_tunnelaxis","BoreClass"]]
# check:  merge_sel.loc[merge_sel["delta_rocksurface_tunnelaxis"].idxmax()]
# check:  merge_sel.loc[merge_sel["delta_rocksurface_tunnelaxis"].idxmin()]
# check:  merge_sel["BoreClass"].value_counts()
merge_sel.to_csv(Alignment_Tunnel_variables, sep=",")


# calculate volume of tunnel between two axis points
# define cross-sectional excavation areas (Area field)
merge_sel["Area1"] = 100.0
merge_sel["Area2"] = 100.0
# initialize interval length (Distance field)
merge_sel["Distance"] = ""
merge_sel["Distance"] = np.nan
# initialize "Area1_mean_dist" field
merge_sel["Area1_mean_dist"] = ""
merge_sel["Area1_mean_dist"] = np.nan
# initialize "Area2_mean_dist" field
merge_sel["Area2_mean_dist"] = ""
merge_sel["Area2_mean_dist"] = np.nan
# Calculate "Distance", "Area1_mean_dist" and "Area2_mean_dist"
n = 0
for i in range(len(merge_sel.index)-1):
    nn= n+1
    merge_sel["Distance"].iloc[n] = ( (merge_sel["Easting"].iloc[nn] -merge_sel["Easting"].iloc[n])**2
                                    +(merge_sel["Northing"].iloc[nn] -merge_sel["Northing"].iloc[n])**2
                                    +(merge_sel["Elevation"].iloc[nn] -merge_sel["Elevation"].iloc[n])**2 )**(0.5)
    merge_sel["Area1_mean_dist"].iloc[n] = np.mean([merge_sel["Area1"].iloc[n],
                                                    merge_sel["Area1"].iloc[nn]]) * merge_sel["Distance"].iloc[n] 
    merge_sel["Area2_mean_dist"].iloc[n] = np.mean([merge_sel["Area2"].iloc[n],
                                                    merge_sel["Area2"].iloc[nn]]) * merge_sel["Distance"].iloc[n] 
    n = n+1
# check:  merge_sel.head()
merge_sel.to_csv("TunnelGIS.Rheintunnel/WORK/TunnelVariables2.csv", sep=",")
