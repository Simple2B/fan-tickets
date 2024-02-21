import {setMessageSendUrl, createChatWindow, setNewRoomUuid} from './chat';
import {listenNewRoom} from './dispute';

setMessageSendUrl('/disputes/send');

document.addEventListener('DOMContentLoaded', () => {
  const startDisputeButtonList =
    document.querySelectorAll('.start-dispute-btn');
  startDisputeButtonList.forEach(button =>
    button.addEventListener('click', async () => {
      createChatWindow();
      const paymentId = button.getAttribute('data-payment-id');
      const resp = await fetch('/disputes/?payment_id='.concat(paymentId));
      const roomUuid = await resp.text();
      listenNewRoom(roomUuid);
      setNewRoomUuid(roomUuid);
    }),
  );
});
