const changingTextElement = document.getElementById('changing-text');
const startEditingButton = document.getElementById('start-editing-btn');
const texts = ['editing', 'cropping', 'blurring'];
let currentIndex = 0;

function changeText() {
  changingTextElement.textContent = `Photo 
  ${texts[currentIndex]} 
  made easy. Just use your voice.`;
  currentIndex = (currentIndex + 1) % texts.length;
}

setInterval(changeText, 3000);

startEditingButton.addEventListener('click', () => {
  // Handle start editing button click event
});


  // anime.js animations for the hover effect
  const libraryItems = document.querySelectorAll('.librarysection > div');

  libraryItems.forEach(item => {
    item.addEventListener('mouseenter', () => {
      anime({
        targets: item,
        backgroundColor: '#f0f0f0', // Change background color on hover
        scale: 1.1, // Scale up the div on hover
        duration: 300, // Animation duration (in ms)
        easing: 'easeOutCubic', // Easing function
      });
    });

    item.addEventListener('mouseleave', () => {
      anime({
        targets: item,
        backgroundColor: '#ffffff', // Change background color back to the original on hover out
        scale: 1, // Scale back to the original size on hover out
        duration: 300, // Animation duration (in ms)
        easing: 'easeOutCubic', // Easing function
      });
    });
  });



/*window.onload = function() {
    // Get the microphone element
    const microphone = document.getElementById('microphone');
  
    // Get the response element
    const responseElement = document.getElementById('response');
  
    // Get the text element
    const textElement = document.getElementById('text');
  
    // Update the response and text elements with initial values
    responseElement.textContent = 'Response: ';
    textElement.textContent = 'You said: ';
  
    // Add click event listener to the microphone
    microphone.addEventListener('click', function() {
      // Update the response and text elements while listening
      responseElement.textContent = 'Response: Listening...';
      textElement.textContent = 'You said: Listening...';
  
      // Make an AJAX request to the '/process_microphone' route
      fetch('/process_microphone', {
        method: 'POST'
      })
        .then(response => response.text())
        .then(reply => {
          console.log('Response:', reply);
          // Update the response element with the generated reply
          responseElement.textContent = 'Response: ' + reply;
          // Update the text element with the recorded speech
          textElement.textContent = 'You said: ' + '{{ text }}';
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  };
  */