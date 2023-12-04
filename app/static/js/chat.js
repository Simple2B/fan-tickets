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
    });
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvY2hhdC5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsRUFBRTtJQUM1QyxJQUFNLFFBQVEsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLFlBQVksQ0FBQyxDQUFDO0lBQ3RELElBQU0sVUFBVSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsY0FBYyxDQUFDLENBQUM7SUFDMUQsSUFBTSxRQUFRLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyxpQkFBaUIsQ0FBQyxDQUFDO0lBQzNELElBQU0sU0FBUyxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsa0JBQWtCLENBQUMsQ0FBQztJQUU3RCxRQUFRLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1FBQ2pDLG1EQUFtRDtRQUNuRCxrREFBa0Q7UUFDbEQsVUFBVSxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsbUJBQW1CLENBQUMsQ0FBQztRQUNqRCxVQUFVLENBQUMsU0FBUyxDQUFDLE1BQU0sQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO0lBQ2xELENBQUMsQ0FBQyxDQUFDO0FBQ0wsQ0FBQyxDQUFDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvY2hhdC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgKCkgPT4ge1xuICBjb25zdCBjaGF0SWNvbiA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWljb24nKTtcbiAgY29uc3QgY2hhdFdpbmRvdyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LXdpbmRvdycpO1xuICBjb25zdCBvcGVuSWNvbiA9IGNoYXRJY29uLnF1ZXJ5U2VsZWN0b3IoJy5jaGF0LWljb24tb3BlbicpO1xuICBjb25zdCBjbG9zZUljb24gPSBjaGF0SWNvbi5xdWVyeVNlbGVjdG9yKCcuY2hhdC1pY29uLWNsb3NlJyk7XG5cbiAgY2hhdEljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgLy8gb3Blbkljb24uY2xhc3NMaXN0LnRvZ2dsZSgnY2hhdC1pY29uLWluYWN0aXZlJyk7XG4gICAgLy8gY2xvc2VJY29uLmNsYXNzTGlzdC50b2dnbGUoJ2NoYXQtaWNvbi1hY3RpdmUnKTtcbiAgICBjaGF0V2luZG93LmNsYXNzTGlzdC50b2dnbGUoJ2NoYXQtd2luZG93LWNsb3NlJyk7XG4gICAgY2hhdFdpbmRvdy5jbGFzc0xpc3QudG9nZ2xlKCdjaGF0LXdpbmRvdy1vcGVuJyk7XG4gIH0pO1xufSk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=