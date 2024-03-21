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
exports.disableDateFlowbite = exports.socialMediaShare = exports.scrollDownSmooth = exports.scrollDown = exports.resizeChat = exports.handleHideElements = void 0;
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
        console.log('body hidden', document.body);
        document.body.style.overflow = 'hidden';
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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QUFVO29CQUFFLE9BQU87Z0JBRXhCLElBQU0sVUFBVSxHQUFHLFVBQVUsQ0FBQyxhQUFhLENBQUMsY0FBYyxDQUFDLENBQUM7Z0JBQzVELElBQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxXQUFXLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO2dCQUNuRCxJQUFNLElBQUksR0FBRyxVQUFVLENBQUMsV0FBVyxDQUFDLEtBQUssQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQztnQkFDbEQsSUFBTSxXQUFXLEdBQUcsSUFBSSxJQUFJLENBQUMsVUFBRyxLQUFLLGlCQUFPLElBQUksQ0FBRSxDQUFDLENBQUMsUUFBUSxFQUFFLENBQUM7Z0JBQy9ELElBQU0sUUFBUSxHQUFHLFVBQVUsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO2dCQUVqRSxRQUFRLENBQUMsT0FBTyxDQUFDLFVBQUMsSUFBb0I7b0JBQ3BDLElBQU0sU0FBUyxHQUFHLElBQUksQ0FBQyxZQUFZLENBQUMsV0FBVyxDQUFDLENBQUM7b0JBQ2pELElBQU0sU0FBUyxHQUFHLElBQUksSUFBSSxDQUFDLFFBQVEsQ0FBQyxTQUFTLENBQUMsQ0FBQyxDQUFDLFFBQVEsRUFBRSxDQUFDO29CQUUzRCxTQUFTLEtBQUssV0FBVzt3QkFDdkIsQ0FBQyxDQUFDLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxLQUFLLEdBQUcsU0FBUyxDQUFDO3dCQUNoQyxDQUFDLENBQUMsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLEtBQUssR0FBRyxNQUFNLENBQUMsQ0FBQztnQkFDbEMsQ0FBQyxDQUFDLENBQUM7WUFDTCxDQUFDLENBQUMsQ0FBQztRQUNMLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQyxFQUFFLElBQUksQ0FBQyxDQUFDO0FBQ1gsQ0FBQztBQXZDRCxrREF1Q0MiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvdXRpbHMudHMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gYWRkSGlkZGVuQ2xhc3MoZWxlbWVudDogSFRNTEVsZW1lbnQpIHtcbiAgZWxlbWVudC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbn1cblxuZnVuY3Rpb24gaGlkZUVsZW1lbnRzKFxuICBldmVudDogTW91c2VFdmVudCxcbiAgZWxlbWVudDogSFRNTEVsZW1lbnQsXG4gIG90aGVyRWxlbWVudD86IEhUTUxFbGVtZW50W10sXG4pIHtcbiAgaWYgKFxuICAgICFlbGVtZW50LmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSAmJlxuICAgICFvdGhlckVsZW1lbnQuc29tZShlbCA9PiBlbC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkpXG4gICkge1xuICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICB9XG59XG5cbi8vIGV4cG9ydCBmdW5jdGlvbiB1bmxvY2tTY3JvbGwoKSB7XG4vLyAgIGNvbnN0IHNjcm9sbFkgPSBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcDtcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5wb3NpdGlvbiA9ICcnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcCA9ICcnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLmxlZnQgPSAnJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5yaWdodCA9ICcnO1xuLy8gICB3aW5kb3cuc2Nyb2xsVG8oMCwgcGFyc2VJbnQoc2Nyb2xsWSB8fCAnMCcpICogLTEpO1xuXG4vLyAgIGNvbnNvbGUubG9nKCd1bmxvY2sgc2Nyb2xsJyk7XG4vLyB9XG5cbi8vIGV4cG9ydCBmdW5jdGlvbiBsb2NrU2Nyb2xsKCkge1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnBvc2l0aW9uID0gJ2ZpeGVkJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS50b3AgPSBgLSR7d2luZG93LnNjcm9sbFl9cHhgO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLmxlZnQgPSAnMCc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnMCc7XG5cbi8vICAgY29uc29sZS5sb2coJ2xvY2sgc2Nyb2xsJyk7XG4vLyB9XG5cbmV4cG9ydCBmdW5jdGlvbiBoYW5kbGVIaWRlRWxlbWVudHMoXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ6IEhUTUxFbGVtZW50W10gPSBbXSxcbikge1xuICBlbGVtZW50LmNsYXNzTGlzdC50b2dnbGUoJ2hpZGRlbicpO1xuICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsIChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICAgIGhpZGVFbGVtZW50cyhldmVudCwgZWxlbWVudCwgb3RoZXJFbGVtZW50KTtcbiAgfSk7XG5cbiAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIGZ1bmN0aW9uIChldmVudCkge1xuICAgIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgICB9XG4gIH0pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVzaXplQ2hhdCgpIHtcbiAgY29uc29sZS5sb2coJ3Jlc2l6ZUNoYXQnKTtcbiAgY29uc3QgaGVhZGVyOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5oZWFkZXInKTtcbiAgY29uc3QgY2hhdE1haW46IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtYm9keScpO1xuICBjb25zdCBjaGF0Rm9vdGVyOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWZvb3RlcicpO1xuICBjb25zdCBjaGF0V2luZG93OiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LXdpbmRvdycpO1xuICBjb25zdCBzY3JlZW5XaXRoOiBudW1iZXIgPSB3aW5kb3cuaW5uZXJXaWR0aDtcbiAgY29uc3QgaGVhZGVyQm90dG9tOiBudW1iZXIgPSBoZWFkZXIub2Zmc2V0VG9wICsgaGVhZGVyLm9mZnNldEhlaWdodDtcbiAgY29uc3QgY2hhdFdpbmRvd1RvcDogbnVtYmVyID0gY2hhdFdpbmRvdy5vZmZzZXRUb3A7XG4gIGNvbnN0IGZpeGVkTWluRGlzdGFuY2U6IG51bWJlciA9IDI1MDtcbiAgY29uc3QgbWF4Q2hhdFdpbmRvd0hlaWdodDogbnVtYmVyID0gNjUwO1xuICBjb25zdCBhdmFpbGFibGVTcGFjZTogbnVtYmVyID0gY2hhdFdpbmRvd1RvcCAtIGhlYWRlckJvdHRvbTtcblxuICBpZiAoc2NyZWVuV2l0aCA8IDY0MCkge1xuICAgIGNoYXRNYWluLnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMCUgLSAke2NoYXRGb290ZXIub2Zmc2V0SGVpZ2h0fXB4KWA7XG4gICAgY29uc29sZS5sb2coJ2JvZHkgaGlkZGVuJywgZG9jdW1lbnQuYm9keSk7XG5cbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLm92ZXJmbG93ID0gJ2hpZGRlbic7XG4gICAgcmV0dXJuO1xuICB9XG5cbiAgaWYgKCFoZWFkZXIgfHwgIWNoYXRXaW5kb3cpIHJldHVybjtcblxuICBpZiAoYXZhaWxhYmxlU3BhY2UgPCBmaXhlZE1pbkRpc3RhbmNlKSB7XG4gICAgY2hhdFdpbmRvdy5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDB2aCAtICR7Zml4ZWRNaW5EaXN0YW5jZX1weClgO1xuICB9XG5cbiAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgaWYgKGNoYXRXaW5kb3cub2Zmc2V0SGVpZ2h0ID4gbWF4Q2hhdFdpbmRvd0hlaWdodCkge1xuICAgICAgY2hhdFdpbmRvdy5zdHlsZS5oZWlnaHQgPSBgJHttYXhDaGF0V2luZG93SGVpZ2h0fXB4YDtcbiAgICB9XG4gIH0sIDUwMCk7XG5cbiAgaWYgKGNoYXRNYWluICYmIGNoYXRGb290ZXIpIHtcbiAgICBjaGF0TWFpbi5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDAlIC0gJHtjaGF0Rm9vdGVyLm9mZnNldEhlaWdodH1weClgO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gIH0pO1xufVxuXG5jb25zdCBzY3JvbGxBbmltYXRpb25EdXJhdGlvbiA9IDIwMDtcbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duU21vb3RoKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgICAgdG9wOiBlbGVtZW50LnNjcm9sbEhlaWdodCxcbiAgICAgIGJlaGF2aW9yOiAnc21vb3RoJyxcbiAgICB9KTtcbiAgfSwgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gc29jaWFsTWVkaWFTaGFyZSgpIHtcbiAgY29uc29sZS5sb2coJ3NvY2lhbE1lZGlhU2hhcmUnKTtcbiAgY29uc3QgZmJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmZiLXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgZmJTaGFyZUljb25zLmZvckVhY2goZmJJY29uID0+IHtcbiAgICBmYkljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGZiSWNvbi5ocmVmID0gYGh0dHBzOi8vd3d3LmZhY2Vib29rLmNvbS9zaGFyZS5waHA/dT0ke2xpbmt9YDtcbiAgICAgIGNvbnNvbGUubG9nKGZiSWNvbi5ocmVmKTtcbiAgICB9KTtcbiAgfSk7XG5cbiAgY29uc3QgaW5zdGFTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmktc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICBpbnN0YVNoYXJlSWNvbnMuZm9yRWFjaChpbnN0YUljb24gPT4ge1xuICAgIGluc3RhSWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgaW5zdGFJY29uLmhyZWYgPSBgaHR0cHM6Ly93d3cuaW5zdGFncmFtLmNvbWA7XG4gICAgICBjb25zb2xlLmxvZyhpbnN0YUljb24uaHJlZik7XG4gICAgfSk7XG4gIH0pO1xuXG4gIGNvbnN0IHR3aXR0ZXJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLngtc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICB0d2l0dGVyU2hhcmVJY29ucy5mb3JFYWNoKHR3aXR0ZXJJY29uID0+IHtcbiAgICB0d2l0dGVySWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgY29uc3QgdGV4dCA9IGVuY29kZVVSSUNvbXBvbmVudChcbiAgICAgICAgJ0NoZWNrIG91dCBjb29sIHRpY2tldHMgZm9yIHNhbGUgb24gRmFuVGlja2V0JyxcbiAgICAgICk7XG4gICAgICBjb25zdCBoYXNodGFncyA9IGVuY29kZVVSSUNvbXBvbmVudCgndGlja2V0cyxmb3JzYWxlJyk7XG4gICAgICB0d2l0dGVySWNvbi5ocmVmID0gYGh0dHBzOi8vdHdpdHRlci5jb20vc2hhcmU/dXJsPSR7bGlua30mdGV4dD0ke3RleHR9Jmhhc2h0YWdzPSR7aGFzaHRhZ3N9YDtcbiAgICAgIGNvbnNvbGUubG9nKHR3aXR0ZXJJY29uLmhyZWYpO1xuICAgIH0pO1xuICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGRpc2FibGVEYXRlRmxvd2JpdGUoKSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGNvbnN0IGFsbERhdGVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXItY2VsbCcpO1xuXG4gICAgY29uc3QgY3VycmVudE1vbnRoID0gbmV3IERhdGUoKS5nZXRNb250aCgpO1xuICAgIGFsbERhdGVzLmZvckVhY2goKGRhdGU6IEhUTUxEaXZFbGVtZW50KSA9PiB7XG4gICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICBjb25zdCBkYXRlTW9udGggPSBuZXcgRGF0ZShwYXJzZUludCh0aW1lU3RhbXApKS5nZXRNb250aCgpO1xuICAgICAgZGF0ZU1vbnRoICE9PSBjdXJyZW50TW9udGhcbiAgICAgICAgPyAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjOTlhMWEzJylcbiAgICAgICAgOiAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjZmZmJyk7XG4gICAgfSk7XG5cbiAgICBjb25zdCBjYWxlbmRhckJ1dHRvbnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcubmV4dC1idG4sIC5wcmV2LWJ0bicpO1xuXG4gICAgY2FsZW5kYXJCdXR0b25zLmZvckVhY2goKGJ1dHRvbjogSFRNTEJ1dHRvbkVsZW1lbnQpID0+IHtcbiAgICAgIGJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChldmVudDogRXZlbnQpID0+IHtcbiAgICAgICAgY29uc3QgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgICAgICBjb25zdCBkYXRlUGlja2VyID0gdGFyZ2V0LmNsb3Nlc3QoJy5kYXRlcGlja2VyLXBpY2tlcicpO1xuXG4gICAgICAgIGlmICghZGF0ZVBpY2tlcikgcmV0dXJuO1xuXG4gICAgICAgIGNvbnN0IG1vbnRoVGl0bGUgPSBkYXRlUGlja2VyLnF1ZXJ5U2VsZWN0b3IoJy52aWV3LXN3aXRjaCcpO1xuICAgICAgICBjb25zdCBtb250aCA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVswXTtcbiAgICAgICAgY29uc3QgeWVhciA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVsxXTtcbiAgICAgICAgY29uc3QgY3VycmVudERhdGUgPSBuZXcgRGF0ZShgJHttb250aH0gMSwgJHt5ZWFyfWApLmdldE1vbnRoKCk7XG4gICAgICAgIGNvbnN0IGFsbERhdGVzID0gZGF0ZVBpY2tlci5xdWVyeVNlbGVjdG9yQWxsKCcuZGF0ZXBpY2tlci1jZWxsJyk7XG5cbiAgICAgICAgYWxsRGF0ZXMuZm9yRWFjaCgoZGF0ZTogSFRNTERpdkVsZW1lbnQpID0+IHtcbiAgICAgICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICAgICAgY29uc3QgZGF0ZU1vbnRoID0gbmV3IERhdGUocGFyc2VJbnQodGltZVN0YW1wKSkuZ2V0TW9udGgoKTtcblxuICAgICAgICAgIGRhdGVNb250aCAhPT0gY3VycmVudERhdGVcbiAgICAgICAgICAgID8gKGRhdGUuc3R5bGUuY29sb3IgPSAnIzk5YTFhMycpXG4gICAgICAgICAgICA6IChkYXRlLnN0eWxlLmNvbG9yID0gJyNmZmYnKTtcbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfSwgMTAwMCk7XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=