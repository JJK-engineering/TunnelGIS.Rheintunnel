# get grass help (reference)
processing.alghelp("grass7:r.what.points")

# import library
import pandas as pd
import numpy as np
import geopandas as gpd
import shapely as sp

# set of input
DTM = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/swissalti3dgeotifflv03-5m/swissALTI3D_.tif"
Felsoberflaeche = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Felsisohypsen-raster.tif"
Ostrohr_csv = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR2.csv"

# name of output
Ostrohr_spatial ='/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR2.shp'
Ostrohr_DTM = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Ostrohr_DTM.csv"
Ostrohr_Felsoberflaeche = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Ostrohr_Felsoberflaeche.csv"

# create *.shp from *.csv
# http://gis.stackexchange.com/questions/197825/how-to-convert-multiple-csv-files-to-shp-using-python-and-no-arcpy
Ostrohr_df = pd.read_csv(Ostrohr_csv)
Ostrohr_df.dropna(how = "all").head()
Ostrohr_df = Ostrohr_df.dropna(how = "all")
Ostrohr_df = Ostrohr_df.drop(Ostrohr_df.index[len(Ostrohr_df)-1])
Ostrohr_spatial = Ostrohr_df
Ostrohr_spatial_points = [sp.geometry.Point(row['Easting'], row['Northing']) for key, row in Ostrohr_spatial.iterrows()]
Ostrohr_crs = {'init': 'epsg:2056'}
Ostrohr_spatial = gpd.GeoDataFrame(Ostrohr_spatial,geometry=Ostrohr_spatial_points, crs = Ostrohr_crs)
Ostrohr_spatial.to_file('/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR2.shp', driver='ESRI Shapefile') 
#Ostrohr_spatial.crs
#Ostrohr_spatial.plot()
#Ostrohr_spatial.tail()


# use grass functions to get raster values for points along axis and write to .csv files
processing.runalg("grass7:r.what.points",DTM,
                  Ostrohr_spatial,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
                  -1,0.0001,Ostrohr_DTM)
                  
processing.runalg("grass7:r.what.points",Felsoberflaeche,
                  Ostrohr_spatial,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
                  -1,0.0001,Ostrohr_Felsoberflaeche)


# join grass results using Panda
Ostrohr_DTM_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Ostrohr_DTM.csv")
Ostrohr_Felsoberflaeche_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Ostrohr_Felsoberflaeche.csv")

# select attributes to be shown in data frame
Ostrohr_df.head()
Ostrohr_df = Ostrohr_df.loc[:,["Easting", "Northing", "Elevation"]]
Ostrohr_df.head()

Ostrohr_DTM_csv.head()
Ostrohr_DTM_csv_coleqtmp = [col for col in Ostrohr_DTM_csv.columns if 'tmp' in col]
if len(Ostrohr_DTM_csv_coleqtmp) != 1:
    print "Rename of DTM attribute did not work properly. Please check"
    exit()
Ostrohr_DTM_csv_rename = Ostrohr_DTM_csv.rename(columns= {Ostrohr_DTM_csv_coleqtmp[0]: "DTM"})
Ostrohr_DTM_csv_sel = Ostrohr_DTM_csv_rename.loc[:,["easting", "northing", "DTM"]]
Ostrohr_DTM_csv_sel.head()

Ostrohr_Felsoberflaeche_csv.head()
Ostrohr_Felsoberflaeche_csv_coleqtmp = [col for col in Ostrohr_Felsoberflaeche_csv.columns if 'tmp' in col]
if len(Ostrohr_Felsoberflaeche_csv_coleqtmp) != 1:
    print "Rename of Felsoberflaeche_csv_coleqtmp attribute did not work properly. Please check"
    exit()
Ostrohr_Felsoberflaeche_csv_rename = Ostrohr_Felsoberflaeche_csv.rename(columns= {Ostrohr_Felsoberflaeche_csv_coleqtmp[0]: "Felsoberflache"})
Ostrohr_Felsoberflaeche_csv_sel = Ostrohr_Felsoberflaeche_csv_rename.loc[:,["easting", "northing", "Felsoberflache"]]
Ostrohr_Felsoberflaeche_csv_sel.head()
                 
merge1= pd.merge(Ostrohr_df, Ostrohr_DTM_csv_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"])
merge1.head()
merge1.columns
                 
merge_final = pd.merge(merge1, Ostrohr_Felsoberflaeche_csv_sel, 
                 left_on = ["Easting","Northing"], 
                 right_on = ["easting","northing"])
merge_final.head()
merge_final.columns

merge_sel = merge_final.loc[:,["Easting", "Northing", "Elevation", "DTM", "Felsoberflache"]]
merge_sel.head()

merge_sel['delta_FelsoberflacheZCoord'] = merge_sel.Felsoberflache - merge_sel.Elevation
merge_sel.head()

Th = 13

merge_sel.loc[merge_sel['Felsoberflache'] < merge_sel['Elevation']-float(Th)/float(100)*float(75), 'BoreClass'] = 'BC1'
merge_sel.loc[(merge_sel['Felsoberflache'] >= merge_sel['Elevation']- float(Th)/float(100)*float(75)) & (merge_sel['Felsoberflache'] >=  merge_sel['Elevation']+ Th/float(2) +1.5), 'BoreClass'] = 'BC2'
merge_sel.loc[merge_sel['Felsoberflache'] >  merge_sel['Elevation']+ Th/float(2) +1.5, 'BoreClass'] = 'BC3'
merge_sel.head()
merge_sel.tail()
merge_sel.loc[:,["delta_FelsoberflacheZCoord","BoreClass"]]
merge_sel.loc[merge_sel["delta_FelsoberflacheZCoord"].idxmax()]
merge_sel.loc[merge_sel["delta_FelsoberflacheZCoord"].idxmin()]
merge_sel["BoreClass"].value_counts()

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




