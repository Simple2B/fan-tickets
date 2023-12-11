document.addEventListener('DOMContentLoaded', () => {
  const chatIcon = document.querySelector('#chat-icon');
  const chatWindow = document.querySelector('#chat-window');
  const openIcon = chatIcon.querySelector('.chat-icon-open');
  const closeIcon = chatIcon.querySelector('.chat-icon-close');
  const locationButton = document.querySelector('#chat-sell-location-button');

  chatIcon.addEventListener('click', () => {
    // openIcon.classList.toggle('chat-icon-inactive');
    // closeIcon.classList.toggle('chat-icon-active');
    chatWindow.classList.toggle('chat-window-close');
    chatWindow.classList.toggle('chat-window-open');

    chatWindow.scrollTo({
      top: chatWindow.scrollHeight,
      behavior: 'smooth',
    });

    const observer = new MutationObserver(mutations => {
      const locationButton = document.querySelector(
        '#chat-sell-location-button',
      );
      if (locationButton) {
        locationButton.addEventListener('click', () => {});
      }

      mutations.forEach(mutation => {
        chatWindow.scrollTo({
          top: chatWindow.scrollHeight,
          behavior: 'smooth',
        });
      });
    });

    observer.observe(chatWindow, {childList: true});
  });
});
