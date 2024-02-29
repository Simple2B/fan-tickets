import {resizeChat, scrollDown} from './utils';
import {
  toggleChatWindow,
  chatMessageContainer,
  showMessage,
  chatWindow,
} from './chat';

document.addEventListener('DOMContentLoaded', () => {
  const chatIcon = document.querySelector('#chat-icon');
  // const chatIconClose = document.querySelector('#chat-icon-close');
  const chatMain = document.querySelector('#chat-main') as HTMLDivElement;

  chatIcon.addEventListener('click', () => {
    setTimeout(() => {
      resizeChat();
    }, 200);
    toggleChatWindow();
    // chatIcon.classList.toggle('hidden');
    if (chatWindow.classList.contains('chat-window-open')) {
      showMessage();
      scrollDown(chatMain);
    } else {
      const chatMessages =
        chatMessageContainer.querySelectorAll('.chat-message');
      chatMessages.forEach(message => {
        message.classList.remove('chat-message-active');
      });
    }

    const observer = new MutationObserver(mutations => {
      const locationButton = document.querySelector(
        '#chat-sell-location-button',
      );
      if (locationButton) {
        locationButton.addEventListener('click', () => {});
      }

      mutations.forEach(mutation => {
        if (mutation.type === 'childList') {
          scrollDown(chatMain);
        }
      });
    });

    observer.observe(chatMain, {childList: true});
  });
});
