g.proj -c proj4="+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs"
r.external input="WORK/Felsisohypsen-raster.tif" band=1 output=tmp1492421149394 --overwrite -o
v.in.ogr min_area=0.0001 snap=-1 input="WORK" layer=Ostroehre.Alignment.R2 output=tmp1492421149395 --overwrite -o
g.region n=1274890.0 s=1260650.0 e=2624270.0 w=2603510.0 res=20.7807807808
r.what  map="tmp1492421149394" points="tmp1492421149395" null_value="NA" separator="," cache="500" -n > WORK/Ostroehre.RockSurface.R2.csv --overwrite
exit