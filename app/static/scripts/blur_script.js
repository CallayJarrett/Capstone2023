// Blur an image in Photoshop using ExtendScript

// Check if a document is open
if (app.documents.length > 0) {
  // Get the active document
  var doc = app.activeDocument;

  // Set the amount of Gaussian Blur (radius in pixels)
  var blurAmount = 5;

  // Create a new Blur Gallery filter
  var blurGalleryFilter = doc.smartFilters.addFilter("Gaussian Blur");
  var blurGallery = blurGalleryFilter.galleryOptions;

  // Set the blur amount
  blurGallery.blur = blurAmount;

  // Apply the filter
  blurGalleryFilter.apply();

  // Save the changes
  doc.save();
} else {
  alert("No document is open in Photoshop.");
}
