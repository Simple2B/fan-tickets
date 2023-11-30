document.addEventListener('DOMContentLoaded', () => {
  const chatIcon = document.querySelector('#chat-icon');
  const chatWindow = document.querySelector('#chat-window');
  const openIcon = chatIcon.querySelector('.chat-icon-open');
  const closeIcon = chatIcon.querySelector('.chat-icon-close');

  chatIcon.addEventListener('click', () => {
    console.log('chat-icon clicked');
    // openIcon.classList.toggle('chat-icon-inactive');
    // closeIcon.classList.toggle('chat-icon-active');
    chatWindow.classList.toggle('chat-window-close');
    chatWindow.classList.toggle('chat-window-open');
  });
});
