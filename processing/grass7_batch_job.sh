g.proj -c proj4="+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs"
v.in.ogr min_area=0.0001 snap=-1 input="/home/kaelin_joseph/TunnelGIS.Rheintunnel/WORK" layer=OstrohrR1 output=tmp1489857645972 --overwrite -o
g.region n=1274890 s=1260650 e=2624270 w=2603510 res=100
v.to.points  input="tmp1489857645972" dmax="2" use=vertex -i output=output1825af211ca04348b4aaa285d53d2ed5 --overwrite
v.out.ogr -s -e input=output1825af211ca04348b4aaa285d53d2ed5 type=auto output="/tmp/processing9bec029e0d1843309195d1865678c52c/5237cc50f9dc4f78b52d05182831caa3" format=ESRI_Shapefile output_layer=output --overwrite
exit