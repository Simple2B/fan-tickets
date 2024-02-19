import {createChatWindow, setNewRoomUuid} from './chat';
import {listenNewRoom} from './dispute';
import * as htmx from 'htmx.org';

const disputeNotifications = ['dispute_created', 'new_post'];

document.addEventListener('htmx:load', e => {
  const target = e.target as HTMLDivElement;

  if (target.classList.contains('notification-item')) {
    console.log('notification-item loaded');

    // Update notifications unread count
    htmx.trigger(
      '#unread-notifications-count',
      'update_unread_notifications_count',
    );

    const notificationType = target.getAttribute('data-notification-type');
    if (disputeNotifications.includes(notificationType)) {
      target.addEventListener('click', () => {
        const notificationDataElement =
          target.querySelector('.notification-data');
        const roomUuid = notificationDataElement.getAttribute('data-room-uuid');
        createChatWindow();
        listenNewRoom(roomUuid);
        setNewRoomUuid(roomUuid);
      });
    }
  }
});
