document.addEventListener('DOMContentLoaded', () => {
    const notificationContainer = document.querySelector('.notification-container') as HTMLDivElement;
    const notificationNewLabel = document.getElementById('notification-new-label');
    const scrollToBottomButton = document.getElementById('notification-scroll-to-bottom');
    const scrollToBottomButtonSvg = document.getElementById('scroll-on-bottom-svg');
    const scrollToBottomButtonMessageCount = document.getElementById('scroll-on-bottom-messages-count');

    let scrollOnBottom = false;
    let newMessagesCount = 0;

    const setIsScrollOnBottom = () => {
        scrollOnBottom = notificationContainer.scrollTop >= notificationContainer.scrollHeight - notificationContainer.clientHeight;
    }

    notificationContainer.addEventListener('scroll', () => {
        setIsScrollOnBottom();

        if (newMessagesCount > 0) {
            scrollToBottomButtonSvg.classList.add('hidden');
            scrollToBottomButtonMessageCount.classList.remove('hidden');
        } else {
            scrollToBottomButtonSvg.classList.remove('hidden');
            scrollToBottomButtonMessageCount.classList.add('hidden');
        }

        if (scrollOnBottom) {
            scrollToBottomButton.classList.add('hidden');
            newMessagesCount = 0;
        } else {
            scrollToBottomButton.classList.remove('hidden');
        }
    });

    scrollToBottomButton.addEventListener('click', () => {
        notificationContainer.scrollTo(0, notificationContainer.scrollHeight);
    });

    document.addEventListener('htmx:beforeSwap', () => {
        setIsScrollOnBottom();
    })

    document.addEventListener('htmx:load', (e) => {
        const targetElement = e.target as HTMLElement;

        if (targetElement.classList.contains('new-notification')) {
            // Show the new notification label if hidden
            if (notificationNewLabel.classList.contains('hidden')) {
                notificationNewLabel.classList.remove('hidden');
                notificationNewLabel.classList.add('flex');
            }

            if (scrollOnBottom){
                notificationContainer.scrollTo(0, notificationContainer.scrollHeight);
            } 

            newMessagesCount++;
            scrollToBottomButtonMessageCount.innerText = newMessagesCount.toString();

            scrollToBottomButtonSvg.classList.add('hidden');
            scrollToBottomButtonMessageCount.classList.remove('hidden');
        } else {
            notificationContainer.scrollTo(0, targetElement.scrollHeight * 5);
        }

    });

    // sse setup
    const userUuidInput = document.getElementById('user-uuid') as HTMLInputElement;
    const userUuid = userUuidInput.value;

    const eventSource = new EventSource('/sse'.concat(`?channel=room:${userUuid}`));
    eventSource.onmessage = (evt) => {
        console.log(evt);
    }
});