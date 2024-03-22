/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!******************************************!*\
  !*** ./src/notification/notification.ts ***!
  \******************************************/
document.addEventListener('DOMContentLoaded', function () {
    var notificationContainer = document.querySelector('.notification-container');
    var notificationNewLabel = document.getElementById('notification-new-label');
    var scrollToBottomButton = document.getElementById('notification-scroll-to-bottom');
    var scrollToBottomButtonSvg = document.getElementById('scroll-on-bottom-svg');
    var scrollToBottomButtonMessageCount = document.getElementById('scroll-on-bottom-messages-count');
    var scrollOnBottom = false;
    var newMessagesCount = 0;
    var setIsScrollOnBottom = function () {
        scrollOnBottom = notificationContainer.scrollTop >= notificationContainer.scrollHeight - notificationContainer.clientHeight;
    };
    notificationContainer.addEventListener('scroll', function () {
        setIsScrollOnBottom();
        if (newMessagesCount > 0) {
            scrollToBottomButtonSvg.classList.add('hidden');
            scrollToBottomButtonMessageCount.classList.remove('hidden');
        }
        else {
            scrollToBottomButtonSvg.classList.remove('hidden');
            scrollToBottomButtonMessageCount.classList.add('hidden');
        }
        if (scrollOnBottom) {
            scrollToBottomButton.classList.add('hidden');
            newMessagesCount = 0;
        }
        else {
            scrollToBottomButton.classList.remove('hidden');
        }
    });
    scrollToBottomButton.addEventListener('click', function () {
        notificationContainer.scrollTo(0, notificationContainer.scrollHeight);
    });
    document.addEventListener('htmx:beforeSwap', function () {
        setIsScrollOnBottom();
    });
    document.addEventListener('htmx:load', function (e) {
        var targetElement = e.target;
        if (targetElement.classList.contains('new-notification')) {
            // Show the new notification label if hidden
            if (notificationNewLabel.classList.contains('hidden')) {
                notificationNewLabel.classList.remove('hidden');
                notificationNewLabel.classList.add('flex');
            }
            if (scrollOnBottom) {
                notificationContainer.scrollTo(0, notificationContainer.scrollHeight);
            }
            newMessagesCount++;
            scrollToBottomButtonMessageCount.innerText = newMessagesCount.toString();
            scrollToBottomButtonSvg.classList.add('hidden');
            scrollToBottomButtonMessageCount.classList.remove('hidden');
        }
        else {
            notificationContainer.scrollTo(0, targetElement.scrollHeight * 5);
        }
    });
    // sse setup
    var userUuidInput = document.getElementById('user-uuid');
    var userUuid = userUuidInput.value;
    var eventSource = new EventSource('/sse'.concat("?channel=room:".concat(userUuid)));
    eventSource.onmessage = function (evt) {
        console.log(evt);
    };
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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QUV6RSx1QkFBdUIsQ0FBQyxTQUFTLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxDQUFDO1lBQ2hELGdDQUFnQyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUM7U0FDL0Q7YUFBTTtZQUNILHFCQUFxQixDQUFDLFFBQVEsQ0FBQyxDQUFDLEVBQUUsYUFBYSxDQUFDLFlBQVksR0FBRyxDQUFDLENBQUMsQ0FBQztTQUNyRTtJQUVMLENBQUMsQ0FBQyxDQUFDO0lBRUgsWUFBWTtJQUNaLElBQU0sYUFBYSxHQUFHLFFBQVEsQ0FBQyxjQUFjLENBQUMsV0FBVyxDQUFxQixDQUFDO0lBQy9FLElBQU0sUUFBUSxHQUFHLGFBQWEsQ0FBQyxLQUFLLENBQUM7SUFFckMsSUFBTSxXQUFXLEdBQUcsSUFBSSxXQUFXLENBQUMsTUFBTSxDQUFDLE1BQU0sQ0FBQyx3QkFBaUIsUUFBUSxDQUFFLENBQUMsQ0FBQyxDQUFDO0lBQ2hGLFdBQVcsQ0FBQyxTQUFTLEdBQUcsVUFBQyxHQUFHO1FBQ3hCLE9BQU8sQ0FBQyxHQUFHLENBQUMsR0FBRyxDQUFDLENBQUM7SUFDckIsQ0FBQztBQUNMLENBQUMsQ0FBQyxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL25vdGlmaWNhdGlvbi9ub3RpZmljYXRpb24udHMiXSwic291cmNlc0NvbnRlbnQiOlsiZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsICgpID0+IHtcbiAgICBjb25zdCBub3RpZmljYXRpb25Db250YWluZXIgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcubm90aWZpY2F0aW9uLWNvbnRhaW5lcicpIGFzIEhUTUxEaXZFbGVtZW50O1xuICAgIGNvbnN0IG5vdGlmaWNhdGlvbk5ld0xhYmVsID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ25vdGlmaWNhdGlvbi1uZXctbGFiZWwnKTtcbiAgICBjb25zdCBzY3JvbGxUb0JvdHRvbUJ1dHRvbiA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdub3RpZmljYXRpb24tc2Nyb2xsLXRvLWJvdHRvbScpO1xuICAgIGNvbnN0IHNjcm9sbFRvQm90dG9tQnV0dG9uU3ZnID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3Njcm9sbC1vbi1ib3R0b20tc3ZnJyk7XG4gICAgY29uc3Qgc2Nyb2xsVG9Cb3R0b21CdXR0b25NZXNzYWdlQ291bnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc2Nyb2xsLW9uLWJvdHRvbS1tZXNzYWdlcy1jb3VudCcpO1xuXG4gICAgbGV0IHNjcm9sbE9uQm90dG9tID0gZmFsc2U7XG4gICAgbGV0IG5ld01lc3NhZ2VzQ291bnQgPSAwO1xuXG4gICAgY29uc3Qgc2V0SXNTY3JvbGxPbkJvdHRvbSA9ICgpID0+IHtcbiAgICAgICAgc2Nyb2xsT25Cb3R0b20gPSBub3RpZmljYXRpb25Db250YWluZXIuc2Nyb2xsVG9wID49IG5vdGlmaWNhdGlvbkNvbnRhaW5lci5zY3JvbGxIZWlnaHQgLSBub3RpZmljYXRpb25Db250YWluZXIuY2xpZW50SGVpZ2h0O1xuICAgIH1cblxuICAgIG5vdGlmaWNhdGlvbkNvbnRhaW5lci5hZGRFdmVudExpc3RlbmVyKCdzY3JvbGwnLCAoKSA9PiB7XG4gICAgICAgIHNldElzU2Nyb2xsT25Cb3R0b20oKTtcblxuICAgICAgICBpZiAobmV3TWVzc2FnZXNDb3VudCA+IDApIHtcbiAgICAgICAgICAgIHNjcm9sbFRvQm90dG9tQnV0dG9uU3ZnLmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuICAgICAgICAgICAgc2Nyb2xsVG9Cb3R0b21CdXR0b25NZXNzYWdlQ291bnQuY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBzY3JvbGxUb0JvdHRvbUJ1dHRvblN2Zy5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcbiAgICAgICAgICAgIHNjcm9sbFRvQm90dG9tQnV0dG9uTWVzc2FnZUNvdW50LmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuICAgICAgICB9XG5cbiAgICAgICAgaWYgKHNjcm9sbE9uQm90dG9tKSB7XG4gICAgICAgICAgICBzY3JvbGxUb0JvdHRvbUJ1dHRvbi5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgICAgICAgICAgIG5ld01lc3NhZ2VzQ291bnQgPSAwO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgc2Nyb2xsVG9Cb3R0b21CdXR0b24uY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7XG4gICAgICAgIH1cbiAgICB9KTtcblxuICAgIHNjcm9sbFRvQm90dG9tQnV0dG9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgICBub3RpZmljYXRpb25Db250YWluZXIuc2Nyb2xsVG8oMCwgbm90aWZpY2F0aW9uQ29udGFpbmVyLnNjcm9sbEhlaWdodCk7XG4gICAgfSk7XG5cbiAgICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdodG14OmJlZm9yZVN3YXAnLCAoKSA9PiB7XG4gICAgICAgIHNldElzU2Nyb2xsT25Cb3R0b20oKTtcbiAgICB9KTtcblxuICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2h0bXg6bG9hZCcsIChlKSA9PiB7XG4gICAgICAgIGNvbnN0IHRhcmdldEVsZW1lbnQgPSBlLnRhcmdldCBhcyBIVE1MRWxlbWVudDtcblxuICAgICAgICBpZiAodGFyZ2V0RWxlbWVudC5jbGFzc0xpc3QuY29udGFpbnMoJ25ldy1ub3RpZmljYXRpb24nKSkge1xuICAgICAgICAgICAgLy8gU2hvdyB0aGUgbmV3IG5vdGlmaWNhdGlvbiBsYWJlbCBpZiBoaWRkZW5cbiAgICAgICAgICAgIGlmIChub3RpZmljYXRpb25OZXdMYWJlbC5jbGFzc0xpc3QuY29udGFpbnMoJ2hpZGRlbicpKSB7XG4gICAgICAgICAgICAgICAgbm90aWZpY2F0aW9uTmV3TGFiZWwuY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7XG4gICAgICAgICAgICAgICAgbm90aWZpY2F0aW9uTmV3TGFiZWwuY2xhc3NMaXN0LmFkZCgnZmxleCcpO1xuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICBpZiAoc2Nyb2xsT25Cb3R0b20pe1xuICAgICAgICAgICAgICAgIG5vdGlmaWNhdGlvbkNvbnRhaW5lci5zY3JvbGxUbygwLCBub3RpZmljYXRpb25Db250YWluZXIuc2Nyb2xsSGVpZ2h0KTtcbiAgICAgICAgICAgIH0gXG5cbiAgICAgICAgICAgIG5ld01lc3NhZ2VzQ291bnQrKztcbiAgICAgICAgICAgIHNjcm9sbFRvQm90dG9tQnV0dG9uTWVzc2FnZUNvdW50LmlubmVyVGV4dCA9IG5ld01lc3NhZ2VzQ291bnQudG9TdHJpbmcoKTtcblxuICAgICAgICAgICAgc2Nyb2xsVG9Cb3R0b21CdXR0b25TdmcuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG4gICAgICAgICAgICBzY3JvbGxUb0JvdHRvbUJ1dHRvbk1lc3NhZ2VDb3VudC5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIG5vdGlmaWNhdGlvbkNvbnRhaW5lci5zY3JvbGxUbygwLCB0YXJnZXRFbGVtZW50LnNjcm9sbEhlaWdodCAqIDUpO1xuICAgICAgICB9XG5cbiAgICB9KTtcblxuICAgIC8vIHNzZSBzZXR1cFxuICAgIGNvbnN0IHVzZXJVdWlkSW5wdXQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndXNlci11dWlkJykgYXMgSFRNTElucHV0RWxlbWVudDtcbiAgICBjb25zdCB1c2VyVXVpZCA9IHVzZXJVdWlkSW5wdXQudmFsdWU7XG5cbiAgICBjb25zdCBldmVudFNvdXJjZSA9IG5ldyBFdmVudFNvdXJjZSgnL3NzZScuY29uY2F0KGA/Y2hhbm5lbD1yb29tOiR7dXNlclV1aWR9YCkpO1xuICAgIGV2ZW50U291cmNlLm9ubWVzc2FnZSA9IChldnQpID0+IHtcbiAgICAgICAgY29uc29sZS5sb2coZXZ0KTtcbiAgICB9XG59KTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=