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
#processing.runalg("grass7:r.what.points",Felstiefe,
#                  OstrohrR1_csv,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
#                  -1,0.0001,OstrohrR1_Felstiefe)
#                          
#processing.runalg("grass7:r.what.points",DTM,
#                  OstrohrR1_csv,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
#                  -1,0.0001,OstrohrR1_DTM)
#                  
#processing.runalg("grass7:r.what.points",Felsoberflaeche,
#                  OstrohrR1_csv,"NA",",",500, True,False,False,False,False,"2603510.0,2624270.0,1260650.0,1274890.0",
#                  -1,0.0001,OstrohrR1_Felsoberflaeche)


# Join results using Panda
import pandas as pd

OstrohrR1_csv = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/2017-03-19.OstrohrR1.csv")
OstrohrR1_Felstiefe_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_Felstiefe.csv")
OstrohrR1_DTM_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_DTM.csv")
OstrohrR1_Felsoberflaeche_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_Felsoberflaeche.csv")

OstrohrR1_csv.head()
OstrohrR1_csv.columns
OstrohrR1_csv = OstrohrR1_csv.loc[:,["Xcoord", "Ycoord", "Zcoord"]]
OstrohrR1_csv.head()

OstrohrR1_Felstiefe_csv.head()
OstrohrR1_Felstiefe_csv.columns
OstrohrR1_Felstiefe_csv = OstrohrR1_Felstiefe_csv.loc[:,["easting", "northing", "tmp14900475028728"]]
OstrohrR1_Felstiefe_csv.head()

OstrohrR1_DTM_csv.head()
OstrohrR1_DTM_csv.columns
OstrohrR1_DTM_csv = OstrohrR1_DTM_csv.loc[:,["easting", "northing", "tmp1490047503330"]]
OstrohrR1_DTM_csv.head()

OstrohrR1_Felsoberflaeche_csv.head()
OstrohrR1_Felsoberflaeche_csv.columns
OstrohrR1_Felsoberflaeche_csv = OstrohrR1_Felsoberflaeche_csv.loc[:,["easting", "northing", "tmp14900475037932"]]
OstrohrR1_Felsoberflaeche_csv.head()

merge_felstiefe = pd.merge(OstrohrR1_csv, OstrohrR1_Felstiefe_csv, 
                 left_on = ["Xcoord","Ycoord"], 
                 right_on = ["easting","northing"])
merge_felstiefe.head()
merge_felstiefe.columns
                 
merge_felstiefe_dtm = pd.merge(merge_felstiefe, OstrohrR1_DTM_csv, 
                 left_on = ["Xcoord","Ycoord"], 
                 right_on = ["easting","northing"])
merge_felstiefe_dtm.head()
merge_felstiefe_dtm.columns
                 
merge_felstiefe_dtm_felsoberflaeche = pd.merge(merge_felstiefe_dtm, OstrohrR1_Felsoberflaeche_csv, 
                 left_on = ["Xcoord","Ycoord"], 
                 right_on = ["easting","northing"])
merge_felstiefe_dtm_felsoberflaeche.head()
merge_felstiefe_dtm_felsoberflaeche.columns


merge_sel = merge_felstiefe_dtm_felsoberflaeche.loc[:,["Xcoord", "Ycoord", "Zcoord", "tmp14900475028728", "tmp1490047503330", "tmp14900475037932"]]
merge_sel.head()

list(merge_sel)
merge_sel.columns
merge_rename1 = merge_sel.rename(columns= {"tmp14900475028728": "Felstiefe"})
list(merge_rename1)
merge_rename2 = merge_rename1.rename(columns= {"tmp1490047503330": "DTM"})
list(merge_rename2)
merge_rename3 = merge_rename2.rename(columns= {"tmp14900475037932": "Felsoberflache"})
list(merge_rename3)

merge_rename3.head()
merge_rename3.columns

merge_rename3['delta_ZCoordFelstiefe'] = merge_rename3.Zcoord - merge_rename3.Felstiefe
merge_rename3.head()


merge_rename3.to_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/Felstiefe.csv", sep="\t")
