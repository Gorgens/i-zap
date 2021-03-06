## ---
## title: "Classificação não supervisionada do uso do solo"
## author: "Eric Gorgens - NEPZAP/UFVJM"
## date: "17/02/2020"
## source("C:/Users/gorge/Documents/GitHub/i-zap/zap_us1_classNaoSup.R")
## ---


require(tidyverse)
require(raster)
require(leaflet)
require(rgdal)
require(rgeos)
require(tmap)
require(sf)
require(sp)

## Uso do solo

### Baixar imagens Google Earth Engine (javaScript)

# var center = /* color: #d63000 */ee.Geometry.Point([-43.22156204898374, -18.06797432111501]),
    # bacia = ee.FeatureCollection("users/egorgens/zap/ribeiraoSantana");
	
# var sentinel = ee.ImageCollection("COPERNICUS/S2_SR")
  # .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)
  # .filterBounds(bacia)
  # .filterDate('2017-07-01', '2019-10-30')
  # .median();                           // Filtra imagens da coleção do período de seca


# var clipped = sentinel.clip(bacia);
# Map.centerObject(center, 14);
# Map.addLayer(clipped,                                             // Adiciona camada no canvas
  # {bands:['B4', 'B3', 'B2'], min:100, max:800}, 
  # 'Sentinel'); 

# var b4 = clipped.select('B4');
# Export.image.toDrive({
  # image: b4,
  # description: 'sentinel_2017_2019_b4',
  # scale: 10,
  # region: bacia,
  # folder: 'export_zap'
# });	

# var b2 = clipped.select('B2');
# Export.image.toDrive({
  # image: b2,
  # description: 'sentinel_2017_2019_b2',
  # scale: 10,
  # region: bacia,
  # folder: 'export_zap'
# });	


# var b3 = clipped.select('B3');
# Export.image.toDrive({
  # image: b3,
  # description: 'sentinel_2017_2019_b3',
  # scale: 10,
  # region: bacia,
  # folder: 'export_zap'
# });	


# var b8 = clipped.select('B8');
# Export.image.toDrive({
  # image: b8,
  # description: 'sentinel_2017_2019_b8',
  # scale: 10,
  # region: bacia,
  # folder: 'export_zap'
# });	



### Importação das imagens

sentinel_b2 = raster('sentinel_2017_2019_b2.tif')
sentinel_b3 = raster('sentinel_2017_2019_b3.tif')
sentinel_b4 = raster('sentinel_2017_2019_b4.tif')
sentinel_b8 = raster('sentinel_2017_2019_b8.tif')
sentinel_vv = raster('sentinel_2017_2019_vv.tif')
sentinel_vh = raster('sentinel_2017_2019_vh.tif')
srtm = raster('srtm_30m.tif')

sentinel_b2r = resample(sentinel_b2, srtm)
sentinel_b3r = resample(sentinel_b3, srtm)
sentinel_b4r = resample(sentinel_b4, srtm)
sentinel_b8r = resample(sentinel_b8, srtm)
sentinel_vvr = resample(sentinel_vv, srtm)
sentinel_vhr = resample(sentinel_vh, srtm)

rm(sentinel_b2, sentinel_b3, sentinel_b4, sentinel_b8, sentinel_vh, sentinel_vv)


### Classificação supervisionada

stack_bacia = stack(sentinel_b2r, sentinel_b3r, sentinel_b4r, sentinel_b8r, sentinel_vvr, sentinel_vhr, srtm)
rm(sentinel_b2r, sentinel_b3r, sentinel_b4r, sentinel_b8r, sentinel_vhr, sentinel_vvr, srtm)

image.df <- as.data.frame(stack_bacia)  
cluster.image = kmeans(na.omit(image.df), centers=15)

image.df.factor <- rep(NA, length(image.df[,1]))
image.df.factor[!is.na(image.df[,1])] <- cluster.image$cluster

#create raster output
clusters <- raster(stack_bacia)   ## create an empty raster with same extent than "image"  
clusters <- setValues(clusters, image.df.factor) ## fill the empty raster with the class results  

tm_shape(clusters) + 
  tm_raster()

# filtro de passa baixa
cluster_focal = focal(clusters, w=matrix(1,nrow=7,ncol=7)  , fun=median)
tm_shape(cluster_focal) + 
  tm_raster()
