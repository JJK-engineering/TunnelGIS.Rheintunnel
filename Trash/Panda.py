import pandas as pd

OstrohrR1_csv = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/2017-03-19.OstrohrR1.csv")
OstrohrR1_Felstiefe_csv  = pd.read_csv("/home/kaelin_joseph/TunnelGIS.Rheintunnel/OstrohrR1_Felstiefe.csv")

OstrohrR1_csv.head()
OstrohrR1_csv = OstrohrR1_csv.loc[:,["Xcoord", "Ycoord", "Zcoord"]]
OstrohrR1_csv.head()

OstrohrR1_Felstiefe_csv.head()
OstrohrR1_Felstiefe_csv = OstrohrR1_Felstiefe_csv.loc[:,["easting", "northing", "tmp149003749668"]]
OstrohrR1_Felstiefe_csv.head()

merge = pd.merge(OstrohrR1_csv, OstrohrR1_Felstiefe_csv, 
                 left_on = ["Xcoord","Ycoord"], 
                 right_on = ["easting","northing"])
merge.head()
merge = merge.loc[:,["Xcoord", "Ycoord", "Ycoord", "tmp149003749668"]]
merge.head()

list(merge)
merge.columns
merge_rename = merge.rename(columns= {"tmp149003749668": "Felstiefe"})
merge_rename.head()
