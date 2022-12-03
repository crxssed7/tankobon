// This is a bloody mess. Try and find better examples online.
const nav = document.querySelector('.navbar');
const collapse = document.querySelector('.navbar-collapse');
const offset = 25;
// colored = nav.classList.contains('navbar-bg')
// opened = collapse.classList.contains('show')

function navChangeColor(colored = true) {
  if (colored) {
    nav.classList.add('navbar-bg');
  } else {
    nav.classList.remove('navbar-bg');
  }
}

function getOffset() {
  if (window.pageYOffset > offset) {
    navChangeColor();
  }
  if (window.pageYOffset < offset && collapse.classList.contains('show') === false && nav.classList.contains('navbar-bg') === true) {
    navChangeColor(false);
    nav.style.transition = 'background .1s ease-out';
  }
}

getOffset();

window.addEventListener('scroll', getOffset);
