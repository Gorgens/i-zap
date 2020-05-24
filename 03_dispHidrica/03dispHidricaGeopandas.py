import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt

outorgasBacia = gp.read_file("/home/gorgens/Github/i_zap/zapRibSantana.gpkg", layer='outorgasBacia')
hidricoInteresse = gp.read_file("/home/gorgens/Github/i_zap/zapRibSantana.gpkg", layer='redeHidro')
ottoInteresse = gp.read_file("/home/gorgens/Github/i_zap/zapRibSantana.gpkg", layer='ottobacias')

limitCaptacao = 0.5

# Join by location
outorgasBacia = outorgasBacia.drop(['index_right'], axis=1)
joinedOutorgas = gp.sjoin(outorgasBacia, ottoInteresse, op="within")
print(joinedOutorgas.head())



# Calculos de disṕonibilidade
# hidricoInteresse['QDH'] = limitCaptacao * hidricoInteresse['q7_10'] - hidricoInteresse['']