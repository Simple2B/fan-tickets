import {resizeChat, scrollDown} from './utils';
import {
  toggleChatWindow,
  chatMessageContainer,
  showMessage,
  chatWindow,
} from './chat';

document.addEventListener('DOMContentLoaded', () => {
  const chatIcon = document.querySelector('#chat-icon');
  const chatMain = document.querySelector('#chat-main') as HTMLDivElement;

  chatIcon.addEventListener('click', () => {
    setTimeout(() => {
      console.log('chat icon clicked inside chat_button_open');

      resizeChat();
    }, 200);
    toggleChatWindow();
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
