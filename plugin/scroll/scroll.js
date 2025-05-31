const RevealScroll = {
    id: 'scroll',
    init: function (deck) {
      deck.on('ready', () => enableSlideScroll(deck));
      deck.on('slidechanged', () => enableSlideScroll(deck));
    }
  };
  
  function enableSlideScroll(deck) {
    const currentSlide = deck.getCurrentSlide();
    if (!currentSlide) return;
  
    const scrollable = currentSlide.querySelector('.scrollable-slide');
    if (scrollable) {
      scrollable.style.overflowY = 'auto';
      scrollable.style.maxHeight = '70vh';
      scrollable.scrollTop = 0;
    }
  }
  
  // No export — define in global scope
  window.RevealScroll = RevealScroll;
  