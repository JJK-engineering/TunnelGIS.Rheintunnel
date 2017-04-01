# routine for grass v.to.points from pyqgis
#   to analyze GIS data along a tunnel axis
Tunnel_Line = QgsVectorLayer("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1.shp","OstrohrLine","ogr")


# list attribute names (for checking)
features	=	Tunnel_Line.getFeatures()
f	=	features.next()
[c.name()	for	c	in	f.fields().toList()]

# get grass help (reference)
processing.alghelp("grass7:r.what.points")

# set name of geographic input files for grass input
#   data for tunnel axis (e.g. OstrphrR1) must be available as .csv and as .shp
#   conversion from .csv to .shp should be made here to make sure up-t0-data                          Todo KLK
Felstiefe = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Felstiefe.tif"
DTM = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/swissalti3dgeotifflv03-5m/swissALTI3D_.tif"
Felsoberflaeche = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Felsisohypsen-raster.tif"
OstrohrR1 = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1.shp"

# name of files for grass output
OstrohrR1_Felstiefe = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_Felstiefe.csv"
OstrohrR1_DTM = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_DTM.csv"
OstrohrR1_Felsoberflaeche = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_Felsoberflaeche.csv"

# use grass functions to get raster values for points along axis and write to .csv files
processing.runalg("grass7:r.what.points",DTM,
                  OstrohrR1,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
                  -1,0.0001,OstrohrR1_DTM)
                  
processing.runalg("grass7:r.what.points",Felsoberflaeche,
                  OstrohrR1,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
                  -1,0.0001,OstrohrR1_Felsoberflaeche)

import pandas as pd
import numpy as np
import geopandas as gpd
import shapely as sp

# convert the csv file to a DataFrame
data = DataFrame.from_csv('enwest2015_1.csv', index_col=False)
# extract the geometry from the DataFrame
points = [Point(row['lon'], row['lat']) for key, row in data.iterrows()]
#convert the DataFrame to a GeoDataFrame 
geo_df = GeoDataFrame(data,geometry=points)
# save the resulting shapefile
geo_df.to_file('enwest2015_1.shp', driver='ESRI Shapefile')

# join grass results using Panda
OstrohrR1_csv = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/2017-03-19.OstrohrR1.csv")
OstrohrR1_Felstiefe_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1_Felstiefe.csv")
OstrohrR1_DTM_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1_DTM.csv")
OstrohrR1_Felsoberflaeche_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1_Felsoberflaeche.csv")

# extract the geometry from the DataFrame
OstrohrR1_spatial = OstrohrR1_csv
OstrohrR1_spatial_points = [sp.geometry.Point(row['Xcoord'], row['Ycoord']) for key, row in OstrohrR1_spatial.iterrows()]
OstrohrR1_spatial_points[1]
#convert the DataFrame to a GeoDataFrame 
OstrohrR1_spatial = gpd.GeoDataFrame(OstrohrR1_spatial,geometry=OstrohrR1_spatial_points)
OstrohrR1_spatial.head()
OstrohrR1_csv.head()
# save the resulting shapefile
OstrohrR1_spatial.to_file('/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1.shp', driver='ESRI Shapefile')

# select attributes to be shown in data frame
OstrohrR1_csv.head()
OstrohrR1_csv = OstrohrR1_csv.loc[:,["Xcoord", "Ycoord", "Zcoord"]]
OstrohrR1_csv.head()

OstrohrR1_DTM_csv.head()
OstrohrR1_DTM_csv_coleqtmp = [col for col in OstrohrR1_DTM_csv.columns if 'tmp' in col]
if len(OstrohrR1_DTM_csv_coleqtmp) != 1:
    print "Rename of Felstiefe attribute did not work properly. Please check"
    exit()
OstrohrR1_DTM_csv_rename = OstrohrR1_DTM_csv.rename(columns= {OstrohrR1_DTM_csv_coleqtmp[0]: "DTM"})
OstrohrR1_DTM_csv_sel = OstrohrR1_DTM_csv_rename.loc[:,["easting", "northing", "DTM"]]
OstrohrR1_DTM_csv_sel.head()

OstrohrR1_Felsoberflaeche_csv.head()
OstrohrR1_Felsoberflaeche_csv_coleqtmp = [col for col in OstrohrR1_Felsoberflaeche_csv.columns if 'tmp' in col]
if len(OstrohrR1_Felsoberflaeche_csv_coleqtmp) != 1:
    print "Rename of Felstiefe attribute did not work properly. Please check"
    exit()
OstrohrR1_Felsoberflaeche_csv_rename = OstrohrR1_Felsoberflaeche_csv.rename(columns= {OstrohrR1_Felsoberflaeche_csv_coleqtmp[0]: "Felsoberflache"})
OstrohrR1_Felsoberflaeche_csv_sel = OstrohrR1_Felsoberflaeche_csv_rename.loc[:,["easting", "northing", "Felsoberflache"]]
OstrohrR1_Felsoberflaeche_csv_sel.head()

merge_felstiefe = pd.merge(OstrohrR1_csv, OstrohrR1_Felstiefe_csv_sel, 
                 left_on = ["Xcoord","Ycoord"], 
                 right_on = ["easting","northing"])
merge_felstiefe.head()
merge_felstiefe.columns
                 
merge_felstiefe_dtm = pd.merge(merge_felstiefe, OstrohrR1_DTM_csv_sel, 
                 left_on = ["Xcoord","Ycoord"], 
                 right_on = ["easting","northing"])
merge_felstiefe_dtm.head()
merge_felstiefe_dtm.columns
                 
merge_felstiefe_dtm_felsoberflaeche = pd.merge(merge_felstiefe_dtm, OstrohrR1_Felsoberflaeche_csv_sel, 
                 left_on = ["Xcoord","Ycoord"], 
                 right_on = ["easting","northing"])
merge_felstiefe_dtm_felsoberflaeche.head()
merge_felstiefe_dtm_felsoberflaeche.columns


merge_sel = merge_felstiefe_dtm_felsoberflaeche.loc[:,["Xcoord", "Ycoord", "Zcoord", "Felstiefe", "DTM", "Felsoberflache"]]
merge_sel.head()

merge_sel['delta_FelsoberflacheZCoord'] = merge_sel.Felsoberflache - merge_sel.Zcoord
merge_sel.head()

#merge_sel.to_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/TunnelVariables.csv", sep=",")

reuslt = []

merge_sel["Area1"] = np.random.randint(0,100, len(merge_sel.index))
merge_sel["Area2"] = np.random.randint(0,100, len(merge_sel.index))  

merge_sel["Distanz"] = ""
merge_sel["Distanz"] = np.nan

merge_sel["Area1_mean_dist"] = ""
merge_sel["Area1_mean_dist"] = np.nan

merge_sel["Area2_mean_dist"] = ""
merge_sel["Area2_mean_dist"] = np.nan

n = 0
for i in range(len(merge_sel.index)-1):
    nn= n+1
    print(n, nn)
    merge_sel["Distanz"].iloc[n] = ((merge_sel["Xcoord"].iloc[nn]-merge_sel["Xcoord"].iloc[n])**2 + (merge_sel["Ycoord"].iloc[nn]-merge_sel["Ycoord"].iloc[n])**2 + (merge_sel["Zcoord"].iloc[nn]-merge_sel["Zcoord"].iloc[n])**2)**(0.5)
    merge_sel["Area1_mean_dist"].iloc[n] = np.mean([merge_sel["Area1"].iloc[n], merge_sel["Area1"].iloc[nn]])* merge_sel["Distanz"].iloc[n] 
    merge_sel["Area2_mean_dist"].iloc[n] = np.mean([merge_sel["Area2"].iloc[n], merge_sel["Area2"].iloc[nn]])* merge_sel["Distanz"].iloc[n] 
    n = n+1
    
merge_sel.head()

merge_sel.to_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/TunnelVariables2.csv", sep=",")



