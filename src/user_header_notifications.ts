import * as htmx from 'htmx.org';

document.addEventListener('DOMContentLoaded', () => {
  const userUuidInput = document.getElementById(
    'user-uuid',
  ) as HTMLInputElement;
  const userUuid = userUuidInput.value;
  const notificationIndicator = document.getElementById(
    'new-notifications-indicator',
  ) as HTMLDivElement;

  const channelQueryParameters = new URLSearchParams({
    channel: 'notification:'.concat(userUuid),
  });

  const sseEventSource = new EventSource(
    '/sse'.concat('?', channelQueryParameters.toString()),
  );
  const unreadNotificationCountDiv = document.getElementById(
    'unread-notifications-count',
  ) as HTMLDivElement;

  let unreadNotificationCount = parseInt(unreadNotificationCountDiv.innerText);

  sseEventSource.onmessage = evt => {
    notificationIndicator.classList.remove('hidden');
    unreadNotificationCountDiv.classList.remove('hidden');
    htmx.trigger(
      '#unread-notifications-count',
      'update_unread_notifications_count',
    );
    unreadNotificationCountDiv.innerText = unreadNotificationCount.toString();
  };

  document.addEventListener('htmx:afterSwap', e => {
    const target = e.target as HTMLDivElement;

    if (target.getAttribute('id') === 'unread-notifications-count') {
      const notificationCount = parseInt(target.innerText);

      if (notificationCount === 0) {
        unreadNotificationCountDiv.classList.add('hidden');
        notificationIndicator.classList.add('hidden');
      }
    }
  });
});
