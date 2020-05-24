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
#print(joinedOutorgas.head())
#print(joinedOutorgas[['Processo Outorga', 'cobacia', 'captacao']].head())

grouped = joinedOutorgas.groupby('cobacia').sum()
grouped.reset_index(inplace=True)

grouped = grouped[['cobacia', 'captacao']]
#print(grouped.head())

hidricoInteresse = hidricoInteresse.merge(grouped, on='cobacia', how='outer')
hidricoInteresse.rename(columns={'captacao': 'QdemTotal'}, inplace=True)

# Calculos de disṕonibilidade
hidricoInteresse['QDH'] = limitCaptacao * hidricoInteresse['q7_10'] - hidricoInteresse['QdemTotal']
hidricoInteresse['compromDH'] = ((limitCaptacao * hidricoInteresse['q7_10']) - hidricoInteresse['QDH']) * 100 / (limitCaptacao * hidricoInteresse['q7_10'])
hidricoInteresse['Qreg'] = (0.7 * hidricoInteresse['qmld_']) - (limitCaptacao * hidricoInteresse['q7_10'])
hidricoInteresse['Viab'] = hidricoInteresse['Qreg'] + hidricoInteresse['QDH']

hidricoInteresse.to_file("/home/gorgens/Github/i_zap/zapRibSantana.gpkg", layer='redeHidro', driver="GPKG")
