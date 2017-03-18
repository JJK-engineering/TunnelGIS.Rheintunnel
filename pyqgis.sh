#!/bin/bash

# set environmental variables for pyqgis
export PYTHONPATH=/usr/share/qgis/python/
export LD_LIBRARY_PATH=/usr/share/qgis/python/
# adjust DISPLAY to your system environment
# "=1.0" is for GIS platform on Google Cloud Compute Engine 
export DISPLAY=:1.0
export PYTHONSTARTUP=./pyqgis.py

python
