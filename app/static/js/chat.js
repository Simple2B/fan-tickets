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
    chatIcon.addEventListener('click', function () {
        // openIcon.classList.toggle('chat-icon-inactive');
        // closeIcon.classList.toggle('chat-icon-active');
        chatWindow.classList.toggle('chat-window-close');
        chatWindow.classList.toggle('chat-window-open');
        var observer = new MutationObserver(function (mutations) {
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvY2hhdC5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsRUFBRTtJQUM1QyxJQUFNLFFBQVEsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLFlBQVksQ0FBQyxDQUFDO0lBQ3RELElBQU0sVUFBVSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsY0FBYyxDQUFDLENBQUM7SUFDMUQsSUFBTSxRQUFRLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyxpQkFBaUIsQ0FBQyxDQUFDO0lBQzNELElBQU0sU0FBUyxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsa0JBQWtCLENBQUMsQ0FBQztJQUU3RCxRQUFRLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1FBQ2pDLG1EQUFtRDtRQUNuRCxrREFBa0Q7UUFDbEQsVUFBVSxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsbUJBQW1CLENBQUMsQ0FBQztRQUNqRCxVQUFVLENBQUMsU0FBUyxDQUFDLE1BQU0sQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO1FBRWhELElBQU0sUUFBUSxHQUFHLElBQUksZ0JBQWdCLENBQUMsbUJBQVM7WUFDN0MsU0FBUyxDQUFDLE9BQU8sQ0FBQyxrQkFBUTtnQkFDeEIsVUFBVSxDQUFDLFFBQVEsQ0FBQztvQkFDbEIsR0FBRyxFQUFFLFVBQVUsQ0FBQyxZQUFZO29CQUM1QixRQUFRLEVBQUUsUUFBUTtpQkFDbkIsQ0FBQyxDQUFDO1lBQ0wsQ0FBQyxDQUFDLENBQUM7UUFDTCxDQUFDLENBQUMsQ0FBQztRQUVILFFBQVEsQ0FBQyxPQUFPLENBQUMsVUFBVSxFQUFFLEVBQUMsU0FBUyxFQUFFLElBQUksRUFBQyxDQUFDLENBQUM7SUFDbEQsQ0FBQyxDQUFDLENBQUM7QUFDTCxDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy9jaGF0LnRzIl0sInNvdXJjZXNDb250ZW50IjpbImRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCAoKSA9PiB7XG4gIGNvbnN0IGNoYXRJY29uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtaWNvbicpO1xuICBjb25zdCBjaGF0V2luZG93ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtd2luZG93Jyk7XG4gIGNvbnN0IG9wZW5JY29uID0gY2hhdEljb24ucXVlcnlTZWxlY3RvcignLmNoYXQtaWNvbi1vcGVuJyk7XG4gIGNvbnN0IGNsb3NlSWNvbiA9IGNoYXRJY29uLnF1ZXJ5U2VsZWN0b3IoJy5jaGF0LWljb24tY2xvc2UnKTtcblxuICBjaGF0SWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAvLyBvcGVuSWNvbi5jbGFzc0xpc3QudG9nZ2xlKCdjaGF0LWljb24taW5hY3RpdmUnKTtcbiAgICAvLyBjbG9zZUljb24uY2xhc3NMaXN0LnRvZ2dsZSgnY2hhdC1pY29uLWFjdGl2ZScpO1xuICAgIGNoYXRXaW5kb3cuY2xhc3NMaXN0LnRvZ2dsZSgnY2hhdC13aW5kb3ctY2xvc2UnKTtcbiAgICBjaGF0V2luZG93LmNsYXNzTGlzdC50b2dnbGUoJ2NoYXQtd2luZG93LW9wZW4nKTtcblxuICAgIGNvbnN0IG9ic2VydmVyID0gbmV3IE11dGF0aW9uT2JzZXJ2ZXIobXV0YXRpb25zID0+IHtcbiAgICAgIG11dGF0aW9ucy5mb3JFYWNoKG11dGF0aW9uID0+IHtcbiAgICAgICAgY2hhdFdpbmRvdy5zY3JvbGxUbyh7XG4gICAgICAgICAgdG9wOiBjaGF0V2luZG93LnNjcm9sbEhlaWdodCxcbiAgICAgICAgICBiZWhhdmlvcjogJ3Ntb290aCcsXG4gICAgICAgIH0pO1xuICAgICAgfSk7XG4gICAgfSk7XG5cbiAgICBvYnNlcnZlci5vYnNlcnZlKGNoYXRXaW5kb3csIHtjaGlsZExpc3Q6IHRydWV9KTtcbiAgfSk7XG59KTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==