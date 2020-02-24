var sentinel = ee.ImageCollection("COPERNICUS/S2_SR")
  .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)
  .filterBounds(bacia)
  .filterDate('2017-07-01', '2019-10-30')
  .median();                           // Filtra imagens da coleção do período de seca


var clipped = sentinel.clip(bacia);
Map.centerObject(center, 14);
// Map.addLayer(clipped,                                             // Adiciona camada no canvas
//   {bands:['B4', 'B3', 'B2'], min:100, max:800}, 
//   'Sentinel'); 

var b4 = clipped.select('B4');
// Export.image.toDrive({
//   image: b4,
//   description: 'sentinel_2017_2019_b4',
//   scale: 10,
//   region: bacia,
//   folder: 'export_zap'
// });	

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
