/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/utils.ts":
/*!**********************!*\
  !*** ./src/utils.ts ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {


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


/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
var exports = __webpack_exports__;
/*!**********************!*\
  !*** ./src/admin.ts ***!
  \**********************/

Object.defineProperty(exports, "__esModule", ({ value: true }));
var utils_1 = __webpack_require__(/*! ./utils */ "./src/utils.ts");
console.log('file admin.ts loaded');
console.log('admin.ts loaded 5 row');
var datesButton = document.querySelector('#event-dates');
var datesDropdown = document.querySelector('#event-dates-dropdown');
datesButton.addEventListener('click', function () {
    var datePickers = document.querySelectorAll('.datepicker');
    var datePickerArray = Array.from(datePickers);
    (0, utils_1.handleHideElements)(datesDropdown, datePickerArray);
});
var searchInput = document.querySelector('#table-search-events');
var searchInputButton = document.querySelector('#table-search-events-button');
if (searchInputButton && searchInput) {
    searchInputButton.addEventListener('click', function () {
        searchInput.value = '';
        searchInput.click();
    });
}

})();

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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R0FBRyxDQUFDLHNCQUFzQixDQUFDLENBQUM7QUFDcEMsT0FBTyxDQUFDLEdBQUcsQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDO0FBRXJDLElBQU0sV0FBVyxHQUFtQixRQUFRLENBQUMsYUFBYSxDQUFDLGNBQWMsQ0FBQyxDQUFDO0FBQzNFLElBQU0sYUFBYSxHQUFzQixRQUFRLENBQUMsYUFBYSxDQUM3RCx1QkFBdUIsQ0FDeEIsQ0FBQztBQUVGLFdBQVcsQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7SUFDcEMsSUFBTSxXQUFXLEdBQUcsUUFBUSxDQUFDLGdCQUFnQixDQUFDLGFBQWEsQ0FBQyxDQUFDO0lBQzdELElBQU0sZUFBZSxHQUFrQixLQUFLLENBQUMsSUFBSSxDQUMvQyxXQUFXLENBQ0ssQ0FBQztJQUVuQiw4QkFBa0IsRUFBQyxhQUFhLEVBQUUsZUFBZSxDQUFDLENBQUM7QUFDckQsQ0FBQyxDQUFDLENBQUM7QUFFSCxJQUFNLFdBQVcsR0FBcUIsUUFBUSxDQUFDLGFBQWEsQ0FDMUQsc0JBQXNCLENBQ3ZCLENBQUM7QUFDRixJQUFNLGlCQUFpQixHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsNkJBQTZCLENBQUMsQ0FBQztBQUNoRixJQUFJLGlCQUFpQixJQUFJLFdBQVcsRUFBRTtJQUNwQyxpQkFBaUIsQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7UUFDMUMsV0FBVyxDQUFDLEtBQUssR0FBRyxFQUFFLENBQUM7UUFDdkIsV0FBVyxDQUFDLEtBQUssRUFBRSxDQUFDO0lBQ3RCLENBQUMsQ0FBQyxDQUFDO0NBQ0oiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvdXRpbHMudHMiLCJ3ZWJwYWNrOi8vc3RhdGljL3dlYnBhY2svYm9vdHN0cmFwIiwid2VicGFjazovL3N0YXRpYy8uL3NyYy9hZG1pbi50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiBhZGRIaWRkZW5DbGFzcyhlbGVtZW50OiBIVE1MRWxlbWVudCkge1xuICBlbGVtZW50LmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xufVxuXG5mdW5jdGlvbiBoaWRlRWxlbWVudHMoXG4gIGV2ZW50OiBNb3VzZUV2ZW50LFxuICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgb3RoZXJFbGVtZW50PzogSFRNTEVsZW1lbnRbXSxcbikge1xuICBpZiAoXG4gICAgIWVsZW1lbnQuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpICYmXG4gICAgIW90aGVyRWxlbWVudC5zb21lKGVsID0+IGVsLmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSlcbiAgKSB7XG4gICAgYWRkSGlkZGVuQ2xhc3MoZWxlbWVudCk7XG4gIH1cbn1cblxuLy8gZXhwb3J0IGZ1bmN0aW9uIHVubG9ja1Njcm9sbCgpIHtcbi8vICAgY29uc3Qgc2Nyb2xsWSA9IGRvY3VtZW50LmJvZHkuc3R5bGUudG9wO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnBvc2l0aW9uID0gJyc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUudG9wID0gJyc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUubGVmdCA9ICcnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnJpZ2h0ID0gJyc7XG4vLyAgIHdpbmRvdy5zY3JvbGxUbygwLCBwYXJzZUludChzY3JvbGxZIHx8ICcwJykgKiAtMSk7XG5cbi8vICAgY29uc29sZS5sb2coJ3VubG9jayBzY3JvbGwnKTtcbi8vIH1cblxuLy8gZXhwb3J0IGZ1bmN0aW9uIGxvY2tTY3JvbGwoKSB7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucG9zaXRpb24gPSAnZml4ZWQnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcCA9IGAtJHt3aW5kb3cuc2Nyb2xsWX1weGA7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUubGVmdCA9ICcwJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5yaWdodCA9ICcwJztcblxuLy8gICBjb25zb2xlLmxvZygnbG9jayBzY3JvbGwnKTtcbi8vIH1cblxuZXhwb3J0IGZ1bmN0aW9uIGhhbmRsZUhpZGVFbGVtZW50cyhcbiAgZWxlbWVudDogSFRNTEVsZW1lbnQsXG4gIG90aGVyRWxlbWVudDogSFRNTEVsZW1lbnRbXSA9IFtdLFxuKSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gIHdpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdtb3VzZXVwJywgKGV2ZW50OiBNb3VzZUV2ZW50KSA9PiB7XG4gICAgaGlkZUVsZW1lbnRzKGV2ZW50LCBlbGVtZW50LCBvdGhlckVsZW1lbnQpO1xuICB9KTtcblxuICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdrZXlkb3duJywgZnVuY3Rpb24gKGV2ZW50KSB7XG4gICAgaWYgKGV2ZW50LmtleSA9PT0gJ0VzY2FwZScpIHtcbiAgICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICAgIH1cbiAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZXNpemVDaGF0KCkge1xuICBjb25zb2xlLmxvZygncmVzaXplQ2hhdCcpO1xuICBjb25zdCBoZWFkZXI6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLmhlYWRlcicpO1xuICBjb25zdCBjaGF0TWFpbjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC1ib2R5Jyk7XG4gIGNvbnN0IGNoYXRGb290ZXI6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtZm9vdGVyJyk7XG4gIGNvbnN0IGNoYXRXaW5kb3c6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtd2luZG93Jyk7XG4gIGNvbnN0IHNjcmVlbldpdGg6IG51bWJlciA9IHdpbmRvdy5pbm5lcldpZHRoO1xuICBjb25zdCBoZWFkZXJCb3R0b206IG51bWJlciA9IGhlYWRlci5vZmZzZXRUb3AgKyBoZWFkZXIub2Zmc2V0SGVpZ2h0O1xuICBjb25zdCBjaGF0V2luZG93VG9wOiBudW1iZXIgPSBjaGF0V2luZG93Lm9mZnNldFRvcDtcbiAgY29uc3QgZml4ZWRNaW5EaXN0YW5jZTogbnVtYmVyID0gMjUwO1xuICBjb25zdCBtYXhDaGF0V2luZG93SGVpZ2h0OiBudW1iZXIgPSA2NTA7XG4gIGNvbnN0IGF2YWlsYWJsZVNwYWNlOiBudW1iZXIgPSBjaGF0V2luZG93VG9wIC0gaGVhZGVyQm90dG9tO1xuXG4gIGlmIChzY3JlZW5XaXRoIDwgNjQwKSB7XG4gICAgY2hhdE1haW4uc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwJSAtICR7Y2hhdEZvb3Rlci5vZmZzZXRIZWlnaHR9cHgpYDtcbiAgICByZXR1cm47XG4gIH1cblxuICBpZiAoIWhlYWRlciB8fCAhY2hhdFdpbmRvdykgcmV0dXJuO1xuXG4gIGlmIChhdmFpbGFibGVTcGFjZSA8IGZpeGVkTWluRGlzdGFuY2UpIHtcbiAgICBjaGF0V2luZG93LnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMHZoIC0gJHtmaXhlZE1pbkRpc3RhbmNlfXB4KWA7XG4gIH1cblxuICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICBpZiAoY2hhdFdpbmRvdy5vZmZzZXRIZWlnaHQgPiBtYXhDaGF0V2luZG93SGVpZ2h0KSB7XG4gICAgICBjaGF0V2luZG93LnN0eWxlLmhlaWdodCA9IGAke21heENoYXRXaW5kb3dIZWlnaHR9cHhgO1xuICAgIH1cbiAgfSwgNTAwKTtcblxuICBpZiAoY2hhdE1haW4gJiYgY2hhdEZvb3Rlcikge1xuICAgIGNoYXRNYWluLnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMCUgLSAke2NoYXRGb290ZXIub2Zmc2V0SGVpZ2h0fXB4KWA7XG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGxvY2tTY3JvbGxCb2R5KCkge1xuICBjb25zb2xlLmxvZygnbG9ja1Njcm9sbEJvZHknKTtcblxuICBjb25zdCBzY3JlZW5XaXRoOiBudW1iZXIgPSB3aW5kb3cuaW5uZXJXaWR0aDtcbiAgaWYgKHNjcmVlbldpdGggPCA2NDApIHtcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLnBvc2l0aW9uID0gJ2ZpeGVkJztcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcCA9IGAtJHt3aW5kb3cuc2Nyb2xsWX1weGA7XG4gICAgZG9jdW1lbnQuYm9keS5zdHlsZS5sZWZ0ID0gJzAnO1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnMCc7XG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHVubG9ja1Njcm9sbEJvZHkoKSB7XG4gIGNvbnNvbGUubG9nKCd1bmxvY2tTY3JvbGxCb2R5Jyk7XG5cbiAgY29uc3Qgc2NyZWVuV2l0aDogbnVtYmVyID0gd2luZG93LmlubmVyV2lkdGg7XG4gIGlmIChzY3JlZW5XaXRoIDwgNjQwKSB7XG4gICAgY29uc3Qgc2Nyb2xsWSA9IGRvY3VtZW50LmJvZHkuc3R5bGUudG9wO1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUucG9zaXRpb24gPSAnJztcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcCA9ICcnO1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUubGVmdCA9ICcnO1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnJztcbiAgICB3aW5kb3cuc2Nyb2xsVG8oMCwgcGFyc2VJbnQoc2Nyb2xsWSB8fCAnMCcpICogLTEpO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gIH0pO1xufVxuXG5jb25zdCBzY3JvbGxBbmltYXRpb25EdXJhdGlvbiA9IDIwMDtcbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duU21vb3RoKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgICAgdG9wOiBlbGVtZW50LnNjcm9sbEhlaWdodCxcbiAgICAgIGJlaGF2aW9yOiAnc21vb3RoJyxcbiAgICB9KTtcbiAgfSwgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gc29jaWFsTWVkaWFTaGFyZSgpIHtcbiAgY29uc29sZS5sb2coJ3NvY2lhbE1lZGlhU2hhcmUnKTtcbiAgY29uc3QgZmJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmZiLXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgZmJTaGFyZUljb25zLmZvckVhY2goZmJJY29uID0+IHtcbiAgICBmYkljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGZiSWNvbi5ocmVmID0gYGh0dHBzOi8vd3d3LmZhY2Vib29rLmNvbS9zaGFyZS5waHA/dT0ke2xpbmt9YDtcbiAgICAgIGNvbnNvbGUubG9nKGZiSWNvbi5ocmVmKTtcbiAgICB9KTtcbiAgfSk7XG5cbiAgY29uc3QgaW5zdGFTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmktc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICBpbnN0YVNoYXJlSWNvbnMuZm9yRWFjaChpbnN0YUljb24gPT4ge1xuICAgIGluc3RhSWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgaW5zdGFJY29uLmhyZWYgPSBgaHR0cHM6Ly93d3cuaW5zdGFncmFtLmNvbWA7XG4gICAgICBjb25zb2xlLmxvZyhpbnN0YUljb24uaHJlZik7XG4gICAgfSk7XG4gIH0pO1xuXG4gIGNvbnN0IHR3aXR0ZXJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLngtc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICB0d2l0dGVyU2hhcmVJY29ucy5mb3JFYWNoKHR3aXR0ZXJJY29uID0+IHtcbiAgICB0d2l0dGVySWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgY29uc3QgdGV4dCA9IGVuY29kZVVSSUNvbXBvbmVudChcbiAgICAgICAgJ0NoZWNrIG91dCBjb29sIHRpY2tldHMgZm9yIHNhbGUgb24gRmFuVGlja2V0JyxcbiAgICAgICk7XG4gICAgICBjb25zdCBoYXNodGFncyA9IGVuY29kZVVSSUNvbXBvbmVudCgndGlja2V0cyxmb3JzYWxlJyk7XG4gICAgICB0d2l0dGVySWNvbi5ocmVmID0gYGh0dHBzOi8vdHdpdHRlci5jb20vc2hhcmU/dXJsPSR7bGlua30mdGV4dD0ke3RleHR9Jmhhc2h0YWdzPSR7aGFzaHRhZ3N9YDtcbiAgICAgIGNvbnNvbGUubG9nKHR3aXR0ZXJJY29uLmhyZWYpO1xuICAgIH0pO1xuICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGRpc2FibGVEYXRlRmxvd2JpdGUoKSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGNvbnN0IGFsbERhdGVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXItY2VsbCcpO1xuXG4gICAgY29uc3QgY3VycmVudE1vbnRoID0gbmV3IERhdGUoKS5nZXRNb250aCgpO1xuICAgIGFsbERhdGVzLmZvckVhY2goKGRhdGU6IEhUTUxEaXZFbGVtZW50KSA9PiB7XG4gICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICBjb25zdCBkYXRlTW9udGggPSBuZXcgRGF0ZShwYXJzZUludCh0aW1lU3RhbXApKS5nZXRNb250aCgpO1xuICAgICAgZGF0ZU1vbnRoICE9PSBjdXJyZW50TW9udGhcbiAgICAgICAgPyAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjOTlhMWEzJylcbiAgICAgICAgOiAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjZmZmJyk7XG4gICAgfSk7XG5cbiAgICBjb25zdCBjYWxlbmRhckJ1dHRvbnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcubmV4dC1idG4sIC5wcmV2LWJ0bicpO1xuXG4gICAgY2FsZW5kYXJCdXR0b25zLmZvckVhY2goKGJ1dHRvbjogSFRNTEJ1dHRvbkVsZW1lbnQpID0+IHtcbiAgICAgIGJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChldmVudDogRXZlbnQpID0+IHtcbiAgICAgICAgY29uc3QgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgICAgICBjb25zdCBkYXRlUGlja2VyID0gdGFyZ2V0LmNsb3Nlc3QoJy5kYXRlcGlja2VyLXBpY2tlcicpO1xuXG4gICAgICAgIGlmICghZGF0ZVBpY2tlcikgcmV0dXJuO1xuXG4gICAgICAgIGNvbnN0IG1vbnRoVGl0bGUgPSBkYXRlUGlja2VyLnF1ZXJ5U2VsZWN0b3IoJy52aWV3LXN3aXRjaCcpO1xuICAgICAgICBjb25zdCBtb250aCA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVswXTtcbiAgICAgICAgY29uc3QgeWVhciA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVsxXTtcbiAgICAgICAgY29uc3QgY3VycmVudERhdGUgPSBuZXcgRGF0ZShgJHttb250aH0gMSwgJHt5ZWFyfWApLmdldE1vbnRoKCk7XG4gICAgICAgIGNvbnN0IGFsbERhdGVzID0gZGF0ZVBpY2tlci5xdWVyeVNlbGVjdG9yQWxsKCcuZGF0ZXBpY2tlci1jZWxsJyk7XG5cbiAgICAgICAgYWxsRGF0ZXMuZm9yRWFjaCgoZGF0ZTogSFRNTERpdkVsZW1lbnQpID0+IHtcbiAgICAgICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICAgICAgY29uc3QgZGF0ZU1vbnRoID0gbmV3IERhdGUocGFyc2VJbnQodGltZVN0YW1wKSkuZ2V0TW9udGgoKTtcblxuICAgICAgICAgIGRhdGVNb250aCAhPT0gY3VycmVudERhdGVcbiAgICAgICAgICAgID8gKGRhdGUuc3R5bGUuY29sb3IgPSAnIzk5YTFhMycpXG4gICAgICAgICAgICA6IChkYXRlLnN0eWxlLmNvbG9yID0gJyNmZmYnKTtcbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfSwgMTAwMCk7XG59XG4iLCIvLyBUaGUgbW9kdWxlIGNhY2hlXG52YXIgX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fID0ge307XG5cbi8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG5mdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuXHR2YXIgY2FjaGVkTW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXTtcblx0aWYgKGNhY2hlZE1vZHVsZSAhPT0gdW5kZWZpbmVkKSB7XG5cdFx0cmV0dXJuIGNhY2hlZE1vZHVsZS5leHBvcnRzO1xuXHR9XG5cdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG5cdHZhciBtb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdID0ge1xuXHRcdC8vIG5vIG1vZHVsZS5pZCBuZWVkZWRcblx0XHQvLyBubyBtb2R1bGUubG9hZGVkIG5lZWRlZFxuXHRcdGV4cG9ydHM6IHt9XG5cdH07XG5cblx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG5cdF9fd2VicGFja19tb2R1bGVzX19bbW9kdWxlSWRdKG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG5cdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG5cdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbn1cblxuIiwiaW1wb3J0IHtoYW5kbGVIaWRlRWxlbWVudHN9IGZyb20gJy4vdXRpbHMnO1xuXG5jb25zb2xlLmxvZygnZmlsZSBhZG1pbi50cyBsb2FkZWQnKTtcbmNvbnNvbGUubG9nKCdhZG1pbi50cyBsb2FkZWQgNSByb3cnKTtcblxuY29uc3QgZGF0ZXNCdXR0b246IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2V2ZW50LWRhdGVzJyk7XG5jb25zdCBkYXRlc0Ryb3Bkb3duOiBIVE1MU2VsZWN0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICcjZXZlbnQtZGF0ZXMtZHJvcGRvd24nLFxuKTtcblxuZGF0ZXNCdXR0b24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gIGNvbnN0IGRhdGVQaWNrZXJzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXInKTtcbiAgY29uc3QgZGF0ZVBpY2tlckFycmF5OiBIVE1MRWxlbWVudFtdID0gQXJyYXkuZnJvbShcbiAgICBkYXRlUGlja2VycyxcbiAgKSBhcyBIVE1MRWxlbWVudFtdO1xuXG4gIGhhbmRsZUhpZGVFbGVtZW50cyhkYXRlc0Ryb3Bkb3duLCBkYXRlUGlja2VyQXJyYXkpO1xufSk7XG5cbmNvbnN0IHNlYXJjaElucHV0OiBIVE1MSW5wdXRFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgJyN0YWJsZS1zZWFyY2gtZXZlbnRzJyxcbik7XG5jb25zdCBzZWFyY2hJbnB1dEJ1dHRvbiA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyN0YWJsZS1zZWFyY2gtZXZlbnRzLWJ1dHRvbicpO1xuaWYgKHNlYXJjaElucHV0QnV0dG9uICYmIHNlYXJjaElucHV0KSB7XG4gIHNlYXJjaElucHV0QnV0dG9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgIHNlYXJjaElucHV0LnZhbHVlID0gJyc7XG4gICAgc2VhcmNoSW5wdXQuY2xpY2soKTtcbiAgfSk7XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=