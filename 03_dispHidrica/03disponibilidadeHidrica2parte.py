#exec(open("/sysroot/home/eric/Github/i_zap/03_dispHidrica/03disponibilidadeHidrica2parte.py").read())

import processing
import subprocess
import os
from osgeo import ogr
import numpy as np
import re

DISP_PATH='/sysroot/home/eric/Github/i_zap/03_dispHidrica/'
LIM_PATH='/sysroot/home/eric/Github/i_zap/01_delimitacao/'
CSV = DISP_PATH+'OutorgasFelicioDosSantos.csv'
EPSG = 4326

print('Intersecting.... cobacia por outorga!')
(processing.run("native:intersection", {
    'INPUT':DISP_PATH+'outorgasBacia.shp',
    'OVERLAY':LIM_PATH+'ottoInteresse.shp',
    'INPUT_FIELDS':[],
    'OVERLAY_FIELDS':['cobacia'],
    'OVERLAY_FIELDS_PREFIX':'',
    'OUTPUT':DISP_PATH+'outorgasBaciaOtto.shp'
}))
print('Intersecting.... done!')

print('Summing.... somando vazão por cobacia!')
(processing.run("qgis:statisticsbycategories", {
    'INPUT':DISP_PATH+'outorgasBaciaOtto.shp',
    'VALUES_FIELD_NAME':'captacao',
    'CATEGORIES_FIELD_NAME':['cobacia'],
    'OUTPUT':DISP_PATH+'OttoDemanda.csv'
}))
print('Summing.... done!')

print('Joining.... Demanda com rede hidrica!')
(processing.run("native:joinattributestable", {
    'INPUT':LIM_PATH+'hidricoInteresse.shp',
    'FIELD':'cobacia',
    'INPUT_2':DISP_PATH+'OttoDemanda.csv',
    'FIELD_2':'cobacia',
    'FIELDS_TO_COPY':['sum'],
    'METHOD':1,
    'DISCARD_NONMATCHING':False,
    'PREFIX':'',
    'OUTPUT':DISP_PATH+'DispHidrica.shp'
}))
print('Joining.... done!')