// Script criado pelo Prof. Eric Bastos Gorgens - UFVJM
// Criação de imagem sentinel RGB + IR para bacia de interesse, e período de interesse
// Licensa uso Creative Commons - Atribuição-CompartilhaIgual 4.0 Internacional

var bacia = ee.FeatureCollection("users/egorgens/zap/ribeiraoSantana");

// Filtra imagens da coleção no período escolhido
var sentinel = ee.ImageCollection("COPERNICUS/S2_SR")
  .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)
  .filterBounds(bacia)
  .filterDate('2019-08-01', '2020-03-11')
  .median();                          

// Recorta a imagem sentinel na área de interesse
var clipped = sentinel.clip(bacia);

// Centraliza o canva na região da bacia
Map.centerObject(bacia, 12);

// Adiciona camada no canvas
Map.addLayer(clipped,                                         
  {bands:['B4', 'B3', 'B2'], min:100, max:800}, 
  'Sentinel'); 

// Exporta as bandas do sentinel para GoogleDrive
var b4 = clipped.select('B4');
Export.image.toDrive({
  image: b4,
  description: 'sentinel_2017_2019_b4',
  scale: 10,
  region: bacia,
  folder: 'export_zap'
});	

var b2 = clipped.select('B2');
Export.image.toDrive({
  image: b2,
  description: 'sentinel_2017_2019_b2',
  scale: 10,
  region: bacia,
  folder: 'export_zap'
});	


var b3 = clipped.select('B3');
Export.image.toDrive({
  image: b3,
  description: 'sentinel_2017_2019_b3',
  scale: 10,
  region: bacia,
  folder: 'export_zap'
});	


var b8 = clipped.select('B8');
Export.image.toDrive({
  image: b8,
  description: 'sentinel_2017_2019_b8',
  scale: 10,
  region: bacia,
  folder: 'export_zap'
});	

