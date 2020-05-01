#exec(open("/sysroot/home/eric/Documentos/Base de dados ZAP/slope.py").read())

import processing
import subprocess
import os
from osgeo import ogr

#DTM = 'S15W041.hgt'
arr = os.listdir('/sysroot/home/eric/Documentos/Base de dados ZAP/srtm/')

for DTM in arr:
	crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId)
	dtmlayer = QgsRasterLayer('/sysroot/home/eric/Documentos/Base de dados ZAP/srtm/'+DTM, "MDT temp")
	dtmlayer.setCrs(crs)
	#QgsProject.instance().addMapLayer(dtmlayer)
	extent = dtmlayer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	coords = "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax)

	#processing.algorithmHelp('grass7:r.slope.aspect')  # para ver os parâmetros da função r.slope.aspect
	#processing.algorithmHelp('grass7:r.resample')      # para ver os parâmetros da função r.resample
	params = {
	    'elevation' : dtmlayer,
	    'format' : 0,
	    'precision' : 0,
	    'GRASS_REGION_PARAMETER':coords,
	    'GRASS_REGION_CELLSIZE_PARAMETER':0,
	    'GRASS_RASTER_FORMAT_OPT':'',
	    'GRASS_RASTER_FORMAT_META':'',
	    'slope' : '/sysroot/home/eric/Documentos/Base de dados ZAP/slope/'+DTM[0:len(DTM)-4] + '_slope.tif',
	    #'aspect' : '/sysroot/home/eric/Documentos/Base de dados ZAP/slope/'+DTM[0:len(DTM)-4] + '_aspect.tif',
	    'pcurvature' : '/sysroot/home/eric/Documentos/Base de dados ZAP/slope/'+DTM[0:len(DTM)-4] + '_pcurv.tif',
	    'tcurvature' : '/sysroot/home/eric/Documentos/Base de dados ZAP/slope/'+DTM[0:len(DTM)-4] + '_tcurv.tif'
	}
	processing.run("grass7:r.slope.aspect", params)
	#slope = QgsRasterLayer('/sysroot/home/eric/Documentos/Base de dados ZAP/slope/'+DTM[0:len(DTM)-4] + '_slope.tif', "Slope model")
	#slope.setCrs(crs)
	#QgsProject.instance().addMapLayer(slope)
	print(DTM + ' done!')
