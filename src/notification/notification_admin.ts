import * as htmx from 'htmx.org';
import {Notification} from './schema';
import {createChatWindow, setNewRoomUuid} from '../chat';
import {listenNewRoom} from '../dispute';

interface NewDisputeNotificationPayload {
  room_uuid: string;
}

document.addEventListener('DOMContentLoaded', () => {
  // Dispute buttons
  const disputesList = document.querySelectorAll(
    '.dispute-tr-element',
  ) as NodeListOf<HTMLTableRowElement>;
  disputesList.forEach(dispute =>
    dispute.addEventListener('click', () => {
      const roomUuid = dispute.getAttribute('data-room-uuid');

      createChatWindow();
      listenNewRoom(roomUuid);
      setNewRoomUuid(roomUuid);
    }),
  );

  const channelQueryParameters = new URLSearchParams({
    channel: 'admin',
  });

  const eventSource = new EventSource(
    '/sse'.concat('?', channelQueryParameters.toString()),
  );

  const newNotificationInput = document.querySelector(
    'input[name="notification_uuid"]',
  ) as HTMLInputElement;
  eventSource.onmessage = evt => {
    const notificationData: Notification = JSON.parse(evt.data);
    newNotificationInput.value = notificationData.uuid;
    htmx.trigger('#notification_loader', 'load_notification');
  };

  document.addEventListener('htmx:load', e => {
    let target = e.target as HTMLElement;

    if (target.classList.contains('new-notification')) {
      target = target.children[0] as HTMLElement;
    }

    if (target.classList.contains('notification-dispute-created')) {
      target.addEventListener('click', e => {
        const {room_uuid} = JSON.parse(
          target.getAttribute('data-notification-payload'),
        ) as NewDisputeNotificationPayload;
        createChatWindow();
        listenNewRoom(room_uuid);
        setNewRoomUuid(room_uuid);
      });
    }
  });
});
