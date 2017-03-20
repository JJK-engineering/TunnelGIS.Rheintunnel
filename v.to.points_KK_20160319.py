# routine for grass v.to.points from pyqgis

# import shapefile
Tunnel_Line = QgsVectorLayer("/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1.shp","OstrohrLine","ogr")

# list attribute names
features	=	LineTest.getFeatures()
f	=	features.next()
[c.name()	for	c	in	f.fields().toList()]

# set extent
ext	=	Tunnel_Line.extent()
xmin	=	ext.xMinimum()
ymin	=	ext.yMinimum()
xmax	=	ext.xMaximum()
ymax	=	ext.yMaximum()
TunnelExt	=	"%s,%s,%s,%s"	%	(xmin,xmax,ymin,ymax)

# get grass help
processing.alghelp("grass7:r.what.points")

# create new shapefile for grass output
Tunnel_Point = "/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK/OstrohrR1_Point.shp"

# set grass function
processing.runalg("grass7:v.to.points",Tunnel_Line,"2",1,True,"2603510,2624270,1260650,1274890",-1,0.0001,0,None)
processing.runalg("grass7:v.to.points",Tunnel_Line,"2",1,True,TunnelExt,-1,0.0001,0,Tunnel_Point)
