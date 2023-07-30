// Create a new layer
var newLayer = app.activeDocument.artLayers.add();

// Fill the new layer with 50% gray
app.activeDocument.selection.selectAll();
app.activeDocument.selection.fill(app.foregroundColor);
app.foregroundColor.rgb.red = 128;
app.foregroundColor.rgb.green = 128;
app.foregroundColor.rgb.blue = 128;

// Set the layer mode to "Multiply"
newLayer.blendMode = BlendMode.MULTIPLY;

// Set the opacity of the new layer to 50%
newLayer.opacity = 50;
