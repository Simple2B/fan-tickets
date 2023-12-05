document.addEventListener('DOMContentLoaded', () => {
  const chatIcon = document.querySelector('#chat-icon');
  const chatWindow = document.querySelector('#chat-window');
  const openIcon = chatIcon.querySelector('.chat-icon-open');
  const closeIcon = chatIcon.querySelector('.chat-icon-close');

  chatIcon.addEventListener('click', () => {
    // openIcon.classList.toggle('chat-icon-inactive');
    // closeIcon.classList.toggle('chat-icon-active');
    chatWindow.classList.toggle('chat-window-close');
    chatWindow.classList.toggle('chat-window-open');
  });
  console.log('chat.ts loaded');
});

const observer = new MutationObserver(mutations => {
  mutations.forEach(mutation => {
    if (mutation.type === 'childList') {
      const chatWindow = document.querySelector('#chat-window');
      const chatMessages = chatWindow.querySelector('.chat-messages');
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  });
});

observer.observe(document.querySelector('.chat-messages'), {
  childList: true,
});

const chatForm = document.querySelector('#chat-form');
const chatInput = document.querySelector('#chat-input');
const chatMessages = document.querySelector('.chat-messages');
