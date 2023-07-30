// Change the saturation of an image in Photoshop using ExtendScript

// Check if a document is open
if (app.documents.length > 0) {
  // Get the active document
  var doc = app.activeDocument;

  // Set the desired saturation value (percentage, -100 to 100)
  var saturationValue = 50; // Example: increase saturation by 50%

  // Create a Hue/Saturation adjustment layer
  var hueSaturationAdjustment = doc.artLayers.add();
  hueSaturationAdjustment.kind = LayerKind.HUESATURATION;

  // Set the saturation value
  var hueSaturation = hueSaturationAdjustment.adjustment;

  hueSaturation.saturation = saturationValue;

  // Save the changes
  doc.save();
} else {
  alert("No document is open in Photoshop.");
}
