/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!*********************!*\
  !*** ./src/chat.ts ***!
  \*********************/
document.addEventListener('DOMContentLoaded', function () {
    var chatIcon = document.querySelector('#chat-icon');
    var chatWindow = document.querySelector('#chat-window');
    var openIcon = chatIcon.querySelector('.chat-icon-open');
    var closeIcon = chatIcon.querySelector('.chat-icon-close');
    var locationButton = document.querySelector('#chat-sell-location-button');
    chatIcon.addEventListener('click', function () {
        // openIcon.classList.toggle('chat-icon-inactive');
        // closeIcon.classList.toggle('chat-icon-active');
        chatWindow.classList.toggle('chat-window-close');
        chatWindow.classList.toggle('chat-window-open');
        chatWindow.scrollTo({
            top: chatWindow.scrollHeight,
            behavior: 'smooth',
        });
        var observer = new MutationObserver(function (mutations) {
            var locationButton = document.querySelector('#chat-sell-location-button');
            if (locationButton) {
                locationButton.addEventListener('click', function () { });
            }
            mutations.forEach(function (mutation) {
                chatWindow.scrollTo({
                    top: chatWindow.scrollHeight,
                    behavior: 'smooth',
                });
            });
        });
        observer.observe(chatWindow, { childList: true });
    });
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvY2hhdC5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsRUFBRTtJQUM1QyxJQUFNLFFBQVEsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLFlBQVksQ0FBQyxDQUFDO0lBQ3RELElBQU0sVUFBVSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsY0FBYyxDQUFDLENBQUM7SUFDMUQsSUFBTSxRQUFRLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyxpQkFBaUIsQ0FBQyxDQUFDO0lBQzNELElBQU0sU0FBUyxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsa0JBQWtCLENBQUMsQ0FBQztJQUM3RCxJQUFNLGNBQWMsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLDRCQUE0QixDQUFDLENBQUM7SUFFNUUsUUFBUSxDQUFDLGdCQUFnQixDQUFDLE9BQU8sRUFBRTtRQUNqQyxtREFBbUQ7UUFDbkQsa0RBQWtEO1FBQ2xELFVBQVUsQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLG1CQUFtQixDQUFDLENBQUM7UUFDakQsVUFBVSxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsa0JBQWtCLENBQUMsQ0FBQztRQUVoRCxVQUFVLENBQUMsUUFBUSxDQUFDO1lBQ2xCLEdBQUcsRUFBRSxVQUFVLENBQUMsWUFBWTtZQUM1QixRQUFRLEVBQUUsUUFBUTtTQUNuQixDQUFDLENBQUM7UUFFSCxJQUFNLFFBQVEsR0FBRyxJQUFJLGdCQUFnQixDQUFDLG1CQUFTO1lBQzdDLElBQU0sY0FBYyxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQzNDLDRCQUE0QixDQUM3QixDQUFDO1lBQ0YsSUFBSSxjQUFjLEVBQUU7Z0JBQ2xCLGNBQWMsQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUUsY0FBTyxDQUFDLENBQUMsQ0FBQzthQUNwRDtZQUVELFNBQVMsQ0FBQyxPQUFPLENBQUMsa0JBQVE7Z0JBQ3hCLFVBQVUsQ0FBQyxRQUFRLENBQUM7b0JBQ2xCLEdBQUcsRUFBRSxVQUFVLENBQUMsWUFBWTtvQkFDNUIsUUFBUSxFQUFFLFFBQVE7aUJBQ25CLENBQUMsQ0FBQztZQUNMLENBQUMsQ0FBQyxDQUFDO1FBQ0wsQ0FBQyxDQUFDLENBQUM7UUFFSCxRQUFRLENBQUMsT0FBTyxDQUFDLFVBQVUsRUFBRSxFQUFDLFNBQVMsRUFBRSxJQUFJLEVBQUMsQ0FBQyxDQUFDO0lBQ2xELENBQUMsQ0FBQyxDQUFDO0FBQ0wsQ0FBQyxDQUFDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvY2hhdC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgKCkgPT4ge1xuICBjb25zdCBjaGF0SWNvbiA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWljb24nKTtcbiAgY29uc3QgY2hhdFdpbmRvdyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LXdpbmRvdycpO1xuICBjb25zdCBvcGVuSWNvbiA9IGNoYXRJY29uLnF1ZXJ5U2VsZWN0b3IoJy5jaGF0LWljb24tb3BlbicpO1xuICBjb25zdCBjbG9zZUljb24gPSBjaGF0SWNvbi5xdWVyeVNlbGVjdG9yKCcuY2hhdC1pY29uLWNsb3NlJyk7XG4gIGNvbnN0IGxvY2F0aW9uQnV0dG9uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtc2VsbC1sb2NhdGlvbi1idXR0b24nKTtcblxuICBjaGF0SWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAvLyBvcGVuSWNvbi5jbGFzc0xpc3QudG9nZ2xlKCdjaGF0LWljb24taW5hY3RpdmUnKTtcbiAgICAvLyBjbG9zZUljb24uY2xhc3NMaXN0LnRvZ2dsZSgnY2hhdC1pY29uLWFjdGl2ZScpO1xuICAgIGNoYXRXaW5kb3cuY2xhc3NMaXN0LnRvZ2dsZSgnY2hhdC13aW5kb3ctY2xvc2UnKTtcbiAgICBjaGF0V2luZG93LmNsYXNzTGlzdC50b2dnbGUoJ2NoYXQtd2luZG93LW9wZW4nKTtcblxuICAgIGNoYXRXaW5kb3cuc2Nyb2xsVG8oe1xuICAgICAgdG9wOiBjaGF0V2luZG93LnNjcm9sbEhlaWdodCxcbiAgICAgIGJlaGF2aW9yOiAnc21vb3RoJyxcbiAgICB9KTtcblxuICAgIGNvbnN0IG9ic2VydmVyID0gbmV3IE11dGF0aW9uT2JzZXJ2ZXIobXV0YXRpb25zID0+IHtcbiAgICAgIGNvbnN0IGxvY2F0aW9uQnV0dG9uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAgICAgJyNjaGF0LXNlbGwtbG9jYXRpb24tYnV0dG9uJyxcbiAgICAgICk7XG4gICAgICBpZiAobG9jYXRpb25CdXR0b24pIHtcbiAgICAgICAgbG9jYXRpb25CdXR0b24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7fSk7XG4gICAgICB9XG5cbiAgICAgIG11dGF0aW9ucy5mb3JFYWNoKG11dGF0aW9uID0+IHtcbiAgICAgICAgY2hhdFdpbmRvdy5zY3JvbGxUbyh7XG4gICAgICAgICAgdG9wOiBjaGF0V2luZG93LnNjcm9sbEhlaWdodCxcbiAgICAgICAgICBiZWhhdmlvcjogJ3Ntb290aCcsXG4gICAgICAgIH0pO1xuICAgICAgfSk7XG4gICAgfSk7XG5cbiAgICBvYnNlcnZlci5vYnNlcnZlKGNoYXRXaW5kb3csIHtjaGlsZExpc3Q6IHRydWV9KTtcbiAgfSk7XG59KTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==