// Change the hue of an image in Photoshop using ExtendScript

// Check if a document is open
if (app.documents.length > 0) {
  // Get the active document
  var doc = app.activeDocument;

  // Set the desired hue shift value (in degrees, -180 to 180)
  var hueShift = 30; // Example: shift the hue by 30 degrees (positive value for clockwise, negative for counterclockwise)

  // Create a Hue/Saturation adjustment layer
  var hueSaturationAdjustment = doc.artLayers.add();
  hueSaturationAdjustment.kind = LayerKind.HUESATURATION;

  // Set the hue shift value
  var hueSaturation = hueSaturationAdjustment.adjustment;

  hueSaturation.hue = hueShift;

  // Save the changes
  doc.save();
} else {
  alert("No document is open in Photoshop.");
}
