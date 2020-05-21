import pandas as pd
import geopandas as gp
import numpy as np
import matplotlib.pyplot as plt
import descartes

### Define variáveis do ambiente  ------------------------------

VAZPATH = '/sysroot/home/eric/Documentos/Base de dados ZAP/zip 2406 reg vazao/'
VAZFILE = '2406_JQ_Igam_UFV_reg_vazao_lin.shp'

OTTOPATH = '/sysroot/home/eric/Documentos/Base de dados ZAP/zip 0102 ottobacias/'
OTTOFILE = '0102_jq_otto_bacia_pol.shp'

EPSG = 4326
CODRIO = "7582998"

hidrico = gp.read_file(VAZPATH+VAZFILE, encoding='ISO-8859-1')
hidrico.crs = 'EPSG:'+str(EPSG)
# Check columns in shapefile
#for col in hidrico.columns:
#    print(col)

# Check columns type in shapefile
#for col in hidrico.columns:
#    print(type(col))

hidricoInteresse = hidrico[hidrico['cocursodag'].str.contains(CODRIO)]
hidricoInteresse.plot()
plt.savefig('/sysroot/home/eric/Github/i_zap/01_delimitacao/hidrico.png')
# for col in hidricoInteresse.columns:
#     print(col)

hidricoInteresse.loc[:,'q7_10'] = [x.replace(',', '.') for x in hidricoInteresse['q7_10']]
hidricoInteresse.loc[:,'q7_10'] = hidricoInteresse['q7_10'].astype(float)

hidricoInteresse.loc[:,'qmld_'] = [x.replace(',', '.') for x in hidricoInteresse['qmld_']]
hidricoInteresse.loc[:,'qmld_'] = hidricoInteresse['qmld_'].astype(float)

# print(hidricoInteresse.head())
# print(hidricoInteresse['q7_10'].sum())

otto = gp.read_file(OTTOPATH+OTTOFILE)
otto.crs = 'EPSG:'+str(EPSG)

ottoInteresse = otto[otto['cocursodag'].str.contains('^'+CODRIO)]
ottoInteresse.plot()
plt.savefig('/sysroot/home/eric/Github/i_zap/01_delimitacao/otto.png')

ottoClean = ottoInteresse[['nunivotto3', 'geometry']]
bacia = ottoClean.dissolve(by='nunivotto3')
bacia.plot()
plt.savefig('/sysroot/home/eric/Github/i_zap/01_delimitacao/bacia.png')

hidricoInteresse.to_file("/sysroot/home/eric/Github/i_zap/01_delimitacao/delimitacao.gpkg", layer='redeHidro', driver="GPKG")
ottoInteresse.to_file("/sysroot/home/eric/Github/i_zap/01_delimitacao/delimitacao.gpkg", layer='ottobacias', driver="GPKG")
bacia.to_file("/sysroot/home/eric/Github/i_zap/01_delimitacao/delimitacao.gpkg", layer='bacia', driver="GPKG")


