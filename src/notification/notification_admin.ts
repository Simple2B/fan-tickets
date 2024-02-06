import { Notification } from './schema';

document.addEventListener('DOMContentLoaded', () => {
    const channelQueryParameters = new URLSearchParams({
        channel: "admin",
    });

    const eventSource = new EventSource('/sse'.concat("?", channelQueryParameters.toString()));

    const newNotificationInput = document.querySelector('input[name="notification_uuid"]') as HTMLInputElement;
    eventSource.onmessage = (evt) => {
        const notificationData: Notification = JSON.parse(evt.data);
        newNotificationInput.value = notificationData.uuid;
        htmx.trigger('#notification_loader', "load_notification");
    }
});