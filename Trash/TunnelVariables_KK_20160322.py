# routine for grass v.to.points from pyqgis

# list attribute names
features	=	LineTest.getFeatures()
f	=	features.next()
[c.name()	for	c	in	f.fields().toList()]

# get grass help
processing.alghelp("grass7:r.what.points")

# Name of imported geographic input files for grass input
Felstiefe = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Felstiefe.tif"
DTM = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/swissalti3dgeotifflv03-5m/swissALTI3D_.tif"
Felsoberflaeche = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Felsisohypsen-raster.tif"
OstrohrR1_csv = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1_csv.shp"

# Name of new shapefile for grass output
OstrohrR1_Felstiefe = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_Felstiefe.csv"
OstrohrR1_DTM = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_DTM.csv"
OstrohrR1_Felsoberflaeche = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_Felsoberflaeche.csv"


# set grass function
processing.runalg("grass7:r.what.points",Felstiefe,
                  OstrohrR1_csv,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
                  -1,0.0001,OstrohrR1_Felstiefe)
                          
processing.runalg("grass7:r.what.points",DTM,
                  OstrohrR1_csv,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
                  -1,0.0001,OstrohrR1_DTM)
                  
processing.runalg("grass7:r.what.points",Felsoberflaeche,
                  OstrohrR1_csv,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
                  -1,0.0001,OstrohrR1_Felsoberflaeche)

# Join results using Panda
import pandas as pd

OstrohrR1_csv = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/2017-03-19.OstrohrR1.csv")
OstrohrR1_Felstiefe_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1_Felstiefe.csv")
OstrohrR1_DTM_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1_DTM.csv")
OstrohrR1_Felsoberflaeche_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1_Felsoberflaeche.csv")

OstrohrR1_csv.head()
OstrohrR1_csv = OstrohrR1_csv.loc[:,["Xcoord", "Ycoord", "Zcoord"]]
OstrohrR1_csv.head()

OstrohrR1_Felstiefe_csv.head()
OstrohrR1_Felstiefe_csv_coleqtmp = [col for col in OstrohrR1_Felstiefe_csv.columns if 'tmp' in col]
if len(OstrohrR1_Felstiefe_csv_coleqtmp) != 1:
    print "Rename of Felstiefe attribute did not work properly. Please check"
    exit()
OstrohrR1_Felstiefe_csv_rename = OstrohrR1_Felstiefe_csv.rename(columns= {OstrohrR1_Felstiefe_csv_coleqtmp[0]: "Felstiefe"})
OstrohrR1_Felstiefe_csv_sel = OstrohrR1_Felstiefe_csv_rename.loc[:,["easting", "northing", "Felstiefe"]]
OstrohrR1_Felstiefe_csv_sel.head()

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

merge_sel.to_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/TunnelVariables.csv", sep=",")


