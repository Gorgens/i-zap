## ---
## title: "Delimitação da bacia"
## author: "Eric Gorgens - NEPZAP/UFVJM"
## date: "17/02/2020"
## ---

require(tidyverse)
require(raster)
require(leaflet)
require(rgdal)
require(tmap)
require(sf)
require(maptools)

## Delimitação da bacia

### Localiza o rio principal a ser estudado

shp2406 = shapefile("../i_zap_input/2406_JQ_Igam_UFV_reg_vazao_lin.shp")
proj4string(shp2406) = CRS("+init=epsg:4326")

rioInteresse = shp2406 %>% subset(noriocomp == 'Ribeirão Santana')
rioId = rioInteresse$cocursodag[1]
map = tm_shape(rioInteresse) + 
    tm_lines("blue") + 
    tm_legend(outside = TRUE, hist.width = 2) +
    tm_grid(lines = FALSE,
			labels.inside.frame = FALSE,
			projection = "+proj=longlat", col = 'gray')

tmap_save(map, "./01_delimitacao/01rioIntresse.png", width = 25, height = 15, units = "cm")


### Filtra as otto bacias contribuintes

shp0102 = shapefile("../i_zap_input/0102_jq_otto_bacia_pol.shp")
proj4string(shp0102) = CRS("+init=epsg:4326")

ottoInteresse = shp0102 %>% subset(grepl(rioId, cocursodag))
writeOGR(ottoInteresse, ".", "./01_delimitacao/02ottoInteresse", driver="ESRI Shapefile")
#print(paste(length(ottoInteresse), 'otto bacias encontradas.'))

map = tm_shape(ottoInteresse) + tm_polygons() +
	  tm_shape(rioInteresse) + tm_lines("blue") +
    tm_legend(outside = TRUE, hist.width = 2) +
    tm_grid(lines = FALSE,
			labels.inside.frame = FALSE,
			projection = "+proj=longlat", col = 'gray')

tmap_save(map, "./01_delimitacao/02ottoInteresse.png", width = 25, height = 15, units = "cm")

### Delimita a bacia de estudo

ottoMerged = unionSpatialPolygons(ottoInteresse, IDs = ottoInteresse$nunivotto6)
ottoMerged$area_sqkm <- area(ottoMerged) / 1000000
#print(paste(round(ottoMerged$area_sqkm, 4), 'km2 é a área da bacia.'))
writeOGR(ottoMerged, ".", "./01_delimitacao/03baciaInteresse", driver="ESRI Shapefile")


map = tm_shape(ottoMerged) + tm_polygons() +
    tm_shape(rioInteresse) + tm_lines("blue") +
    tm_legend(outside = TRUE, hist.width = 2) +
    tm_grid(lines = FALSE,
			labels.inside.frame = FALSE,
			projection = "+proj=longlat", col = 'gray')

tmap_save(map, "./01_delimitacao/03baciaInteresse.png", width = 25, height = 15, units = "cm")


### Determina rede hídrica da bacia de estudo

redeHidrica = raster::intersect(shp2406, ottoMerged)
writeOGR(redeHidrica, ".", "./01_delimitacao/04redeHidrica", driver="ESRI Shapefile")

map = tm_shape(ottoMerged) + tm_polygons() +
	  tm_shape(redeHidrica) + tm_lines("blue") +
    tm_legend(outside = TRUE, hist.width = 2) +
    tm_grid(lines = FALSE,
			labels.inside.frame = FALSE,
			projection = "+proj=longlat", col = 'gray')

tmap_save(map, "./01_delimitacao/04redeHidrica.png", width = 25, height = 15, units = "cm")


rm(shp0102, shp2406, rioInteresse, rioId)
