## ---
## title: "Disponibilidade Hidrica"
## author: "Eric Gorgens - NEPZAP/UFVJM"
## date: "17/02/2020"
## source("C:/Users/gorge/Documents/GitHub/i-zap/zap_dh2_dispHidrica.R")
## ---


require(tidyverse)
require(raster)
require(leaflet)
require(rgdal)
require(tmap)
require(sf)
require(maptools)
require(xlsx)
require(knitr)

setwd('C:/Users/gorge/Documents/GitHub/i-zap/')


## Disponibilidade hídrica

### Ajusta base de dados

outorgas = read.xlsx("./input/Outorgas_FelicioDosSantos.xlsx", 1, encoding="UTF-8")

outorgas$Latitude.Grau = as.numeric(gsub("º","", outorgas$Latitude.Grau))
outorgas$Latitude.Minutos = as.numeric(gsub("´","", outorgas$Latitude.Minutos))
outorgas$Latitude.Segundos = as.numeric(gsub(",", ".", gsub('"','', outorgas$Latitude.Segundos)))

outorgas$Longitude.Graus = as.numeric(gsub("º","", outorgas$Longitude.Graus))
outorgas$Longitude.Minutos = as.numeric(gsub("´","", outorgas$Longitude.Minutos))
outorgas$Longitude.Segundos = as.numeric(gsub(",", ".", gsub('"','', outorgas$Longitude.Segundos)))

outorgas$Latitude = gsub(",",".", outorgas$Latitude)
outorgas$Longitude = gsub(",",".", outorgas$Longitude)

outorgas$UTM.X = as.numeric(as.character(outorgas$UTM.X))
outorgas$UTM.Y = as.numeric(as.character(outorgas$UTM.Y))

outorgas$Vazao.Jan = as.numeric(as.character(outorgas$Vazao.Jan))

outorgas$Long = -1 * (outorgas$Longitude.Graus + outorgas$Longitude.Minutos/60 + outorgas$Longitude.Segundos/3600)
outorgas$Lat = -1 * (outorgas$Latitude.Grau + outorgas$Latitude.Minutos/60 + outorgas$Latitude.Segundos/3600)

outorgas$Data.de.Publicação = as.Date(outorgas$Data.de.Publicação, "%d/%m/%Y")
outorgas$Data.de.Vencimento.da.Portaria = as.Date(outorgas$Data.de.Vencimento.da.Portaria, "%d/%m/%Y")


### Filtra base de dados por data e por tipo de outorga

superficial = dplyr::filter(outorgas, grepl('Superficial', Tipo))
superficial = distinct(superficial)
superficialCaptacao = dplyr::filter(superficial, !grepl('TRAVESSIA', Modo.de.Uso))
recentes = dplyr::filter(superficialCaptacao, 
                  superficialCaptacao$Data.de.Vencimento.da.Portaria > as.Date('01/07/2019', '%d/%m/%Y'))

renovada = dplyr::filter(recentes, grepl('OUTORGA RENOVADA', Status.Processo))
deferida = dplyr::filter(recentes, grepl('OUTORGA DEFERIDA', Status.Processo))
efetivado = dplyr::filter(recentes, grepl('CADASTRO EFETIVADO', Status.Processo))

uteis = rbind(renovada, deferida, efetivado)

### Separa dados em WGS84 GMS e filtra pontos dentro da bacia

wgs84_gms = filter(uteis, uteis$DATUM == "WGS84" & is.na(uteis$UTM.X))
coordinates(wgs84_gms) = ~Long+Lat
proj4string(wgs84_gms) = CRS("+init=epsg:4326")

ottoMerged = shapefile('../01_Delimitacao_e_Hidrografia/01_Bacia_Interesse.shp')
proj4string(ottoMerged) = CRS("+init=epsg:4326")

tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(wgs84_gms) + tm_dots("blue") +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')

wgs84_gmsBacia = raster::intersect(wgs84_gms, ottoMerged)

if(length(wgs84_gmsBacia) != 0) {
  tm_shape(ottoMerged) + tm_polygons() +
    tm_shape(wgs84_gmsBacia) + tm_dots("blue") +
          tm_grid(labels.inside.frame = FALSE, 
                  projection = "+proj=longlat", col = 'gray')
}

### Separa dados em SAD69 GMS, converte para WGS84 e filtra pontos dentro da bacia

sad69_gms = filter(uteis, uteis$DATUM == "SAD 69" & is.na(uteis$UTM.X))
coordinates(sad69_gms) <- ~Long+Lat
proj4string(sad69_gms) <- CRS("+init=epsg:4618")
sad69_gms2wgs84 = spTransform(sad69_gms, crs(ottoMerged))

tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(sad69_gms) + tm_dots("blue") +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')

sad69_gms2wgs84Bacia = raster::intersect(sad69_gms2wgs84, ottoMerged)

if(length(sad69_gms2wgs84Bacia) != 0) {
  tm_shape(ottoMerged) + tm_polygons() +
    tm_shape(sad69_gms2wgs84Bacia) + tm_dots("blue") +
          tm_grid(labels.inside.frame = FALSE, 
                  projection = "+proj=longlat", col = 'gray')
}

### Separa dados em WGS84m UTM, converte para WGS84 e filtra pontos dentro da bacia

wgs84_utm = filter(uteis, uteis$DATUM == "WGS84" & !is.na(uteis$UTM.X))
coordinates(wgs84_utm) <- ~UTM.X+UTM.Y
proj4string(wgs84_utm) <- CRS("+init=epsg:32723")  
wgs84_utm2gms = spTransform(wgs84_utm, crs(ottoMerged))

tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(wgs84_utm2gms) + tm_dots("blue") +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')

wgs84_utm2gmsBacia = raster::intersect(wgs84_utm2gms, ottoMerged)

if(length(wgs84_utm2gmsBacia) != 0) {
tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(wgs84_utm2gmsBacia) + tm_dots("blue") +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')
}

### Separa dados em SAD69 UTM, converte para WGS84 e filtra pontos dentro da bacia

sad69_utm = filter(uteis, uteis$DATUM == "SAD 69" & !is.na(uteis$UTM.X))
coordinates(sad69_utm) <- ~UTM.X+UTM.Y
proj4string(sad69_utm) <- CRS("+init=epsg:5533")
sad69_utm2gms = spTransform(sad69_utm, crs(ottoMerged))

tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(sad69_utm2gms) + tm_dots("blue") +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')

sad69_utm2gmsBacia = raster::intersect(sad69_utm2gms, ottoMerged)

if(length(sad69_utm2gmsBacia) != 0) {
tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(sad69_utm2gmsBacia) + tm_dots("blue") +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')
}

### Unifica dados de outorga dentro da bacia

outorgasBacia = union(wgs84_gmsBacia, sad69_gms2wgs84Bacia)
outorgasBacia = union(outorgasBacia, wgs84_utm2gmsBacia)
outorgasBacia = union(outorgasBacia, sad69_utm2gmsBacia)
outorgasBacia = outorgasBacia[c('Processo.Outorga' , 'Portaria', 'Data.de.Vencimento.da.Portaria', 'Status.Processo', 'Tipo', 'CPF_CNPJ.Empreendedor')]
outorgasBacia$Vazao.Captada = 0.001

ottoInteresse = shapefile('./output/02ottoInteresse.shp')
proj4string(ottoInteresse) = CRS("+init=epsg:4326")


tm_shape(ottoInteresse) + tm_polygons() +
  tm_shape(outorgasBacia) + tm_dots("blue") +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')

writeOGR(outorgasBacia, ".", "05outorgasBacia", driver="ESRI Shapefile", encoding = 'UTF-8')

### Conferir dados de outorga
## http://www.igam.mg.gov.br/outorga/sistema-de-consulta-e-decisoes-de-outorga

### Agrupa pela soma dados de outorga de uma ottobacia

getOttoId = over(outorgasBacia, ottoInteresse)
outorgasBacia$cobacia = getOttoId$cobacia
VazaoOtto = outorgasBacia@data %>%
        group_by(cobacia) %>%
        summarise(QdemTotal = sum(Vazao.Captada))

ottoInteresse = merge(ottoInteresse, VazaoOtto, by='cobacia')

tm_shape(ottoInteresse) + tm_polygons('QdemTotal') +
  tm_shape(outorgasBacia) + tm_dots("blue") +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')

redeHidrica = shapefile('./output/04redeHidrica.shp', encoding="UTF-8")
proj4string(redeHidrica) = CRS("+init=epsg:4326")

getVazaoAcum = over(redeHidrica, ottoInteresse)

redeHidrica = merge(redeHidrica, VazaoOtto, by='cobacia')
redeHidrica$q7_10 = as.numeric(gsub(",", ".", gsub("\\.", "", redeHidrica$q7_10)))
redeHidrica$qmld_ = as.numeric(gsub(",", ".", gsub("\\.", "", redeHidrica$qmld_)))
redeHidrica$QDH = 0.5 * redeHidrica$q7_10 - redeHidrica$QdemTotal
redeHidrica$compromDH = ((0.5 * redeHidrica$q7_10) - redeHidrica$QDH) * 100 / (0.5 * redeHidrica$q7_10)
redeHidrica$QReg = (0.7 * redeHidrica$qmld_) - (0.5 * redeHidrica$q7_10)
redeHidrica$Viab = redeHidrica$QReg + redeHidrica$QDH

### Exporta gráficos finais

tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(redeHidrica) + tm_lines('QDH') +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')

tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(redeHidrica) + tm_lines('compromDH') +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')

tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(redeHidrica) + tm_lines('QReg') +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')

tm_shape(ottoMerged) + tm_polygons() +
  tm_shape(redeHidrica) + tm_lines('Viab') +
        tm_grid(labels.inside.frame = FALSE, 
                projection = "+proj=longlat", col = 'gray')