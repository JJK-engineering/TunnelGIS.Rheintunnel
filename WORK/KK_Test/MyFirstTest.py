#from qgis.core import *
#
## supply path to qgis install location
#QgsApplication.setPrefixPath("/path/to/qgis/installation", True)
#
## create a reference to the QgsApplication, setting the
## second argument to False disables the GUI
#qgs = QgsApplication([], False)

# http://gis.stackexchange.com/questions/129513/how-can-i-access-processing-with-python
# Prepare the environment
import sys
from qgis.core import *
from PyQt4.QtGui import *
app = QApplication([])
QgsApplication.setPrefixPath("/usr", True)
QgsApplication.initQgis()

# Prepare processing framework 
sys.path.append('/usr/share/qgis/python/plugins') # Folder where Processing is located
from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *

# Run the algorithm
LineTest = QgsVectorLayer('/home/katharina/Desktop/TunnelGis_KK/TestFiles/Line.shp', 'line', 'ogr')

# list attribute names
features	=	LineTest.getFeatures()
f	=	features.next()
[c.name()	for	c	in	f.fields().toList()]


ext	=	LineTest.extent()
xmin	=	ext.xMinimum()
ymin	=	ext.yMinimum()
xmax	=	ext.xMaximum()
ymax	=	ext.yMaximum()
LineTestBox	=	"%s,%s,%s,%s"	%	(xmin,xmax,ymin,ymax)

# Example from Geopython Cookbook: Computing	road	slope	using	elevation
processing.runalg("grass:v.split.length",LineTest,3,\
LineTestBox,-1,0.0001,0,"/home/katharina/Desktop/TunnelGis_KK/TestFiles/SegLineTest.shp")

segRoadLyr = QgsVectorLayer("/home/katharina/Desktop/TunnelGis_KK/TestFiles/SegLineTest.shp",	\
"LineTest",	"ogr")

# Exit applications
QgsApplication.exitQgis()
QApplication.exit()

# load providers
qgs.initQgis()

# Write your code here to load some layers, use processing algorithms, etc.

# When your script is complete, call exitQgis() to remove the provider and
# layer registries from memory
qgs.exitQgis()