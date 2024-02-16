document.addEventListener('DOMContentLoaded', () => {
    const userUuidInput = document.getElementById('user-uuid') as HTMLInputElement;
    const userUuid = userUuidInput.value;
    
    const channelQueryParameters = new URLSearchParams({
        channel: "notification:".concat(userUuid),
    });

    const sseEventSource = new EventSource('/sse'.concat("?", channelQueryParameters.toString()));
    const unreadNotificationCountDiv = document.getElementById('unread-notifications-count') as HTMLDivElement;

    let unreadNotificationCount = parseInt(unreadNotificationCountDiv.innerText);

    sseEventSource.onmessage = (evt) => {
        unreadNotificationCount += 1;
        unreadNotificationCountDiv.innerText = unreadNotificationCount.toString();
    }
});