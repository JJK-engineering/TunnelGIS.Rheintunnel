<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" version="1.0" encoding="UTF-8" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/>
  <xsl:decimal-format name="extent" grouping-separator="'"/>
  <xsl:template match="/">
    <html>
      <head>
        <style type="text/css">
          body {
            font-family: arial, "lucida console", sans-serif;
            font-size: 10px;
          }
          h1 {
            font-size: 16px;
          }
          table {
            border-width: 1px 1px 1px 1px;
            border-spacing: 1px;
            border-style: outset outset outset outset;
            border-color: gray gray gray gray;
            border-collapse: separate;
            background-color: white;
          }
          table th {
            border-width: 1px 1px 1px 1px;
            padding: 0px 0px 0px 0px;
            border-style: inset inset inset inset;
            border-color: white white white white;
            background-color: white;
          }
          table td {
            border-width: 1px 1px 1px 1px;
            padding: 0px 0px 0px 0px;
            border-style: inset inset inset inset;
            border-color: white white white white;
            background-color: white;
          }
          th {
            font-size: 12px;
          }
          .source {
            font-size: 14px;
            font-weight: bold;
          }
          .dataset {
            font-weight: bold;
          }
          .listOfExporterRaster {
          	font-size: 12px;
          }
          .total {
          	font-size: 12px;
          }
        </style>
      </head>
    <body>
      <h1>Delivery Receipt of Terrain to Raster Export</h1>
      <table  >
        <tr>
          <th rowspan="2">Item</th>
          <th rowspan="2" colspan="2">Value</th>
        </tr>
        <tr>
        	<xsl:call-template name="data" />
        </tr>
      </table>
    </body>
    </html>
  </xsl:template>
  
  <!-- *************************************************************************************** -->
  <!-- xslt templates: -->
  <!-- main template: 
        1. generate main tree structure in xslt document and 
        2. calls subtemplate matching elements in xml-tree -->
  <xsl:template name="data">
  	<tr class="inputterrain">
	  	<td colspan="1">Inputterrain</td>
	  	<xsl:call-template name="inputterrain" />
	</tr>
	<tr class="terrainSpatialReference">
	  	<td colspan="1">Spatial Reference Terrain</td>
	  	<xsl:call-template name="terrainSpatialReference" />
	</tr>
	<tr class="terrainLinearUnit">
	  	<td colspan="1">Linear Unit Terrain</td>
	  	<xsl:call-template name="terrainLinearUnit" />
	</tr>
	<tr class="extentAsString">
	  	<td colspan="1">Export Perimeter Extent (xmin ymin xmax ymax)</td>
	  	<xsl:call-template name="extentAsString" />
	</tr>
	<tr class="outputRasterFormat">
	  	<td colspan="1">OutputRasterFormat</td>
	  	<xsl:call-template name="outputRasterFormat" />
	</tr>
	<tr class="cellsize">
	  	<td colspan="1">Cellsize</td>
	  	<xsl:call-template name="cellsize" />
	</tr>
	<tr class="interpolationMethod">
	  	<td colspan="1">Interpolation Method</td>
	  	<xsl:call-template name="interpolationMethod" />
	</tr>
	<tr class="listOfExporterRaster">
	  	<td colspan="1">List of Exported Raster:</td>
	  	<td colspan="1">Name of Exported Raster</td>
	  	<td colspan="1">Size of Exported Raster [MB]</td>
	  	<xsl:call-template name="ListOfExportedRaster" />
	</tr>
	<tr class="exportedRasterStatistics">
	  	<td colspan="1" >Total</td>
	  	<xsl:call-template name="exportedRasterStatistics" />
	</tr>	
  </xsl:template>

  <!-- *************************************************************************************** -->
  <!--subtemplates -->
  
  <xsl:template name="inputterrain">
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/terrain">
        <td colspan="2"><xsl:value-of select="@name" /></td>
    </xsl:for-each>
  </xsl:template>
  
  <xsl:template name="terrainSpatialReference">
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/terrainSpatialReference">
        <td colspan="2"><xsl:value-of select="@name" /></td>
    </xsl:for-each>
  </xsl:template>
  
  <xsl:template name="terrainLinearUnit">
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/terrain_linear_unit">
        <td colspan="2"><xsl:value-of select="@name" /></td>
    </xsl:for-each>
  </xsl:template>
  
  <xsl:template name="extentAsString">
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/extentAsString">
        <td colspan="2"><xsl:value-of select="@name" /></td>
    </xsl:for-each>
  </xsl:template>  
  
  <xsl:template name="outputRasterFormat">
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/output_raster_format">
        <td colspan="2"><xsl:value-of select="@name" /></td>
    </xsl:for-each>
  </xsl:template>
  
  <xsl:template name="cellsize">
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/cellsize">
        <td colspan="2"><xsl:value-of select="@name" /></td>
    </xsl:for-each>
  </xsl:template>
  
  <xsl:template name="interpolationMethod">
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/interpolation_method">
        <td colspan="2"><xsl:value-of select="@name" /></td>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="ListOfExportedRaster">
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/exportedRasters/exportedRaster">
    	<tr>
        	<td/>
        	<td colspan="1"><xsl:value-of select="@name" /></td>
        	<td colspan="1"><xsl:value-of select="@size" /></td>
        </tr>
    </xsl:for-each>
  </xsl:template>
  
  <xsl:template name="exportedRasterStatistics">
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/exportedRasterStatistics">
        <td colspan="1"><xsl:value-of select="@number" /></td>
    </xsl:for-each>
    <xsl:for-each select="aggregatedDelivery/datasets/dataset/deliveries/delivery/exportedRasterStatistics">
    	<td colspan="1"><xsl:value-of select="@size" /></td>
    </xsl:for-each>
  </xsl:template>
  
</xsl:stylesheet>