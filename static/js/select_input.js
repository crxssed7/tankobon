const searchInput = document.getElementById('main-search');

window.addEventListener('keyup', (e) => {
  if (e.key === '/') {
    searchInput.focus();
  }
});
