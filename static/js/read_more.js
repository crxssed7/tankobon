// This code is all for the 'Read more' button on the manga description
let readMore = true;
const emToPx = 193.6;

if (document.querySelector('.manga-description').clientHeight < emToPx) {
  readMore = false;
  document.querySelector('.manga-description').style.height = 'auto';
  document.querySelector('#readmore').style.display = 'none';
} else {
  document.querySelector('.manga-description').style.height = '12.1em';
  document.querySelector('#readmore').addEventListener('click', (e) => {
    e.preventDefault();
    if (readMore === true) {
      document.querySelector('.manga-description').style.height = 'auto';
      this.innerText = 'Read less';
      readMore = false;
    } else {
      document.querySelector('.manga-description').style.height = '12.1em';
      this.innerText = 'Read more';
      readMore = true;
    }
  });
}
