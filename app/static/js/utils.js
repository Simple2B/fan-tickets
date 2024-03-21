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
        document.body.style.position = 'fixed';
        document.body.style.top = "-".concat(window.scrollY, "px");
        document.body.style.left = '0';
        document.body.style.right = '0';
    }
}
exports.lockScrollBody = lockScrollBody;
function unlockScrollBody() {
    console.log('unlockScrollBody');
    var screenWith = window.innerWidth;
    if (screenWith < 640) {
        var scrollY_1 = document.body.style.top;
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';
        window.scrollTo(0, parseInt(scrollY_1 || '0') * -1);
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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SUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLFdBQVcsQ0FBQyxLQUFLLENBQUMsR0FBRyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7Z0JBQ25ELElBQU0sSUFBSSxHQUFHLFVBQVUsQ0FBQyxXQUFXLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO2dCQUNsRCxJQUFNLFdBQVcsR0FBRyxJQUFJLElBQUksQ0FBQyxVQUFHLEtBQUssaUJBQU8sSUFBSSxDQUFFLENBQUMsQ0FBQyxRQUFRLEVBQUUsQ0FBQztnQkFDL0QsSUFBTSxRQUFRLEdBQUcsVUFBVSxDQUFDLGdCQUFnQixDQUFDLGtCQUFrQixDQUFDLENBQUM7Z0JBRWpFLFFBQVEsQ0FBQyxPQUFPLENBQUMsVUFBQyxJQUFvQjtvQkFDcEMsSUFBTSxTQUFTLEdBQUcsSUFBSSxDQUFDLFlBQVksQ0FBQyxXQUFXLENBQUMsQ0FBQztvQkFDakQsSUFBTSxTQUFTLEdBQUcsSUFBSSxJQUFJLENBQUMsUUFBUSxDQUFDLFNBQVMsQ0FBQyxDQUFDLENBQUMsUUFBUSxFQUFFLENBQUM7b0JBRTNELFNBQVMsS0FBSyxXQUFXO3dCQUN2QixDQUFDLENBQUMsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLEtBQUssR0FBRyxTQUFTLENBQUM7d0JBQ2hDLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsS0FBSyxHQUFHLE1BQU0sQ0FBQyxDQUFDO2dCQUNsQyxDQUFDLENBQUMsQ0FBQztZQUNMLENBQUMsQ0FBQyxDQUFDO1FBQ0wsQ0FBQyxDQUFDLENBQUM7SUFDTCxDQUFDLEVBQUUsSUFBSSxDQUFDLENBQUM7QUFDWCxDQUFDO0FBdkNELGtEQXVDQyIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy91dGlscy50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiBhZGRIaWRkZW5DbGFzcyhlbGVtZW50OiBIVE1MRWxlbWVudCkge1xuICBlbGVtZW50LmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xufVxuXG5mdW5jdGlvbiBoaWRlRWxlbWVudHMoXG4gIGV2ZW50OiBNb3VzZUV2ZW50LFxuICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgb3RoZXJFbGVtZW50PzogSFRNTEVsZW1lbnRbXSxcbikge1xuICBpZiAoXG4gICAgIWVsZW1lbnQuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpICYmXG4gICAgIW90aGVyRWxlbWVudC5zb21lKGVsID0+IGVsLmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSlcbiAgKSB7XG4gICAgYWRkSGlkZGVuQ2xhc3MoZWxlbWVudCk7XG4gIH1cbn1cblxuLy8gZXhwb3J0IGZ1bmN0aW9uIHVubG9ja1Njcm9sbCgpIHtcbi8vICAgY29uc3Qgc2Nyb2xsWSA9IGRvY3VtZW50LmJvZHkuc3R5bGUudG9wO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnBvc2l0aW9uID0gJyc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUudG9wID0gJyc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUubGVmdCA9ICcnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnJpZ2h0ID0gJyc7XG4vLyAgIHdpbmRvdy5zY3JvbGxUbygwLCBwYXJzZUludChzY3JvbGxZIHx8ICcwJykgKiAtMSk7XG5cbi8vICAgY29uc29sZS5sb2coJ3VubG9jayBzY3JvbGwnKTtcbi8vIH1cblxuLy8gZXhwb3J0IGZ1bmN0aW9uIGxvY2tTY3JvbGwoKSB7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucG9zaXRpb24gPSAnZml4ZWQnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcCA9IGAtJHt3aW5kb3cuc2Nyb2xsWX1weGA7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUubGVmdCA9ICcwJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5yaWdodCA9ICcwJztcblxuLy8gICBjb25zb2xlLmxvZygnbG9jayBzY3JvbGwnKTtcbi8vIH1cblxuZXhwb3J0IGZ1bmN0aW9uIGhhbmRsZUhpZGVFbGVtZW50cyhcbiAgZWxlbWVudDogSFRNTEVsZW1lbnQsXG4gIG90aGVyRWxlbWVudDogSFRNTEVsZW1lbnRbXSA9IFtdLFxuKSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gIHdpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdtb3VzZXVwJywgKGV2ZW50OiBNb3VzZUV2ZW50KSA9PiB7XG4gICAgaGlkZUVsZW1lbnRzKGV2ZW50LCBlbGVtZW50LCBvdGhlckVsZW1lbnQpO1xuICB9KTtcblxuICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdrZXlkb3duJywgZnVuY3Rpb24gKGV2ZW50KSB7XG4gICAgaWYgKGV2ZW50LmtleSA9PT0gJ0VzY2FwZScpIHtcbiAgICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICAgIH1cbiAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZXNpemVDaGF0KCkge1xuICBjb25zb2xlLmxvZygncmVzaXplQ2hhdCcpO1xuICBjb25zdCBoZWFkZXI6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLmhlYWRlcicpO1xuICBjb25zdCBjaGF0TWFpbjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC1ib2R5Jyk7XG4gIGNvbnN0IGNoYXRGb290ZXI6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtZm9vdGVyJyk7XG4gIGNvbnN0IGNoYXRXaW5kb3c6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtd2luZG93Jyk7XG4gIGNvbnN0IHNjcmVlbldpdGg6IG51bWJlciA9IHdpbmRvdy5pbm5lcldpZHRoO1xuICBjb25zdCBoZWFkZXJCb3R0b206IG51bWJlciA9IGhlYWRlci5vZmZzZXRUb3AgKyBoZWFkZXIub2Zmc2V0SGVpZ2h0O1xuICBjb25zdCBjaGF0V2luZG93VG9wOiBudW1iZXIgPSBjaGF0V2luZG93Lm9mZnNldFRvcDtcbiAgY29uc3QgZml4ZWRNaW5EaXN0YW5jZTogbnVtYmVyID0gMjUwO1xuICBjb25zdCBtYXhDaGF0V2luZG93SGVpZ2h0OiBudW1iZXIgPSA2NTA7XG4gIGNvbnN0IGF2YWlsYWJsZVNwYWNlOiBudW1iZXIgPSBjaGF0V2luZG93VG9wIC0gaGVhZGVyQm90dG9tO1xuXG4gIGlmIChzY3JlZW5XaXRoIDwgNjQwKSB7XG4gICAgY2hhdE1haW4uc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwJSAtICR7Y2hhdEZvb3Rlci5vZmZzZXRIZWlnaHR9cHgpYDtcbiAgICByZXR1cm47XG4gIH1cblxuICBpZiAoIWhlYWRlciB8fCAhY2hhdFdpbmRvdykgcmV0dXJuO1xuXG4gIGlmIChhdmFpbGFibGVTcGFjZSA8IGZpeGVkTWluRGlzdGFuY2UpIHtcbiAgICBjaGF0V2luZG93LnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMHZoIC0gJHtmaXhlZE1pbkRpc3RhbmNlfXB4KWA7XG4gIH1cblxuICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICBpZiAoY2hhdFdpbmRvdy5vZmZzZXRIZWlnaHQgPiBtYXhDaGF0V2luZG93SGVpZ2h0KSB7XG4gICAgICBjaGF0V2luZG93LnN0eWxlLmhlaWdodCA9IGAke21heENoYXRXaW5kb3dIZWlnaHR9cHhgO1xuICAgIH1cbiAgfSwgNTAwKTtcblxuICBpZiAoY2hhdE1haW4gJiYgY2hhdEZvb3Rlcikge1xuICAgIGNoYXRNYWluLnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMCUgLSAke2NoYXRGb290ZXIub2Zmc2V0SGVpZ2h0fXB4KWA7XG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGxvY2tTY3JvbGxCb2R5KCkge1xuICBjb25zb2xlLmxvZygnbG9ja1Njcm9sbEJvZHknKTtcblxuICBjb25zdCBzY3JlZW5XaXRoOiBudW1iZXIgPSB3aW5kb3cuaW5uZXJXaWR0aDtcbiAgaWYgKHNjcmVlbldpdGggPCA2NDApIHtcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLnBvc2l0aW9uID0gJ2ZpeGVkJztcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcCA9IGAtJHt3aW5kb3cuc2Nyb2xsWX1weGA7XG4gICAgZG9jdW1lbnQuYm9keS5zdHlsZS5sZWZ0ID0gJzAnO1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnMCc7XG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHVubG9ja1Njcm9sbEJvZHkoKSB7XG4gIGNvbnNvbGUubG9nKCd1bmxvY2tTY3JvbGxCb2R5Jyk7XG5cbiAgY29uc3Qgc2NyZWVuV2l0aDogbnVtYmVyID0gd2luZG93LmlubmVyV2lkdGg7XG4gIGlmIChzY3JlZW5XaXRoIDwgNjQwKSB7XG4gICAgY29uc3Qgc2Nyb2xsWSA9IGRvY3VtZW50LmJvZHkuc3R5bGUudG9wO1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUucG9zaXRpb24gPSAnJztcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcCA9ICcnO1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUubGVmdCA9ICcnO1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnJztcbiAgICB3aW5kb3cuc2Nyb2xsVG8oMCwgcGFyc2VJbnQoc2Nyb2xsWSB8fCAnMCcpICogLTEpO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gIH0pO1xufVxuXG5jb25zdCBzY3JvbGxBbmltYXRpb25EdXJhdGlvbiA9IDIwMDtcbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duU21vb3RoKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgICAgdG9wOiBlbGVtZW50LnNjcm9sbEhlaWdodCxcbiAgICAgIGJlaGF2aW9yOiAnc21vb3RoJyxcbiAgICB9KTtcbiAgfSwgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gc29jaWFsTWVkaWFTaGFyZSgpIHtcbiAgY29uc29sZS5sb2coJ3NvY2lhbE1lZGlhU2hhcmUnKTtcbiAgY29uc3QgZmJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmZiLXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgZmJTaGFyZUljb25zLmZvckVhY2goZmJJY29uID0+IHtcbiAgICBmYkljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGZiSWNvbi5ocmVmID0gYGh0dHBzOi8vd3d3LmZhY2Vib29rLmNvbS9zaGFyZS5waHA/dT0ke2xpbmt9YDtcbiAgICAgIGNvbnNvbGUubG9nKGZiSWNvbi5ocmVmKTtcbiAgICB9KTtcbiAgfSk7XG5cbiAgY29uc3QgaW5zdGFTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmktc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICBpbnN0YVNoYXJlSWNvbnMuZm9yRWFjaChpbnN0YUljb24gPT4ge1xuICAgIGluc3RhSWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgaW5zdGFJY29uLmhyZWYgPSBgaHR0cHM6Ly93d3cuaW5zdGFncmFtLmNvbWA7XG4gICAgICBjb25zb2xlLmxvZyhpbnN0YUljb24uaHJlZik7XG4gICAgfSk7XG4gIH0pO1xuXG4gIGNvbnN0IHR3aXR0ZXJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLngtc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICB0d2l0dGVyU2hhcmVJY29ucy5mb3JFYWNoKHR3aXR0ZXJJY29uID0+IHtcbiAgICB0d2l0dGVySWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgY29uc3QgdGV4dCA9IGVuY29kZVVSSUNvbXBvbmVudChcbiAgICAgICAgJ0NoZWNrIG91dCBjb29sIHRpY2tldHMgZm9yIHNhbGUgb24gRmFuVGlja2V0JyxcbiAgICAgICk7XG4gICAgICBjb25zdCBoYXNodGFncyA9IGVuY29kZVVSSUNvbXBvbmVudCgndGlja2V0cyxmb3JzYWxlJyk7XG4gICAgICB0d2l0dGVySWNvbi5ocmVmID0gYGh0dHBzOi8vdHdpdHRlci5jb20vc2hhcmU/dXJsPSR7bGlua30mdGV4dD0ke3RleHR9Jmhhc2h0YWdzPSR7aGFzaHRhZ3N9YDtcbiAgICAgIGNvbnNvbGUubG9nKHR3aXR0ZXJJY29uLmhyZWYpO1xuICAgIH0pO1xuICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGRpc2FibGVEYXRlRmxvd2JpdGUoKSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGNvbnN0IGFsbERhdGVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXItY2VsbCcpO1xuXG4gICAgY29uc3QgY3VycmVudE1vbnRoID0gbmV3IERhdGUoKS5nZXRNb250aCgpO1xuICAgIGFsbERhdGVzLmZvckVhY2goKGRhdGU6IEhUTUxEaXZFbGVtZW50KSA9PiB7XG4gICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICBjb25zdCBkYXRlTW9udGggPSBuZXcgRGF0ZShwYXJzZUludCh0aW1lU3RhbXApKS5nZXRNb250aCgpO1xuICAgICAgZGF0ZU1vbnRoICE9PSBjdXJyZW50TW9udGhcbiAgICAgICAgPyAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjOTlhMWEzJylcbiAgICAgICAgOiAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjZmZmJyk7XG4gICAgfSk7XG5cbiAgICBjb25zdCBjYWxlbmRhckJ1dHRvbnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcubmV4dC1idG4sIC5wcmV2LWJ0bicpO1xuXG4gICAgY2FsZW5kYXJCdXR0b25zLmZvckVhY2goKGJ1dHRvbjogSFRNTEJ1dHRvbkVsZW1lbnQpID0+IHtcbiAgICAgIGJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChldmVudDogRXZlbnQpID0+IHtcbiAgICAgICAgY29uc3QgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgICAgICBjb25zdCBkYXRlUGlja2VyID0gdGFyZ2V0LmNsb3Nlc3QoJy5kYXRlcGlja2VyLXBpY2tlcicpO1xuXG4gICAgICAgIGlmICghZGF0ZVBpY2tlcikgcmV0dXJuO1xuXG4gICAgICAgIGNvbnN0IG1vbnRoVGl0bGUgPSBkYXRlUGlja2VyLnF1ZXJ5U2VsZWN0b3IoJy52aWV3LXN3aXRjaCcpO1xuICAgICAgICBjb25zdCBtb250aCA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVswXTtcbiAgICAgICAgY29uc3QgeWVhciA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVsxXTtcbiAgICAgICAgY29uc3QgY3VycmVudERhdGUgPSBuZXcgRGF0ZShgJHttb250aH0gMSwgJHt5ZWFyfWApLmdldE1vbnRoKCk7XG4gICAgICAgIGNvbnN0IGFsbERhdGVzID0gZGF0ZVBpY2tlci5xdWVyeVNlbGVjdG9yQWxsKCcuZGF0ZXBpY2tlci1jZWxsJyk7XG5cbiAgICAgICAgYWxsRGF0ZXMuZm9yRWFjaCgoZGF0ZTogSFRNTERpdkVsZW1lbnQpID0+IHtcbiAgICAgICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICAgICAgY29uc3QgZGF0ZU1vbnRoID0gbmV3IERhdGUocGFyc2VJbnQodGltZVN0YW1wKSkuZ2V0TW9udGgoKTtcblxuICAgICAgICAgIGRhdGVNb250aCAhPT0gY3VycmVudERhdGVcbiAgICAgICAgICAgID8gKGRhdGUuc3R5bGUuY29sb3IgPSAnIzk5YTFhMycpXG4gICAgICAgICAgICA6IChkYXRlLnN0eWxlLmNvbG9yID0gJyNmZmYnKTtcbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfSwgMTAwMCk7XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=