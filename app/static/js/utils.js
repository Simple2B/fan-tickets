/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it uses a non-standard name for the exports (exports).
(() => {
var exports = __webpack_exports__;
/*!**********************!*\
  !*** ./src/utils.ts ***!
  \**********************/

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.disableDateFlowbite = exports.socialMediaShare = exports.scrollDownSmooth = exports.scrollDown = exports.unlockScrollBody = exports.lockScrollBody = exports.resizeChat = exports.handleHideElements = void 0;
function addHiddenClass(element) {
    element.classList.add('hidden');
}
function hideElements(event, element, otherElement) {
    if (!element.contains(event.target) &&
        !otherElement.some(function (el) { return el.contains(event.target); })) {
        addHiddenClass(element);
    }
}
// export function unlockScroll() {
//   const scrollY = document.body.style.top;
//   document.body.style.position = '';
//   document.body.style.top = '';
//   document.body.style.left = '';
//   document.body.style.right = '';
//   window.scrollTo(0, parseInt(scrollY || '0') * -1);
//   console.log('unlock scroll');
// }
// export function lockScroll() {
//   document.body.style.position = 'fixed';
//   document.body.style.top = `-${window.scrollY}px`;
//   document.body.style.left = '0';
//   document.body.style.right = '0';
//   console.log('lock scroll');
// }
function handleHideElements(element, otherElement) {
    if (otherElement === void 0) { otherElement = []; }
    element.classList.toggle('hidden');
    window.addEventListener('mouseup', function (event) {
        hideElements(event, element, otherElement);
    });
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            addHiddenClass(element);
        }
    });
}
exports.handleHideElements = handleHideElements;
function resizeChat() {
    console.log('resizeChat');
    var header = document.querySelector('.header');
    var chatMain = document.querySelector('#chat-body');
    var chatFooter = document.querySelector('#chat-footer');
    var chatWindow = document.querySelector('#chat-window');
    var screenWith = window.innerWidth;
    var headerBottom = header.offsetTop + header.offsetHeight;
    var chatWindowTop = chatWindow.offsetTop;
    var fixedMinDistance = 250;
    var maxChatWindowHeight = 650;
    var availableSpace = chatWindowTop - headerBottom;
    if (screenWith < 640) {
        chatMain.style.height = "calc(100% - ".concat(chatFooter.offsetHeight, "px)");
        return;
    }
    if (!header || !chatWindow)
        return;
    if (availableSpace < fixedMinDistance) {
        chatWindow.style.height = "calc(100vh - ".concat(fixedMinDistance, "px)");
    }
    setTimeout(function () {
        if (chatWindow.offsetHeight > maxChatWindowHeight) {
            chatWindow.style.height = "".concat(maxChatWindowHeight, "px");
        }
    }, 500);
    if (chatMain && chatFooter) {
        chatMain.style.height = "calc(100% - ".concat(chatFooter.offsetHeight, "px)");
    }
}
exports.resizeChat = resizeChat;
function lockScrollBody() {
    console.log('lockScrollBody');
    var screenWith = window.innerWidth;
    if (screenWith < 640) {
        document.body.style.overflow = 'hidden';
    }
}
exports.lockScrollBody = lockScrollBody;
function unlockScrollBody() {
    console.log('unlockScrollBody');
    var screenWith = window.innerWidth;
    if (screenWith < 640) {
        document.body.style.overflow = 'auto';
    }
}
exports.unlockScrollBody = unlockScrollBody;
function scrollDown(element) {
    element.scrollTo({
        top: element.scrollHeight,
    });
}
exports.scrollDown = scrollDown;
var scrollAnimationDuration = 200;
function scrollDownSmooth(element) {
    setTimeout(function () {
        element.scrollTo({
            top: element.scrollHeight,
            behavior: 'smooth',
        });
    }, scrollAnimationDuration);
}
exports.scrollDownSmooth = scrollDownSmooth;
function socialMediaShare() {
    console.log('socialMediaShare');
    var fbShareIcons = document.querySelectorAll('.fb-share');
    fbShareIcons.forEach(function (fbIcon) {
        fbIcon.addEventListener('click', function () {
            var link = encodeURIComponent(window.location.href);
            fbIcon.href = "https://www.facebook.com/share.php?u=".concat(link);
            console.log(fbIcon.href);
        });
    });
    var instaShareIcons = document.querySelectorAll('.i-share');
    instaShareIcons.forEach(function (instaIcon) {
        instaIcon.addEventListener('click', function () {
            var link = encodeURIComponent(window.location.href);
            instaIcon.href = "https://www.instagram.com";
            console.log(instaIcon.href);
        });
    });
    var twitterShareIcons = document.querySelectorAll('.x-share');
    twitterShareIcons.forEach(function (twitterIcon) {
        twitterIcon.addEventListener('click', function () {
            var link = encodeURIComponent(window.location.href);
            var text = encodeURIComponent('Check out cool tickets for sale on FanTicket');
            var hashtags = encodeURIComponent('tickets,forsale');
            twitterIcon.href = "https://twitter.com/share?url=".concat(link, "&text=").concat(text, "&hashtags=").concat(hashtags);
            console.log(twitterIcon.href);
        });
    });
}
exports.socialMediaShare = socialMediaShare;
function disableDateFlowbite() {
    setTimeout(function () {
        var allDates = document.querySelectorAll('.datepicker-cell');
        var currentMonth = new Date().getMonth();
        allDates.forEach(function (date) {
            var timeStamp = date.getAttribute('data-date');
            var dateMonth = new Date(parseInt(timeStamp)).getMonth();
            dateMonth !== currentMonth
                ? (date.style.color = '#99a1a3')
                : (date.style.color = '#fff');
        });
        var calendarButtons = document.querySelectorAll('.next-btn, .prev-btn');
        calendarButtons.forEach(function (button) {
            button.addEventListener('click', function (event) {
                var target = event.target;
                var datePicker = target.closest('.datepicker-picker');
                if (!datePicker)
                    return;
                var monthTitle = datePicker.querySelector('.view-switch');
                var month = monthTitle.textContent.split(' ')[0];
                var year = monthTitle.textContent.split(' ')[1];
                var currentDate = new Date("".concat(month, " 1, ").concat(year)).getMonth();
                var allDates = datePicker.querySelectorAll('.datepicker-cell');
                allDates.forEach(function (date) {
                    var timeStamp = date.getAttribute('data-date');
                    var dateMonth = new Date(parseInt(timeStamp)).getMonth();
                    dateMonth !== currentDate
                        ? (date.style.color = '#99a1a3')
                        : (date.style.color = '#fff');
                });
            });
        });
    }, 1000);
}
exports.disableDateFlowbite = disableDateFlowbite;

})();

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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Q3ZCLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsS0FBSyxHQUFHLFNBQVMsQ0FBQzt3QkFDaEMsQ0FBQyxDQUFDLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxLQUFLLEdBQUcsTUFBTSxDQUFDLENBQUM7Z0JBQ2xDLENBQUMsQ0FBQyxDQUFDO1lBQ0wsQ0FBQyxDQUFDLENBQUM7UUFDTCxDQUFDLENBQUMsQ0FBQztJQUNMLENBQUMsRUFBRSxJQUFJLENBQUMsQ0FBQztBQUNYLENBQUM7QUF2Q0Qsa0RBdUNDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL3V0aWxzLnRzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQ6IEhUTUxFbGVtZW50KSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG59XG5cbmZ1bmN0aW9uIGhpZGVFbGVtZW50cyhcbiAgZXZlbnQ6IE1vdXNlRXZlbnQsXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ/OiBIVE1MRWxlbWVudFtdLFxuKSB7XG4gIGlmIChcbiAgICAhZWxlbWVudC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkgJiZcbiAgICAhb3RoZXJFbGVtZW50LnNvbWUoZWwgPT4gZWwuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpKVxuICApIHtcbiAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgfVxufVxuXG4vLyBleHBvcnQgZnVuY3Rpb24gdW5sb2NrU2Nyb2xsKCkge1xuLy8gICBjb25zdCBzY3JvbGxZID0gZG9jdW1lbnQuYm9keS5zdHlsZS50b3A7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucG9zaXRpb24gPSAnJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS50b3AgPSAnJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5sZWZ0ID0gJyc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnJztcbi8vICAgd2luZG93LnNjcm9sbFRvKDAsIHBhcnNlSW50KHNjcm9sbFkgfHwgJzAnKSAqIC0xKTtcblxuLy8gICBjb25zb2xlLmxvZygndW5sb2NrIHNjcm9sbCcpO1xuLy8gfVxuXG4vLyBleHBvcnQgZnVuY3Rpb24gbG9ja1Njcm9sbCgpIHtcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5wb3NpdGlvbiA9ICdmaXhlZCc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUudG9wID0gYC0ke3dpbmRvdy5zY3JvbGxZfXB4YDtcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5sZWZ0ID0gJzAnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnJpZ2h0ID0gJzAnO1xuXG4vLyAgIGNvbnNvbGUubG9nKCdsb2NrIHNjcm9sbCcpO1xuLy8gfVxuXG5leHBvcnQgZnVuY3Rpb24gaGFuZGxlSGlkZUVsZW1lbnRzKFxuICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgb3RoZXJFbGVtZW50OiBIVE1MRWxlbWVudFtdID0gW10sXG4pIHtcbiAgZWxlbWVudC5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ21vdXNldXAnLCAoZXZlbnQ6IE1vdXNlRXZlbnQpID0+IHtcbiAgICBoaWRlRWxlbWVudHMoZXZlbnQsIGVsZW1lbnQsIG90aGVyRWxlbWVudCk7XG4gIH0pO1xuXG4gIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICBpZiAoZXZlbnQua2V5ID09PSAnRXNjYXBlJykge1xuICAgICAgYWRkSGlkZGVuQ2xhc3MoZWxlbWVudCk7XG4gICAgfVxuICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHJlc2l6ZUNoYXQoKSB7XG4gIGNvbnNvbGUubG9nKCdyZXNpemVDaGF0Jyk7XG4gIGNvbnN0IGhlYWRlcjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcuaGVhZGVyJyk7XG4gIGNvbnN0IGNoYXRNYWluOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWJvZHknKTtcbiAgY29uc3QgY2hhdEZvb3RlcjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC1mb290ZXInKTtcbiAgY29uc3QgY2hhdFdpbmRvdzogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC13aW5kb3cnKTtcbiAgY29uc3Qgc2NyZWVuV2l0aDogbnVtYmVyID0gd2luZG93LmlubmVyV2lkdGg7XG4gIGNvbnN0IGhlYWRlckJvdHRvbTogbnVtYmVyID0gaGVhZGVyLm9mZnNldFRvcCArIGhlYWRlci5vZmZzZXRIZWlnaHQ7XG4gIGNvbnN0IGNoYXRXaW5kb3dUb3A6IG51bWJlciA9IGNoYXRXaW5kb3cub2Zmc2V0VG9wO1xuICBjb25zdCBmaXhlZE1pbkRpc3RhbmNlOiBudW1iZXIgPSAyNTA7XG4gIGNvbnN0IG1heENoYXRXaW5kb3dIZWlnaHQ6IG51bWJlciA9IDY1MDtcbiAgY29uc3QgYXZhaWxhYmxlU3BhY2U6IG51bWJlciA9IGNoYXRXaW5kb3dUb3AgLSBoZWFkZXJCb3R0b207XG5cbiAgaWYgKHNjcmVlbldpdGggPCA2NDApIHtcbiAgICBjaGF0TWFpbi5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDAlIC0gJHtjaGF0Rm9vdGVyLm9mZnNldEhlaWdodH1weClgO1xuICAgIHJldHVybjtcbiAgfVxuXG4gIGlmICghaGVhZGVyIHx8ICFjaGF0V2luZG93KSByZXR1cm47XG5cbiAgaWYgKGF2YWlsYWJsZVNwYWNlIDwgZml4ZWRNaW5EaXN0YW5jZSkge1xuICAgIGNoYXRXaW5kb3cuc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwdmggLSAke2ZpeGVkTWluRGlzdGFuY2V9cHgpYDtcbiAgfVxuXG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGlmIChjaGF0V2luZG93Lm9mZnNldEhlaWdodCA+IG1heENoYXRXaW5kb3dIZWlnaHQpIHtcbiAgICAgIGNoYXRXaW5kb3cuc3R5bGUuaGVpZ2h0ID0gYCR7bWF4Q2hhdFdpbmRvd0hlaWdodH1weGA7XG4gICAgfVxuICB9LCA1MDApO1xuXG4gIGlmIChjaGF0TWFpbiAmJiBjaGF0Rm9vdGVyKSB7XG4gICAgY2hhdE1haW4uc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwJSAtICR7Y2hhdEZvb3Rlci5vZmZzZXRIZWlnaHR9cHgpYDtcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gbG9ja1Njcm9sbEJvZHkoKSB7XG4gIGNvbnNvbGUubG9nKCdsb2NrU2Nyb2xsQm9keScpO1xuXG4gIGNvbnN0IHNjcmVlbldpdGg6IG51bWJlciA9IHdpbmRvdy5pbm5lcldpZHRoO1xuICBpZiAoc2NyZWVuV2l0aCA8IDY0MCkge1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUub3ZlcmZsb3cgPSAnaGlkZGVuJztcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gdW5sb2NrU2Nyb2xsQm9keSgpIHtcbiAgY29uc29sZS5sb2coJ3VubG9ja1Njcm9sbEJvZHknKTtcblxuICBjb25zdCBzY3JlZW5XaXRoOiBudW1iZXIgPSB3aW5kb3cuaW5uZXJXaWR0aDtcbiAgaWYgKHNjcmVlbldpdGggPCA2NDApIHtcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLm92ZXJmbG93ID0gJ2F1dG8nO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gIH0pO1xufVxuXG5jb25zdCBzY3JvbGxBbmltYXRpb25EdXJhdGlvbiA9IDIwMDtcbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duU21vb3RoKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgICAgdG9wOiBlbGVtZW50LnNjcm9sbEhlaWdodCxcbiAgICAgIGJlaGF2aW9yOiAnc21vb3RoJyxcbiAgICB9KTtcbiAgfSwgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gc29jaWFsTWVkaWFTaGFyZSgpIHtcbiAgY29uc29sZS5sb2coJ3NvY2lhbE1lZGlhU2hhcmUnKTtcbiAgY29uc3QgZmJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmZiLXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgZmJTaGFyZUljb25zLmZvckVhY2goZmJJY29uID0+IHtcbiAgICBmYkljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGZiSWNvbi5ocmVmID0gYGh0dHBzOi8vd3d3LmZhY2Vib29rLmNvbS9zaGFyZS5waHA/dT0ke2xpbmt9YDtcbiAgICAgIGNvbnNvbGUubG9nKGZiSWNvbi5ocmVmKTtcbiAgICB9KTtcbiAgfSk7XG5cbiAgY29uc3QgaW5zdGFTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmktc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICBpbnN0YVNoYXJlSWNvbnMuZm9yRWFjaChpbnN0YUljb24gPT4ge1xuICAgIGluc3RhSWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgaW5zdGFJY29uLmhyZWYgPSBgaHR0cHM6Ly93d3cuaW5zdGFncmFtLmNvbWA7XG4gICAgICBjb25zb2xlLmxvZyhpbnN0YUljb24uaHJlZik7XG4gICAgfSk7XG4gIH0pO1xuXG4gIGNvbnN0IHR3aXR0ZXJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLngtc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICB0d2l0dGVyU2hhcmVJY29ucy5mb3JFYWNoKHR3aXR0ZXJJY29uID0+IHtcbiAgICB0d2l0dGVySWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgY29uc3QgdGV4dCA9IGVuY29kZVVSSUNvbXBvbmVudChcbiAgICAgICAgJ0NoZWNrIG91dCBjb29sIHRpY2tldHMgZm9yIHNhbGUgb24gRmFuVGlja2V0JyxcbiAgICAgICk7XG4gICAgICBjb25zdCBoYXNodGFncyA9IGVuY29kZVVSSUNvbXBvbmVudCgndGlja2V0cyxmb3JzYWxlJyk7XG4gICAgICB0d2l0dGVySWNvbi5ocmVmID0gYGh0dHBzOi8vdHdpdHRlci5jb20vc2hhcmU/dXJsPSR7bGlua30mdGV4dD0ke3RleHR9Jmhhc2h0YWdzPSR7aGFzaHRhZ3N9YDtcbiAgICAgIGNvbnNvbGUubG9nKHR3aXR0ZXJJY29uLmhyZWYpO1xuICAgIH0pO1xuICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGRpc2FibGVEYXRlRmxvd2JpdGUoKSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGNvbnN0IGFsbERhdGVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXItY2VsbCcpO1xuXG4gICAgY29uc3QgY3VycmVudE1vbnRoID0gbmV3IERhdGUoKS5nZXRNb250aCgpO1xuICAgIGFsbERhdGVzLmZvckVhY2goKGRhdGU6IEhUTUxEaXZFbGVtZW50KSA9PiB7XG4gICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICBjb25zdCBkYXRlTW9udGggPSBuZXcgRGF0ZShwYXJzZUludCh0aW1lU3RhbXApKS5nZXRNb250aCgpO1xuICAgICAgZGF0ZU1vbnRoICE9PSBjdXJyZW50TW9udGhcbiAgICAgICAgPyAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjOTlhMWEzJylcbiAgICAgICAgOiAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjZmZmJyk7XG4gICAgfSk7XG5cbiAgICBjb25zdCBjYWxlbmRhckJ1dHRvbnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcubmV4dC1idG4sIC5wcmV2LWJ0bicpO1xuXG4gICAgY2FsZW5kYXJCdXR0b25zLmZvckVhY2goKGJ1dHRvbjogSFRNTEJ1dHRvbkVsZW1lbnQpID0+IHtcbiAgICAgIGJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChldmVudDogRXZlbnQpID0+IHtcbiAgICAgICAgY29uc3QgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgICAgICBjb25zdCBkYXRlUGlja2VyID0gdGFyZ2V0LmNsb3Nlc3QoJy5kYXRlcGlja2VyLXBpY2tlcicpO1xuXG4gICAgICAgIGlmICghZGF0ZVBpY2tlcikgcmV0dXJuO1xuXG4gICAgICAgIGNvbnN0IG1vbnRoVGl0bGUgPSBkYXRlUGlja2VyLnF1ZXJ5U2VsZWN0b3IoJy52aWV3LXN3aXRjaCcpO1xuICAgICAgICBjb25zdCBtb250aCA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVswXTtcbiAgICAgICAgY29uc3QgeWVhciA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVsxXTtcbiAgICAgICAgY29uc3QgY3VycmVudERhdGUgPSBuZXcgRGF0ZShgJHttb250aH0gMSwgJHt5ZWFyfWApLmdldE1vbnRoKCk7XG4gICAgICAgIGNvbnN0IGFsbERhdGVzID0gZGF0ZVBpY2tlci5xdWVyeVNlbGVjdG9yQWxsKCcuZGF0ZXBpY2tlci1jZWxsJyk7XG5cbiAgICAgICAgYWxsRGF0ZXMuZm9yRWFjaCgoZGF0ZTogSFRNTERpdkVsZW1lbnQpID0+IHtcbiAgICAgICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICAgICAgY29uc3QgZGF0ZU1vbnRoID0gbmV3IERhdGUocGFyc2VJbnQodGltZVN0YW1wKSkuZ2V0TW9udGgoKTtcblxuICAgICAgICAgIGRhdGVNb250aCAhPT0gY3VycmVudERhdGVcbiAgICAgICAgICAgID8gKGRhdGUuc3R5bGUuY29sb3IgPSAnIzk5YTFhMycpXG4gICAgICAgICAgICA6IChkYXRlLnN0eWxlLmNvbG9yID0gJyNmZmYnKTtcbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfSwgMTAwMCk7XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=