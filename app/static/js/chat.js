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
        console.log('chat-icon clicked');
        // openIcon.classList.toggle('chat-icon-inactive');
        // closeIcon.classList.toggle('chat-icon-active');
        chatWindow.classList.toggle('chat-window-close');
        chatWindow.classList.toggle('chat-window-open');
    });
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvY2hhdC5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsRUFBRTtJQUM1QyxJQUFNLFFBQVEsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLFlBQVksQ0FBQyxDQUFDO0lBQ3RELElBQU0sVUFBVSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsY0FBYyxDQUFDLENBQUM7SUFDMUQsSUFBTSxRQUFRLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyxpQkFBaUIsQ0FBQyxDQUFDO0lBQzNELElBQU0sU0FBUyxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsa0JBQWtCLENBQUMsQ0FBQztJQUU3RCxRQUFRLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1FBQ2pDLE9BQU8sQ0FBQyxHQUFHLENBQUMsbUJBQW1CLENBQUMsQ0FBQztRQUNqQyxtREFBbUQ7UUFDbkQsa0RBQWtEO1FBQ2xELFVBQVUsQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLG1CQUFtQixDQUFDLENBQUM7UUFDakQsVUFBVSxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsa0JBQWtCLENBQUMsQ0FBQztJQUNsRCxDQUFDLENBQUMsQ0FBQztBQUNMLENBQUMsQ0FBQyxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL2NoYXQudHMiXSwic291cmNlc0NvbnRlbnQiOlsiZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsICgpID0+IHtcbiAgY29uc3QgY2hhdEljb24gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC1pY29uJyk7XG4gIGNvbnN0IGNoYXRXaW5kb3cgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC13aW5kb3cnKTtcbiAgY29uc3Qgb3Blbkljb24gPSBjaGF0SWNvbi5xdWVyeVNlbGVjdG9yKCcuY2hhdC1pY29uLW9wZW4nKTtcbiAgY29uc3QgY2xvc2VJY29uID0gY2hhdEljb24ucXVlcnlTZWxlY3RvcignLmNoYXQtaWNvbi1jbG9zZScpO1xuXG4gIGNoYXRJY29uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgIGNvbnNvbGUubG9nKCdjaGF0LWljb24gY2xpY2tlZCcpO1xuICAgIC8vIG9wZW5JY29uLmNsYXNzTGlzdC50b2dnbGUoJ2NoYXQtaWNvbi1pbmFjdGl2ZScpO1xuICAgIC8vIGNsb3NlSWNvbi5jbGFzc0xpc3QudG9nZ2xlKCdjaGF0LWljb24tYWN0aXZlJyk7XG4gICAgY2hhdFdpbmRvdy5jbGFzc0xpc3QudG9nZ2xlKCdjaGF0LXdpbmRvdy1jbG9zZScpO1xuICAgIGNoYXRXaW5kb3cuY2xhc3NMaXN0LnRvZ2dsZSgnY2hhdC13aW5kb3ctb3BlbicpO1xuICB9KTtcbn0pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9