#=========================================================================================================================
# Python Procedure for TunnelGIS
# Author: KK
# Date: 01.04.2017
#=========================================================================================================================

#=========================================================================================================================
# import library
#=========================================================================================================================
import pandas as pd
import numpy as np
import geopandas as gpd
import shapely as sp
import os 

#=========================================================================================================================
# setwd 
#=========================================================================================================================
os.chdir =("/home/kaelin_joseph/")

#=========================================================================================================================
# name of input files
#=========================================================================================================================
DTM = "TunnelGIS.Rheintunnel/WORK/swissalti3dgeotifflv03-5m/swissALTI3D_.tif"
Felsoberflaeche = "TunnelGIS.Rheintunnel/WORK/Felsisohypsen-raster.tif"
Ostrohr_csv = "TunnelGIS.Rheintunnel/WORK/OstrohrR2.csv"

#=========================================================================================================================
# name of output files
#=========================================================================================================================Ostrohr_spatial ='TunnelGIS.Rheintunnel/WORK/OstrohrR2.shp'
Ostrohr_DTM = "TunnelGIS.Rheintunnel/WORK/Ostrohr_DTM.csv"
Ostrohr_Felsoberflaeche = "TunnelGIS.Rheintunnel/WORK/Ostrohr_Felsoberflaeche.csv"

#=========================================================================================================================
# create *.shp from *.csv
# http://gis.stackexchange.com/questions/197825/how-to-convert-multiple-csv-files-to-shp-using-python-and-no-arcpy
# result: Ostrohr_spatial
#=========================================================================================================================
Ostrohr_df = pd.read_csv(Ostrohr_csv)
Ostrohr_df = Ostrohr_df.dropna(how = "all") # delete row if only NA are present
Ostrohr_df = Ostrohr_df.drop(Ostrohr_df.index[len(Ostrohr_df)-1]) # delte trailing blank line
Ostrohr_spatial = Ostrohr_df
Ostrohr_spatial_points = [sp.geometry.Point(row['Easting'], row['Northing']) for key, row in Ostrohr_spatial.iterrows()]
Ostrohr_crs = {'init': 'epsg:2056'} # define crs
Ostrohr_spatial = gpd.GeoDataFrame(Ostrohr_spatial,geometry=Ostrohr_spatial_points, crs = Ostrohr_crs)
Ostrohr_spatial.to_file('TunnelGIS.Rheintunnel/WORK/OstrohrR2.shp', driver='ESRI Shapefile') 

#=========================================================================================================================
# use grass functions to get raster values for points along tunnel axis and write to .csv files
# result: Ostrohr_DTM & Ostrohr_Felsoberflaeche
#=========================================================================================================================
# get grass help (reference)
processing.alghelp("grass7:r.what.points")
# Ostroht_DTM
processing.runalg("grass7:r.what.points",DTM,
                  Ostrohr_spatial,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
                  -1,0.0001,Ostrohr_DTM)
# Ostrohr_Felsoberflaeche                  
processing.runalg("grass7:r.what.points",Felsoberflaeche,
                  Ostrohr_spatial,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
                  -1,0.0001,Ostrohr_Felsoberflaeche)
                  
#=========================================================================================================================
# join of grass results using panda
# result: merge_sel
#=========================================================================================================================
#-------------------------------------------------------------------------------------------------------------------------
# import dataframe
# result:  Ostrohr_DTM_df &  Ostrohr_Felsoberflaeche_df                
#-------------------------------------------------------------------------------------------------------------------------
Ostrohr_DTM_df  = pd.read_csv(Ostrohr_DTM)
Ostrohr_Felsoberflaeche_df  = pd.read_csv(Ostrohr_Felsoberflaeche)
#-------------------------------------------------------------------------------------------------------------------------
# prepare join of grass results using Panda
# result: Ostrohr_df, Ostrohr_DTM_df_sel, Ostrohr_Felsoberflaeche_df_sel
#-------------------------------------------------------------------------------------------------------------------------## create df: Ostrohr_DTM_df and Ostrohr_Felsoberflaeche_df
## prepare Ostrohr_csv
Ostrohr_df.head()
Ostrohr_df = Ostrohr_df.loc[:,["Easting", "Northing", "Elevation"]]
Ostrohr_df.head()
## prepare Ostrohr_DTM_df
Ostrohr_DTM_df.head()
Ostrohr_DTM_df_coleqtmp = [col for col in Ostrohr_DTM_df.columns if 'tmp' in col]
if len(Ostrohr_DTM_df_coleqtmp) != 1:
    print "Rename of DTM attribute did not work properly. Please check"
    exit()
Ostrohr_DTM_df_rename = Ostrohr_DTM_df.rename(columns= {Ostrohr_DTM_df_coleqtmp[0]: "DTM"})
Ostrohr_DTM_df_sel = Ostrohr_DTM_df_rename.loc[:,["easting", "northing", "DTM"]]
Ostrohr_DTM_df_sel.head()
# prepare Ostrohr_Felsoberflaeche_df
Ostrohr_Felsoberflaeche_df.head()
Ostrohr_Felsoberflaeche_df_coleqtmp = [col for col in Ostrohr_Felsoberflaeche_df.columns if 'tmp' in col]
if len(Ostrohr_Felsoberflaeche_df_coleqtmp) != 1:
    print "Rename of Felsoberflaeche_csv_coleqtmp attribute did not work properly. Please check"
    exit()
Ostrohr_Felsoberflaeche_df_rename = Ostrohr_Felsoberflaeche_df.rename(columns= {Ostrohr_Felsoberflaeche_df_coleqtmp[0]: "Felsoberflache"})
Ostrohr_Felsoberflaeche_df_sel = Ostrohr_Felsoberflaeche_df_rename.loc[:,["easting", "northing", "Felsoberflache"]]
Ostrohr_Felsoberflaeche_df_sel.head()
#-------------------------------------------------------------------------------------------------------------------------
# join of grass results using Panda
# reuslt: merge_final
#-------------------------------------------------------------------------------------------------------------------------
## join DTM to Ostrohr_df
merge_Ostrohr_DTM= pd.merge(Ostrohr_df, Ostrohr_DTM_df_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"])
merge_Ostrohr_DTM.head()
merge_Ostrohr_DTM.columns
## join Felsoberfläche to merge_Ostrohr_DTM
merge_final = pd.merge(merge_Ostrohr_DTM, Ostrohr_Felsoberflaeche_df_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"])
merge_final.head()
merge_final.columns
#-------------------------------------------------------------------------------------------------------------------------
# clean up join of grass results using Panda: Define columns that should be kept for following analysis
# result: merge_sel
#-------------------------------------------------------------------------------------------------------------------------
merge_sel = merge_final.loc[:,["Easting", "Northing", "Elevation", "DTM", "Felsoberflache"]]
merge_sel.head()

#=========================================================================================================================
# calculate "delta_FelsoberflacheZCoord"
#=========================================================================================================================
merge_sel['delta_FelsoberflacheZCoord'] = merge_sel.Felsoberflache - merge_sel.Elevation
merge_sel.head()


#=========================================================================================================================
# calculate "BoreClass"
#=========================================================================================================================
Th = 13 # Tunnel height
# BC1
merge_sel.loc[merge_sel['Felsoberflache'] <= merge_sel['Elevation']-float(Th)/float(100)*float(75), 'BoreClass'] = 'BC1'
# BC2
merge_sel.loc[(merge_sel['Felsoberflache'] > merge_sel['Elevation']- float(Th)/float(100)*float(75)) & 
              (merge_sel['Felsoberflache'] < merge_sel['Elevation']+ Th/float(2) +1.5), 'BoreClass'] = 'BC2'
# BC3
merge_sel.loc[merge_sel['Felsoberflache'] >= merge_sel['Elevation']+ Th/float(2) +1.5, 'BoreClass'] = 'BC3'
#merge_sel.head()
#merge_sel.tail()
#merge_sel.loc[:,["delta_FelsoberflacheZCoord","BoreClass"]]
#merge_sel.loc[merge_sel["delta_FelsoberflacheZCoord"].idxmax()]
#merge_sel.loc[merge_sel["delta_FelsoberflacheZCoord"].idxmin()]
#merge_sel["BoreClass"].value_counts()
merge_sel.to_csv("TunnelGIS.Rheintunnel/WORK/TunnelVariables_new.csv", sep=",")

#=========================================================================================================================
# calculate volume of tunnel between two axis points
#=========================================================================================================================
## prepare "Area1" field
merge_sel["Area1"] = np.random.randint(0,100, len(merge_sel.index))
## prepare "Area2" field
merge_sel["Area2"] = np.random.randint(0,100, len(merge_sel.index))  
## prepare "Distanz" field
merge_sel["Distanz"] = ""
merge_sel["Distanz"] = np.nan
## prepare "Area1_mean_dist" field
merge_sel["Area1_mean_dist"] = ""
merge_sel["Area1_mean_dist"] = np.nan
## prepare "Area2_mean_dist" field
merge_sel["Area2_mean_dist"] = ""
merge_sel["Area2_mean_dist"] = np.nan
## Calculate "Distanz", "Area1_mean_dist" and "Area2_mean_dist"
n = 0
for i in range(len(merge_sel.index)-1):
    nn= n+1
    print(n, nn)
    merge_sel["Distanz"].iloc[n] = ((merge_sel["Xcoord"].iloc[nn]-merge_sel["Xcoord"].iloc[n])**2 + (merge_sel["Ycoord"].iloc[nn]-merge_sel["Ycoord"].iloc[n])**2 + (merge_sel["Zcoord"].iloc[nn]-merge_sel["Zcoord"].iloc[n])**2)**(0.5)
    merge_sel["Area1_mean_dist"].iloc[n] = np.mean([merge_sel["Area1"].iloc[n], merge_sel["Area1"].iloc[nn]])* merge_sel["Distanz"].iloc[n] 
    merge_sel["Area2_mean_dist"].iloc[n] = np.mean([merge_sel["Area2"].iloc[n], merge_sel["Area2"].iloc[nn]])* merge_sel["Distanz"].iloc[n] 
    n = n+1
merge_sel.head()

#merge_sel.to_csv("TunnelGIS.Rheintunnel/WORK/TunnelVariables2.csv", sep=",")







