# routine for grass v.to.points from pyqgis

# example

# set extent
xmin	=	ext.xMinimum()
ymin	=	ext.yMinimum()
xmax	=	ext.xMaximum()
ymax	=	ext.yMaximum()
LineTestBox	=	"%s,%s,%s,%s"	%	(xmin,xmax,ymin,ymax)

# import shapefile
Tunnel_Line = QgsVectorLayer("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1.shp","OstrohrLine","ogr")

# get grass help
processing.alghelp("grass7:r.what.points")

# set grass function
Tunnel_Point = QgsVectorLayer("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1_Point.shp","OstrohrLine","ogr")

processing.runalg("grass7:v.to.points",Tunnel_Line,"2",1,True,"2603510,2624270,1260650,1274890",-1,0.0001,0,Tunnel_Point)
