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

  