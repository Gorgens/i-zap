#exec(open("/sysroot/home/eric/Github/i_zap/01_delimitacao/00delimitacao.py").read())

import processing
import subprocess
import os
from osgeo import ogr

### Define variáveis do ambiente  ------------------------------

VAZPATH = '/sysroot/home/eric/Documentos/Base de dados ZAP/zip 2406 reg vazao/'
#VAZPATH = 'C:/Users/gorge/Documents/GIS DataBase/izap input/'
VAZFILE = '2406_JQ_Igam_UFV_reg_vazao_lin.shp'

OTTOPATH = '/sysroot/home/eric/Documentos/Base de dados ZAP/zip 0102 ottobacias/'
#OTTOPATH = 'C:/Users/gorge/Documents/GIS DataBase/izap input/'
OTTOFILE = '0102_jq_otto_bacia_pol.shp'

OUTPATH = '/sysroot/home/eric/Github/i_zap/01_delimitacao/'
#OUTPATH = 'C:/Users/gorge/Documents/GitHub/i_zap/01_delimitacao/'
CRS = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId)
CODRIO = "7582998"


### Importa e ajusta a camada da rede hídrica -----------------------------

hidrico = QgsVectorLayer(VAZPATH+VAZFILE, "Reg Vazao", 'ogr')
hidrico.setCrs(CRS)
#print(vazao.dataProvider().encoding())

hidrico.dataProvider().setEncoding(u'ISO-8859-1')


### Filtra o rio de interesse ---------------

hidrico.setSubsetString("cocursodag LIKE '"+str(CODRIO)+"%'")
#QgsProject.instance().addMapLayer(hidrico)

QgsVectorFileWriter.writeAsVectorFormat(hidrico, OUTPATH+'hidricoInteresse.shp', "utf-8", hidrico.crs(), "ESRI Shapefile")

### Filtra ottobacias ----------------------------------------

otto = QgsVectorLayer(OTTOPATH+OTTOFILE, "Ottobacias", 'ogr')
otto.setCrs(CRS)

otto.setSubsetString("cocursodag LIKE '"+str(CODRIO)+"%'")
#QgsProject.instance().addMapLayer(otto)

QgsVectorFileWriter.writeAsVectorFormat(otto, OUTPATH+'ottoInteresse.shp', "utf-8", otto.crs(), "ESRI Shapefile")

### Criar limites da bacia
(processing.run("native:dissolve", {
    'INPUT':OUTPATH+'ottoInteresse.shp',
    'FIELD':[],
    'OUTPUT':OUTPATH+'limiteBacia.shp'}))


##QgsProject.instance().addMapLayer(dtmlayer)
#extent = dtmlayer.extent()
#xmin = extent.xMinimum()
#xmax = extent.xMaximum()
#ymin = extent.yMinimum()
#ymax = extent.yMaximum()
#coords = "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax)