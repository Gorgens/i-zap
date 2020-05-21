import pandas as pd
import geopandas as gp
import numpy as np
import matplotlib.pyplot as plt
import descartes

DISPPATH='/sysroot/home/eric/Github/i_zap/03_dispHidrica/'
LIMPATH='/sysroot/home/eric/Github/i_zap/01_delimitacao/'
CSV = '/sysroot/home/eric/Github/i_zap/03_dispHidrica/OutorgasFelicioDosSantos.csv'
EPSG = 4326

print('Cleaning: limpando arquivo com as outorgas!')
df = pd.read_csv(CSV, encoding='latin-1')
df.rename(columns={'Portaria':'portaria',
    'Data de Publicação': 'publicacao',
    'Data de Vencimento da Portaria': 'vencimento',
    'Status Processo': 'status',
    'Empreendedor': 'pf',
    'CPF_CNPJ Empreendedor': 'cpfCnpjPf',
    'Endereço Empreendedor': 'enderecoPf',
    'Número Empreendedor': 'numPf',
    'Complemento Empreendedor': 'complementoPf',
    'Bairro Empreendedor': 'bairroPf',
    'Município Empreendedor': 'municipioPf',
    'UF Empreendedor': 'estadoPf',
    'CEP Empreendedor': 'cepPf',
    'Telefone Empreendedor': 'telefonePf',
    'Caixa Postal Empreendedor': 'caixaPostalPf',
    'Empreendimento': 'Pj',
    'CPF_CNPJ Empreendimento': 'cpfCnpjPj',
    'Endereço Empreendimento': 'enderecoPj',
    'Número Empreendimento': 'numPj',
    'Complemento Empreendimento': 'complementoPj',
    'Bairro Empreendimento': 'bairroPj',
    'Município Empreendimento': 'municipioPj',
    'UF Empreendimento': 'estadoPj',
    'CEP Empreendimento': 'cepPj',
    'Telefone Empreendimento': 'telefonePj',
    'Caixa Postal Empreendimento': 'caixaPostalPj',
    'Bacia Federal GEO': 'baciaFederal',
    'Bacia Estadual': 'baciaEstadual',
    'UPGRH': 'upgrh',
    'Curso D´água': 'cursoDagua',
    'Tipo': 'tipo',
    'Codigo_Modo_Uso': 'codigoUso',
    'Modo de Uso': 'modoUso',
    'Área inundada': 'areaInundada',
    'Volume de acumulação': 'volAcumulacao',
    'Finalidades': 'finalidades',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
    'Latitude Grau': 'latGrau',
    'Latitude Minutos': 'latMin',
    'Latitude Segundos': 'latSeg',
    'Longitude Graus': 'longGrau',
    'Longitude Minutos': 'longMin',
    'Longitude Segundos': 'longSeg',
    'UTM X': 'utmX',
    'UTM Y': 'utmY',
    'DATUM': 'datum',
    'Fuso': "fuso",
    'Meridiano Central': 'meridiano',
    'Unidade_Vazao': 'unidadeVazao',
    'Vazao Jan': 'vazaoJan',
    'Vazao Fev': 'vazaoFev',
    'Vazao Mar': 'vazaoMar',
    'Vazao Abr': 'vazaoAbr',
    'Vazao Mai': 'vazaoMai',
    'Vazao Jun': 'vazaoJun',
    'Vazao Jul': 'vazaoJul',
    'Vazao Ago': 'vazaoAgo',
    'Vazao Set': 'vazaoSet',
    'Vazao Out': 'vazaoOut',
    'Vazao Nov': 'vazaoNov',
    'Vazao Dez': 'vazaoDez',
    'Captacao Jan': 'capJan',
    'Captacao Fev': 'capFev',
    'Captacao Mar': 'capMar',
    'Captacao Abr': 'capAbr',
    'Captacao Mai': 'caoMai',
    'Captacao Jun': 'capJun',
    'Captacao Jul': 'capJul',
    'Captacao Ago': 'capAgo',
    'Captacao Set': 'capSet',
    'Captacao Out': 'capOut',
    'Captacao Nov': 'capNov',
    'Captacao Dez': 'capDez',
    'Dia/Mes Jan': 'diaMesJan',
    'Dia/Mes Fev': 'diaMesFev',
    'Dia/Mes Mar': 'diaMesMar',
    'Dia/Mes Abr': 'diaMesAbr',
    'Dia/Mes Mai': 'diaMesMai',
    'Dia/Mes Jun': 'diaMesJun',
    'Dia/Mes Jul': 'diaMesJul',
    'Dia/Mes Ago': 'diaMesAgo',
    'Dia/Mes Set': 'diaMesSet',
    'Dia/Mes Out': 'diaMesOut',
    'Dia/Mes Nov': 'diaMesNov',
    'Dia/Mes Dez': 'diaMesDez',
    'DES_ATIVIDADE': 'desAtividade',
    'COD_COPAM': 'codCopam',
    'TIPO_LICENCA': 'tipoLicenca',
    'DNPM': 'dnpm',
    'PORTE': 'porte',
    'CLASSE': 'classe',
    'Uso Insignificante': 'usoInsignificante',
    'Data Maxima da Decisao': 'dataMaxDecisao',
    'Formalizacao': 'formalizacao',
    'Concessao': 'concessao',
    'OBSERVACAO': 'observacao',
    'Num_FCE': 'numFce',
    'Ano_FCE': 'anoFce',
    'Num_FOB': 'numFob',
    'Ano_FOB': 'anoFob',
    'OBS_VALOR_COBRANCA': 'valorCobranca',
    'VALOR_LICENCIAMENTO': 'valorLicenciamento',
    'VALOR_ANALISE': 'valorAnalise',
    'VALOR_IGAM': 'valorIgam',
    'VALOR_LICENCIAMENTO_IEF': 'valorLicenIef',
    'Unidade de Análise': 'unidadeAnalise',
    'Natureza_Outorga': 'naturezaOutorga',
    'Portaria_Renovada_Retificada': 'portRenovRetif'
}, inplace = True)
#df.columns

df['publicacao'] = pd.to_datetime(df['publicacao'], format='%d/%m/%Y')
df['vencimento'] = pd.to_datetime(df['vencimento'], format='%d/%m/%Y')
df[['publicacao', 'vencimento', 'latitude', 'longitude']].head()

df['latGrau'] = df['latGrau'].str.replace('º', '')
df['longGrau'] = df['longGrau'].str.replace('º', '')
#df[['latGrau', 'longGrau']].head()

df['latMin'] = df['latMin'].str.replace('´', '')
df['longMin'] = df['longMin'].str.replace('´', '')
#df[['latMin', 'longMin']].head()

df['latSeg'] = df['latSeg'].str.replace('"', '')
df['longSeg'] = df['longSeg'].str.replace('"', '')
#df[['latSeg', 'longSeg']].head()

#df.loc['48302/2019']['latSeg']
df['latSeg'] = df['latSeg'].str.replace(',', '.')
df['longSeg'] = df['longSeg'].str.replace(',', '.')
df['latSeg'] = df['latSeg'].str.replace(' ', '')
df['longSeg'] = df['longSeg'].str.replace(' ', '')
df['latitude'] = df['latitude'].str.replace(',', '.')
df['longitude'] = df['longitude'].str.replace(',', '.')

df[["latGrau", "latMin", "latSeg", "longGrau", "longMin", "longSeg"]] = df[["latGrau", "latMin", "latSeg", "longGrau", "longMin", "longSeg"]].apply(pd.to_numeric)
#df[['latitude', 'latGrau', 'latMin', 'latSeg', 'longitude', 'longGrau', 'longMin', 'longSeg', ]].head()

df[["utmX", "utmY"]] = df[["utmX", "utmY"]].apply(pd.to_numeric)
#(df[["utmX", "utmY"]].dropna()
#    .head())

df['longDec'] = -1 * (df['longGrau'] + df['longMin']/60 + df['longSeg']/3600)
df['latDec'] = -1 * (df['latGrau'] + df['latMin']/60 + df['latSeg']/3600)
#df[['latDec', 'longDec']].head()
#print(outorga.shape)
outorga = (df[df['tipo'].str.contains("Superficial")]
     .drop_duplicates())
#print(outorga.shape)
outorga = outorga[~outorga['modoUso'].str.contains('TRAVESSIA')]
#print(outorga.shape)
outorga = outorga[outorga['vencimento'] > '2019-07-01']
#print(outorga.shape)
outorga = outorga[(outorga['status'] == 'OUTORGA RENOVADA') | (outorga['status'] == 'OUTORGA DEFERIDA') | (outorga['status'] == 'CADASTRO EFETIVADO')]

#print(df.shape, outorga.shape)
#outorga.head()

sad69utm = outorga[(outorga['datum'] == 'SAD 69')].dropna(subset=['utmX'])
#print(sad69utm.shape)
wgs84utm = outorga[outorga['datum'] == 'WGS84'].dropna(subset=['utmX'])
#print(wgs84utm.shape)
sad69scg = outorga[(outorga['datum'] == 'SAD 69')].dropna(subset=['latDec'])
#print(sad69scg.shape)
#print(sad69scg.head())
wgs84scg = outorga[(outorga['datum'] == 'WGS84')].dropna(subset=['latDec'])
#print(wgs84scg.shape)
#print(wgs84scg.head())

sad69scg.to_csv(DISPPATH+'sad69scg.csv', index=False, sep = ',')
wgs84scg.to_csv(DISPPATH+'wgs84scg.csv', index=False, sep = ',')
sad69utm.to_csv(DISPPATH+'sad69utm.csv', index=False, sep = ',')
wgs84utm.to_csv(DISPPATH+'wgs84utm.csv', index=False, sep = ',')
print('Cleaning done!')

# print('Importing: outorgas por projeção!')
bacia = gp.read_file("/sysroot/home/eric/Github/i_zap/01_delimitacao/delimitacao.gpkg", layer='bacia')
base1 = bacia.plot(color='white', edgecolor='black')

sad69scg = pd.read_csv(DISPPATH+'sad69scg.csv')
sad69scgLayer = gp.GeoDataFrame(sad69scg, geometry=gp.points_from_xy(sad69scg.longDec, sad69scg.latDec))
sad69scgLayer.crs = 'EPSG:4291'
sad69scgLayer = sad69scgLayer.to_crs('EPSG:4326')
base2 = sad69scgLayer.plot(ax=base1, marker='o', color = 'red')

wgs84scg = pd.read_csv(DISPPATH+'wgs84scg.csv')
wgs84scgLayer = gp.GeoDataFrame(wgs84scg, geometry=gp.points_from_xy(wgs84scg.longDec, wgs84scg.latDec))
wgs84scgLayer.crs = 'EPSG:4326'
base3 = wgs84scgLayer.plot(ax=base2, marker='o', color = 'blue')

sad69utm = pd.read_csv(DISPPATH+'sad69utm.csv')
sad69utmLayer = gp.GeoDataFrame(sad69utm, geometry=gp.points_from_xy(sad69utm.utmX, sad69utm.utmY))
sad69utmLayer.crs = 'EPSG:29183'
sad69utmLayer = sad69utmLayer.to_crs('EPSG:4326')
base4 = sad69utmLayer.plot(ax=base3, marker='o', color = 'green')

wgs84utm = pd.read_csv(DISPPATH+'wgs84utm.csv')
wgs84utmLayer = gp.GeoDataFrame(wgs84utm, geometry=gp.points_from_xy(wgs84utm.utmX, wgs84utm.utmY))
wgs84utmLayer.crs = 'EPSG:32723'
wgs84utmLayer = wgs84utmLayer.to_crs('EPSG:4326')
wgs84utmLayer.plot(ax=base4, marker='o', color = 'black')
plt.savefig('/sysroot/home/eric/Github/i_zap/03_dispHidrica/outorgas.png')

# print('Merging: outorgas!')
gdf = gpd.GeoDataFrame(pd.concat([gdf1, gdf2, gdf3]))
# processing.run("saga:mergevectorlayers", {
#     'INPUT':[DISP_PATH+'sad69scg.shp',
#         DISP_PATH+'sad69utm.shp',
#         DISP_PATH+'wgs84scg.shp',
#         DISP_PATH+'wgs84utm.shp'],
#     'SRCINFO':True,
#     'MATCH':True,
#     'MERGED':DISP_PATH+'outorgas.shp'})
# print('Merging done!')
#
# print('Cliping: outorgas dentro da bacia!')
# (processing.run("native:clip", {
#     'INPUT':DISP_PATH+'outorgas.shp',
#     'OVERLAY':LIM_PATH+'limiteBacia.shp',
#     'OUTPUT':DISP_PATH+'outorgasBacia.shp'
# }))
# print('Cliping done!')
#
# outorgasBacia = QgsVectorLayer(DISP_PATH+'outorgasBacia.shp', "Outorgas bacia", 'ogr')
# outorgasBacia.setCrs(CRS)
# QgsProject.instance().addMapLayer(outorgasBacia)
# outorgasBacia.dataProvider().addAttributes( [ QgsField("captacao", QVariant.Double) ] )
# outorgasBacia.updateFields()
#
# print('Atualize manualmente o campo [captacao].')