class ReadMore {
  init(height, textSelector, btnSelector) {
    const text = document.querySelector(textSelector);
    const btn = document.querySelector(btnSelector);

    if (text.clientHeight < height) {
      btn.readMore = false;
      text.style.height = 'auto';
      btn.style.display = 'none';
    } else {
      text.style.height = height;
      btn.addEventListener('click', this.trigger, false);
      btn.height = height;
      btn.textSelector = textSelector;
      btn.readMore = true;
    }
  }

  trigger(e) {
    e.preventDefault();
    if (e.currentTarget.readMore === true) {
      document.querySelector(e.currentTarget.textSelector).style.height = 'auto';
      this.innerText = 'Read less';
      e.currentTarget.readMore = false;
    } else {
      document.querySelector(e.currentTarget.textSelector).style.height = e.currentTarget.height;
      this.innerText = 'Read more';
      e.currentTarget.readMore = true;
    }
  }
}

new ReadMore().init('193.6px', '.manga-description', '#readmore');
