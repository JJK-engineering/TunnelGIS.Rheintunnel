# python setup for qgis processing

import sys
from qgis.core import *
# need qgis,gui ?
#from qgis.gui import *
# need PyQt4.QtCore ?
#from PyQt4.QtCore import *
from PyQt4.QtGui import *

# what does True refer to below ?
app = QApplication([], True)
QgsApplication.setPrefixPath("/usr", True)
# /usr correct?
#QgsApplication.setPrefixPath(qgis_path, True)
QgsApplication.initQgis()

sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *

#why is this still needed
import processing
