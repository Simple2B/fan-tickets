import { scrollDown, scrollDownSmooth, resizeChat } from './utils';
import * as htmx from 'htmx.org'

const timeTyping = 1500;
export let chatWindow: HTMLDivElement;
export let chatMessageContainer: HTMLDivElement;

console.log('chat.js')

let roomUuidInput: HTMLInputElement;
let messageSendUrl: string;

export function setNewRoomUuid(roomUuid: string) {
  roomUuidInput.value = roomUuid;
  htmx.trigger('#message_history_loader', 'load_message_history')
}

export function setMessageSendUrl(url: string) {
  messageSendUrl = url;
}

export function toggleChatWindow() {
  chatWindow.classList.toggle('chat-window-close');
  chatWindow.classList.toggle('chat-window-open');
}

function closeChatWindow() {
  chatWindow.classList.remove('chat-window-open');
  chatWindow.classList.add('chat-window-close');
}

export function openChatWindow () {
  chatWindow.classList.remove('chat-window-close');
  chatWindow.classList.add('chat-window-open');
}

export function createChatWindow() {
  const messages = document.querySelectorAll('.chat-dispute-messages');
  messages.forEach(message => message.remove());

  const newMessages = document.querySelectorAll('.new_message');
  newMessages.forEach(message => message.remove());

  openChatWindow();
}

export async function showMessage() {
  const chatMessages = chatMessageContainer.querySelectorAll('.chat-message');
  const chatSpinner: HTMLDivElement = document.querySelector('.chat-spinner');

  if (!chatMessages || !chatSpinner) return;

  for (let index = 0; index < chatMessages.length; index++) {
    const message = chatMessages[index];
    await showSpinnerAndMessage(message, chatSpinner);
  }
}

async function showSpinnerAndMessage(
  message: Element,
  chatSpinner: HTMLDivElement,
) {
  const spinnerClone = chatSpinner.cloneNode(true) as HTMLDivElement;
  const chatMain: HTMLDivElement = document.querySelector('#chat-main');

  message.parentNode.insertBefore(spinnerClone, message);

  spinnerClone.style.display = 'flex';
  spinnerClone.classList.add('chat-spinner-active');
  scrollDown(chatMain);

  await new Promise(resolve => setTimeout(resolve, timeTyping));

  spinnerClone.remove();
  message.classList.add('chat-message-active');
  scrollDownSmooth(chatMain);
}

// HTMX chat handler
document.addEventListener('DOMContentLoaded', () => {  
  // Nodes
  const chatCloseButton = document.querySelector('#chat-close-button') as HTMLButtonElement;
  const chatMain = document.getElementById('chat-main') as HTMLDivElement;
  const chatHeaderTitle = document.getElementById('chat-header-title') as HTMLSpanElement;
  const chatCloseButtons = document.querySelectorAll('.chat-close-button') as NodeListOf<HTMLButtonElement>;
  const sendMessageButton = document.getElementById('message-send-button') as HTMLButtonElement;
  const messageInput = document.getElementById('chat-get') as HTMLInputElement;
  
  roomUuidInput = document.querySelector('[name="room_uuid"]') as HTMLInputElement;

  chatWindow = document.querySelector('#chat-window') as HTMLDivElement;
  chatMessageContainer = document.querySelector('#chat-message-container');

  // Handlers
  if (chatMessageContainer.hasAttribute('data-send-message')) {
    showMessage();
  }

  chatCloseButton.addEventListener('click', closeChatWindow);

  document.addEventListener('htmx:beforeRequest', e => {
    const targetElement = e.target as HTMLElement;
    // Change chat title
    if (targetElement.classList.contains('start-dispute-btn')){
      chatHeaderTitle.innerHTML = 'Chat';
      openChatWindow();
    } 
  });

  document.addEventListener('htmx:load', (e) => {
    const targetElement = e.target as HTMLElement;

    if (targetElement.classList.contains('chat-dispute-messages')) {
      resizeChat();
      chatMain.scrollTo(0, targetElement.scrollHeight);
    }

    else if (targetElement.classList.contains('new_message')){
      chatMain.scrollTo(0, chatMain.scrollHeight);
    }
  })

  chatCloseButtons.forEach(button => button.addEventListener('click', () => toggleChatWindow));

  // send message button
  async function sendMessage() {
    const messageText = messageInput.value;
    const roomUuid = roomUuidInput.value;

    const formData = new FormData();
    formData.append('room_unique_id', roomUuid);
    formData.append('message', messageText);

    await fetch(messageSendUrl, {
        method: 'POST',
        body: formData,
    });
    messageInput.value = '';
  }

  sendMessageButton.addEventListener('click', sendMessage);
  document.addEventListener("keyup", async (event) => {
      switch(event.key) {
          case "Enter":
              await sendMessage();
          break;
      }

  });
});