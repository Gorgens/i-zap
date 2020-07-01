var bacia = ee.FeatureCollection("users/egorgens/zap/ribeiraoSantana");
var sq_bacia = 
    /* color: #98ff00 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-43.34009440347327, -18.026400164484432],
          [-43.34009440347327, -18.214998642278406],
          [-43.203451947418586, -18.214998642278406],
          [-43.203451947418586, -18.026400164484432]]], null, false);

// Filtra imagens da coleção no período escolhido
var input = ee.ImageCollection("COPERNICUS/S2_SR")
  .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 10)
  .filterBounds(bacia)
  .filterDate('2019-08-01', '2020-03-11')
  .median(); 

// use the bounding box of a Landsat-8 image
// var region = input.geometry();
var region = bacia.geometry();

// Display the image
// Map.centerObject(bacia);

// training region is the full image
var training = input.sample({
  region: region,
  scale: 30,
  numPixels: 5000
});

// train cluster on image
var clusterer = ee.Clusterer.wekaKMeans(10).train(training);

// cluster the complete image
var result = input.cluster(clusterer);

// Display the clusters with random colors.
// Map.addLayer(result.clip(bacia).randomVisualizer(), {}, 'clusters');


//Extended Directional Smoothing
function eds(image) {
  // Create a list of weights for a 3x3 kernel.
  var dir1 = ee.List([[0, 0, 0], [0.5, 0, 0.5], [0, 0, 0]]);
  var dir2 = ee.List([[0, 0.5, 0], [0, 0, 0], [0, 0.5, 0]]);
  var dir3 = ee.List([[0, 0, 0.5], [0, 0, 0], [0.5, 0, 0]]);
  var dir4 = ee.List([[0.5, 0, 0], [0, 0, 0], [0, 0, 0.5]]);
  //Convolve directional kernels with the image
  var d1 = image.convolve(ee.Kernel.fixed(3, 3, dir1, -1, -1));
  var d2 = image.convolve(ee.Kernel.fixed(3, 3, dir2, -1, -1));
  var d3 = image.convolve(ee.Kernel.fixed(3, 3, dir3, -1, -1));
  var d4 = image.convolve(ee.Kernel.fixed(3, 3, dir4, -1, -1));
  //Absolute value of the difference from convolved image with original values
  var D1=(d1.subtract(image)).abs();
  var D2=(d2.subtract(image)).abs();
  var D3=(d3.subtract(image)).abs();
  var D4=(d4.subtract(image)).abs();
  //Pick min pixel value based on abs difference(first input) using reducers
  var Dd=ee.ImageCollection([[D1,d1],[D2,d2],[D3,d3],[D4,d4]]);
  var reducer =ee.Reducer.min(2);
  //Select the second input to the reducer
  var v = Dd.reduce(reducer).select('min1');
  return v;
}


function msd(denoised,original) {
  var diff = denoised.subtract(original);
  var sq= diff.pow(2);
  var meanDict = sq.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: poly,
  scale: 20 ,
  bestEffort:true
  });
  return meanDict;
}

//plane smoothing to remove speckle noise
var smooth = ee.Image(result.focal_median(11, 'square'));
// var image_spk = eds(result);

// Compare classifications
// var msd1=msd(smooth,image);
// print (msd1);


// Map.addLayer(result.clip(bacia).randomVisualizer(), {}, 'classified');
Map.addLayer(smooth.clip(bacia).randomVisualizer(), {},'classified smooth');
// Map.addLayer(image_spk.clip(bacia).randomVisualizer(), {},'classified EDS');

// print(smooth.clip(bacia).bandNames());

Export.image.toDrive({
  image: smooth.clip(sq_bacia),
  description: 'usoSolo10class',
  scale: 5,
  region: sq_bacia,
  folder: 'export_zap'
});