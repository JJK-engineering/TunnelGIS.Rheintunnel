# routine for grass v.to.points from pyqgis

# example
Tunnel = QgsVectorLayer("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1.shp","OstrohrLine","ogr")
processing.runalg("grass7:v.to.points",Tunnel,"2",1,True,"2603510,2624270,1260650,1274890",-1,0.0001,0,None)
