import {setMessageSendUrl, createChatWindow, setNewRoomUuid} from './chat';
import {listenNewRoom} from './dispute';

setMessageSendUrl('/disputes/send');

document.addEventListener('DOMContentLoaded', () => {
  const startDisputeButtonList =
    document.querySelectorAll('.start-dispute-btn');
  startDisputeButtonList.forEach(button =>
    button.addEventListener('click', async () => {
      const messages = document.querySelectorAll('.chat-dispute-messages');

      createChatWindow();

      if (messages.length === 0) {
        const chatSpinner = document.querySelector('.chat-spinner');
        const spinnerClone = chatSpinner.cloneNode(true) as HTMLDivElement;
        const chatMessageContainer = document.querySelector(
          '#chat-message-container',
        );
        chatMessageContainer.appendChild(spinnerClone);
        spinnerClone.classList.remove('hidden');
        spinnerClone.style.display = 'flex';
        spinnerClone.classList.add('chat-spinner-active');
      }

      const paymentId = button.getAttribute('data-payment-id');
      const resp = await fetch('/disputes/?payment_id='.concat(paymentId));
      const roomUuid = await resp.text();
      listenNewRoom(roomUuid);
      setNewRoomUuid(roomUuid);
    }),
  );

  const paymentIcons = document.querySelectorAll('.payment-icon');
  paymentIcons.forEach(icon => {
    const hint = icon.querySelector('.payment-hint');
    icon.addEventListener('mouseover', () => {
      if (hint) {
        hint.classList.remove('hidden');
      }
    });
    icon.addEventListener('mouseleave', () => {
      if (hint) {
        hint.classList.add('hidden');
      }
    });
  });
});
