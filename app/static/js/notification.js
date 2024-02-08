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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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dUJBQXVCLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQztZQUNoRCxnQ0FBZ0MsQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQyxDQUFDO1NBQy9EO2FBQU07WUFDSCxxQkFBcUIsQ0FBQyxRQUFRLENBQUMsQ0FBQyxFQUFFLGFBQWEsQ0FBQyxZQUFZLEdBQUcsQ0FBQyxDQUFDLENBQUM7U0FDckU7SUFFTCxDQUFDLENBQUMsQ0FBQztJQUVILFlBQVk7SUFDWixJQUFNLGFBQWEsR0FBRyxRQUFRLENBQUMsY0FBYyxDQUFDLFdBQVcsQ0FBcUIsQ0FBQztJQUMvRSxJQUFNLFFBQVEsR0FBRyxhQUFhLENBQUMsS0FBSyxDQUFDO0lBRXJDLElBQU0sV0FBVyxHQUFHLElBQUksV0FBVyxDQUFDLE1BQU0sQ0FBQyxNQUFNLENBQUMsd0JBQWlCLFFBQVEsQ0FBRSxDQUFDLENBQUMsQ0FBQztJQUNoRixXQUFXLENBQUMsU0FBUyxHQUFHLFVBQUMsR0FBRztRQUN4QixPQUFPLENBQUMsR0FBRyxDQUFDLEdBQUcsQ0FBQyxDQUFDO0lBQ3JCLENBQUM7QUFDTCxDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy9ub3RpZmljYXRpb24vbm90aWZpY2F0aW9uLnRzIl0sInNvdXJjZXNDb250ZW50IjpbImRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCAoKSA9PiB7XG4gICAgY29uc3Qgbm90aWZpY2F0aW9uQ29udGFpbmVyID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLm5vdGlmaWNhdGlvbi1jb250YWluZXInKSBhcyBIVE1MRGl2RWxlbWVudDtcbiAgICBjb25zdCBub3RpZmljYXRpb25OZXdMYWJlbCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdub3RpZmljYXRpb24tbmV3LWxhYmVsJyk7XG4gICAgY29uc3Qgc2Nyb2xsVG9Cb3R0b21CdXR0b24gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnbm90aWZpY2F0aW9uLXNjcm9sbC10by1ib3R0b20nKTtcbiAgICBjb25zdCBzY3JvbGxUb0JvdHRvbUJ1dHRvblN2ZyA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdzY3JvbGwtb24tYm90dG9tLXN2ZycpO1xuICAgIGNvbnN0IHNjcm9sbFRvQm90dG9tQnV0dG9uTWVzc2FnZUNvdW50ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3Njcm9sbC1vbi1ib3R0b20tbWVzc2FnZXMtY291bnQnKTtcblxuICAgIGxldCBzY3JvbGxPbkJvdHRvbSA9IGZhbHNlO1xuICAgIGxldCBuZXdNZXNzYWdlc0NvdW50ID0gMDtcblxuICAgIGNvbnN0IHNldElzU2Nyb2xsT25Cb3R0b20gPSAoKSA9PiB7XG4gICAgICAgIHNjcm9sbE9uQm90dG9tID0gbm90aWZpY2F0aW9uQ29udGFpbmVyLnNjcm9sbFRvcCA+PSBub3RpZmljYXRpb25Db250YWluZXIuc2Nyb2xsSGVpZ2h0IC0gbm90aWZpY2F0aW9uQ29udGFpbmVyLmNsaWVudEhlaWdodDtcbiAgICB9XG5cbiAgICBub3RpZmljYXRpb25Db250YWluZXIuYWRkRXZlbnRMaXN0ZW5lcignc2Nyb2xsJywgKCkgPT4ge1xuICAgICAgICBzZXRJc1Njcm9sbE9uQm90dG9tKCk7XG5cbiAgICAgICAgaWYgKG5ld01lc3NhZ2VzQ291bnQgPiAwKSB7XG4gICAgICAgICAgICBzY3JvbGxUb0JvdHRvbUJ1dHRvblN2Zy5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgICAgICAgICAgIHNjcm9sbFRvQm90dG9tQnV0dG9uTWVzc2FnZUNvdW50LmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgc2Nyb2xsVG9Cb3R0b21CdXR0b25TdmcuY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7XG4gICAgICAgICAgICBzY3JvbGxUb0JvdHRvbUJ1dHRvbk1lc3NhZ2VDb3VudC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgICAgICAgfVxuXG4gICAgICAgIGlmIChzY3JvbGxPbkJvdHRvbSkge1xuICAgICAgICAgICAgc2Nyb2xsVG9Cb3R0b21CdXR0b24uY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG4gICAgICAgICAgICBuZXdNZXNzYWdlc0NvdW50ID0gMDtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHNjcm9sbFRvQm90dG9tQnV0dG9uLmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpO1xuICAgICAgICB9XG4gICAgfSk7XG5cbiAgICBzY3JvbGxUb0JvdHRvbUJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgICAgbm90aWZpY2F0aW9uQ29udGFpbmVyLnNjcm9sbFRvKDAsIG5vdGlmaWNhdGlvbkNvbnRhaW5lci5zY3JvbGxIZWlnaHQpO1xuICAgIH0pO1xuXG4gICAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignaHRteDpiZWZvcmVTd2FwJywgKCkgPT4ge1xuICAgICAgICBzZXRJc1Njcm9sbE9uQm90dG9tKCk7XG4gICAgfSlcblxuICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2h0bXg6bG9hZCcsIChlKSA9PiB7XG4gICAgICAgIGNvbnN0IHRhcmdldEVsZW1lbnQgPSBlLnRhcmdldCBhcyBIVE1MRWxlbWVudDtcblxuICAgICAgICBpZiAodGFyZ2V0RWxlbWVudC5jbGFzc0xpc3QuY29udGFpbnMoJ25ldy1ub3RpZmljYXRpb24nKSkge1xuICAgICAgICAgICAgLy8gU2hvdyB0aGUgbmV3IG5vdGlmaWNhdGlvbiBsYWJlbCBpZiBoaWRkZW5cbiAgICAgICAgICAgIGlmIChub3RpZmljYXRpb25OZXdMYWJlbC5jbGFzc0xpc3QuY29udGFpbnMoJ2hpZGRlbicpKSB7XG4gICAgICAgICAgICAgICAgbm90aWZpY2F0aW9uTmV3TGFiZWwuY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7XG4gICAgICAgICAgICAgICAgbm90aWZpY2F0aW9uTmV3TGFiZWwuY2xhc3NMaXN0LmFkZCgnZmxleCcpO1xuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICBpZiAoc2Nyb2xsT25Cb3R0b20pe1xuICAgICAgICAgICAgICAgIG5vdGlmaWNhdGlvbkNvbnRhaW5lci5zY3JvbGxUbygwLCBub3RpZmljYXRpb25Db250YWluZXIuc2Nyb2xsSGVpZ2h0KTtcbiAgICAgICAgICAgIH0gXG5cbiAgICAgICAgICAgIG5ld01lc3NhZ2VzQ291bnQrKztcbiAgICAgICAgICAgIHNjcm9sbFRvQm90dG9tQnV0dG9uTWVzc2FnZUNvdW50LmlubmVyVGV4dCA9IG5ld01lc3NhZ2VzQ291bnQudG9TdHJpbmcoKTtcblxuICAgICAgICAgICAgc2Nyb2xsVG9Cb3R0b21CdXR0b25TdmcuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG4gICAgICAgICAgICBzY3JvbGxUb0JvdHRvbUJ1dHRvbk1lc3NhZ2VDb3VudC5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIG5vdGlmaWNhdGlvbkNvbnRhaW5lci5zY3JvbGxUbygwLCB0YXJnZXRFbGVtZW50LnNjcm9sbEhlaWdodCAqIDUpO1xuICAgICAgICB9XG5cbiAgICB9KTtcblxuICAgIC8vIHNzZSBzZXR1cFxuICAgIGNvbnN0IHVzZXJVdWlkSW5wdXQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndXNlci11dWlkJykgYXMgSFRNTElucHV0RWxlbWVudDtcbiAgICBjb25zdCB1c2VyVXVpZCA9IHVzZXJVdWlkSW5wdXQudmFsdWU7XG5cbiAgICBjb25zdCBldmVudFNvdXJjZSA9IG5ldyBFdmVudFNvdXJjZSgnL3NzZScuY29uY2F0KGA/Y2hhbm5lbD1yb29tOiR7dXNlclV1aWR9YCkpO1xuICAgIGV2ZW50U291cmNlLm9ubWVzc2FnZSA9IChldnQpID0+IHtcbiAgICAgICAgY29uc29sZS5sb2coZXZ0KTtcbiAgICB9XG59KTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=