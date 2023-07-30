// Resize an image in Photoshop using ExtendScript

// Check if a document is open
if (app.documents.length > 0) {
  // Get the active document
  var doc = app.activeDocument;

  // Set the desired new width and height (in pixels)
  var newWidth = 800;
  var newHeight = 600;

  // Resize the document
  doc.resizeImage(newWidth, newHeight);

  // Save the changes
  doc.save();
} else {
  alert("No document is open in Photoshop.");
}
