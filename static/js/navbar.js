const nav = document.querySelector('.navbar');
const offset = 25;

function navChangeColor(colored = true) {
  if (colored) {
    nav.classList.add('bg-blay', 'transition-all', 'duration-[0.25s]');
  } else {
    nav.classList.remove('bg-blay', 'transition-all', 'duration-[0.25s]');
  }
}

function getOffset() {
  if (window.screen.width >= 640) {
    nav.classList.remove('bg-blay');
    if (window.pageYOffset > offset) {
      navChangeColor();
    }
    if (window.pageYOffset < offset) {
      navChangeColor(false);
      nav.style.transition = 'background .25s ease-out';
    }
  }
}

getOffset();

window.addEventListener('scroll', getOffset);

window.addEventListener('resize', () => {
  if (window.screen.width < 640) {
    nav.classList.add('bg-blay');
  } else {
    nav.classList.remove('bg-blay');
  }
}, true);
