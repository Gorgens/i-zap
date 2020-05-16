#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd
import numpy as np
import re


# In[33]:


df = pd.read_csv('OutorgasFelicioDosSantos.csv', index_col=0, encoding='latin-1')


# In[34]:


df.rename(columns={'Portaria':'portaria',                    'Data de Publicação': 'publicacao',                   'Data de Vencimento da Portaria': 'vencimento',                   'Status Processo': 'status',                   'Empreendedor': 'pf',                   'CPF_CNPJ Empreendedor': 'cpfCnpjPf',                   'Endereço Empreendedor': 'enderecoPf',                   'Número Empreendedor': 'numPf',                   'Complemento Empreendedor': 'complementoPf',                   'Bairro Empreendedor': 'bairroPf',                   'Município Empreendedor': 'municipioPf',                   'UF Empreendedor': 'estadoPf',                   'CEP Empreendedor': 'cepPf',                   'Telefone Empreendedor': 'telefonePf',                   'Caixa Postal Empreendedor': 'caixaPostalPf',                   'Empreendimento': 'Pj',                   'CPF_CNPJ Empreendimento': 'cpfCnpjPj',                   'Endereço Empreendimento': 'enderecoPj',                   'Número Empreendimento': 'numPj',                   'Complemento Empreendimento': 'complementoPj',                   'Bairro Empreendimento': 'bairroPj',                   'Município Empreendimento': 'municipioPj',                   'UF Empreendimento': 'estadoPj',                   'CEP Empreendimento': 'cepPj',                   'Telefone Empreendimento': 'telefonePj',                   'Caixa Postal Empreendimento': 'caixaPostalPj',                   'Bacia Federal GEO': 'baciaFederal',                   'Bacia Estadual': 'baciaEstadual',                   'UPGRH': 'upgrh',                   'Curso D´água': 'cursoDagua',                   'Tipo': 'tipo',                   'Codigo_Modo_Uso': 'codigoUso',                   'Modo de Uso': 'modoUso',                   'Área inundada': 'areaInundada',                   'Volume de acumulação': 'volAcumulacao',                   'Finalidades': 'finalidades',                   'Latitude': 'latitude',                   'Longitude': 'longitude',                   'Latitude Grau': 'latGrau',                   'Latitude Minutos': 'latMin',                   'Latitude Segundos': 'latSeg',                   'Longitude Graus': 'longGrau',                   'Longitude Minutos': 'longMin',                   'Longitude Segundos': 'longSeg',                   'UTM X': 'utmX',                   'UTM Y': 'utmY',                   'DATUM': 'datum',                   'Fuso': "fuso",                   'Meridiano Central': 'meridiano',                   'Unidade_Vazao': 'unidadeVazao',                   'Vazao Jan': 'vazaoJan',                   'Vazao Fev': 'vazaoFev',                   'Vazao Mar': 'vazaoMar',                   'Vazao Abr': 'vazaoAbr',                   'Vazao Mai': 'vazaoMai',                   'Vazao Jun': 'vazaoJun',                   'Vazao Jul': 'vazaoJul',                   'Vazao Ago': 'vazaoAgo',                   'Vazao Set': 'vazaoSet',                   'Vazao Out': 'vazaoOut',                   'Vazao Nov': 'vazaoNov',                   'Vazao Dez': 'vazaoDez',                   'Captacao Jan': 'capJan',                   'Captacao Fev': 'capFev',                   'Captacao Mar': 'capMar',                   'Captacao Abr': 'capAbr',                   'Captacao Mai': 'caoMai',                   'Captacao Jun': 'capJun',                   'Captacao Jul': 'capJul',                   'Captacao Ago': 'capAgo',                   'Captacao Set': 'capSet',                   'Captacao Out': 'capOut',                   'Captacao Nov': 'capNov',                   'Captacao Dez': 'capDez',                   'Dia/Mes Jan': 'diaMesJan',                   'Dia/Mes Fev': 'diaMesFev',                   'Dia/Mes Mar': 'diaMesMar',                   'Dia/Mes Abr': 'diaMesAbr',                   'Dia/Mes Mai': 'diaMesMai',                   'Dia/Mes Jun': 'diaMesJun',                   'Dia/Mes Jul': 'diaMesJul',                   'Dia/Mes Ago': 'diaMesAgo',                   'Dia/Mes Set': 'diaMesSet',                   'Dia/Mes Out': 'diaMesOut',                   'Dia/Mes Nov': 'diaMesNov',                   'Dia/Mes Dez': 'diaMesDez',                   'DES_ATIVIDADE': 'desAtividade',                   'COD_COPAM': 'codCopam',                   'TIPO_LICENCA': 'tipoLicenca',                   'DNPM': 'dnpm',                   'PORTE': 'porte',                   'CLASSE': 'classe',                   'Uso Insignificante': 'usoInsignificante',                   'Data Maxima da Decisao': 'dataMaxDecisao',                   'Formalizacao': 'formalizacao',                   'Concessao': 'concessao',                   'OBSERVACAO': 'observacao',                   'Num_FCE': 'numFce',                   'Ano_FCE': 'anoFce',                   'Num_FOB': 'numFob',                   'Ano_FOB': 'anoFob',                   'OBS_VALOR_COBRANCA': 'valorCobranca',                   'VALOR_LICENCIAMENTO': 'valorLicenciamento',                   'VALOR_ANALISE': 'valorAnalise',                   'VALOR_IGAM': 'valorIgam',                   'VALOR_LICENCIAMENTO_IEF': 'valorLicenIef',                   'Unidade de Análise': 'unidadeAnalise',                   'Natureza_Outorga': 'naturezaOutorga',                   'Portaria_Renovada_Retificada': 'portRenovRetif'             
                  }, inplace = True)
#df.columns


# In[70]:


df['publicacao'] = pd.to_datetime(df['publicacao'], format='%d/%m/%Y')
df['vencimento'] = pd.to_datetime(df['vencimento'], format='%d/%m/%Y')
df[['publicacao', 'vencimento', 'latitude', 'longitude']].head()


# In[37]:


df['latGrau'] = df['latGrau'].str.replace('º', '')
df['longGrau'] = df['longGrau'].str.replace('º', '')
#df[['latGrau', 'longGrau']].head()


# In[38]:


df['latMin'] = df['latMin'].str.replace('´', '')
df['longMin'] = df['longMin'].str.replace('´', '')
#df[['latMin', 'longMin']].head()


# In[39]:


df['latSeg'] = df['latSeg'].str.replace('"', '')
df['longSeg'] = df['longSeg'].str.replace('"', '')
#df[['latSeg', 'longSeg']].head()


# In[47]:


#df.loc['48302/2019']['latSeg']

df['latSeg'] = df['latSeg'].str.replace(',', '.')
df['longSeg'] = df['longSeg'].str.replace(',', '.')
df['latSeg'] = df['latSeg'].str.replace(' ', '')
df['longSeg'] = df['longSeg'].str.replace(' ', '')
df['latitude'] = df['latitude'].str.replace(',', '.')
df['longitude'] = df['longitude'].str.replace(',', '.')

df[["latGrau", "latMin", "latSeg", "longGrau", "longMin", "longSeg"]] = df[["latGrau", "latMin", "latSeg", "longGrau", "longMin", "longSeg"]].apply(pd.to_numeric)
#df[['latitude', 'latGrau', 'latMin', 'latSeg', 'longitude', 'longGrau', 'longMin', 'longSeg', ]].head()


# In[56]:


df[["utmX", "utmY"]] = df[["utmX", "utmY"]].apply(pd.to_numeric)
#(df[["utmX", "utmY"]].dropna()
#    .head())


# In[55]:


df['longDec'] = -1 * (df['longGrau'] + df['longMin']/60 + df['longSeg']/3600)
df['latDec'] = -1 * (df['latGrau'] + df['latMin']/60 + df['latSeg']/3600)
#df[['latDec', 'longDec']].head()


# In[69]:


outorga = (df[df['tipo'].str.contains("Superficial")]
     .drop_duplicates())
outorga = outorga[~outorga['modoUso'].str.contains('TRAVESSIA')]
outorga = outorga[outorga['vencimento'] > '2019-07-01']
outorga = outorga[(outorga['status'] == 'OUTORGA RENOVADA') | (outorga['status'] == 'OUTORGA DEFERIDA') | (outorga['status'] == 'CADASTRO EFETIVADA')]

#print(df.shape, outorga.shape)
#outorga.head()


# In[ ]:


sad69 = df[df['datum'] == 'SAD 69']
wgs84 = df[df['datum'] == 'WGS84']

