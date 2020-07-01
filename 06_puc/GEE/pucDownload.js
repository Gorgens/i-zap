var bacia = ee.FeatureCollection("users/egorgens/zap/ribeiraoSantana"); // limites da bacia de interesse
var srtm = ee.Image("USGS/SRTMGL1_003").clip(bacia);                                // import srtm
var slope = ee.Terrain.slope(srtm);                                     // compute slope

var customRemap = function(image, lowerLimit, upperLimit, newValue) {   // functions to reclass slope based on Embrapa
  var mask = image.gte(lowerLimit).and(image.lt(upperLimit));
  return image.where(mask, newValue);
};
var slopePesos = customRemap(slope, 3, 7.999, 4);                          // Raclass slope raster
var slopePesos = customRemap(slopePesos, 0, 2.999, 5);
var slopePesos = customRemap(slopePesos, 8, 19.999, 3);
var slopePesos = customRemap(slopePesos, 20, 44.999, 2);
var slopePesos = customRemap(slopePesos, 45, 90, 1);

var soloPesos = ee.Image("users/egorgens/zap/solos_mg_pesos").clip(bacia);
var litoPesos = ee.Image("users/egorgens/zap/tipo_mg_pesos").clip(bacia);

var puc = slopePesos.multiply(0.5).add(soloPesos.multiply(0.39)).add(litoPesos.multiply(0.11));

// Add layers to canvas
Map.addLayer(puc, 
  {min: 0, max: 5}, 
  'PUC', 
  true);
  
// Export.image.toDrive({
//   image: puc.clip(bacia),
//   description: 'puc',
//   scale: 30,
//   region: bacia,
//   folder: 'export_zap'
// });