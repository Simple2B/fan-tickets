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
  !*** ./src/event.ts ***!
  \**********************/

Object.defineProperty(exports, "__esModule", ({ value: true }));
var utils_1 = __webpack_require__(/*! ./utils */ "./src/utils.ts");
function filterDropdownLocation(dropdownList, dropdownInput) {
    var filter = dropdownInput.value.toUpperCase();
    for (var i = 0; i < dropdownList.length; i++) {
        var txtValue = dropdownList[i].textContent || dropdownList[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            dropdownList[i].style.display = '';
        }
        else {
            dropdownList[i].style.display = 'none';
        }
    }
}
document.addEventListener('DOMContentLoaded', function () {
    var buttonFilterDate = document.querySelector('#events-filter-date-button');
    var buttonLocation = document.querySelector('#events-filter-location-button');
    var buttonLocationNames = document.querySelectorAll('.dropdown-location-name-button');
    var buttonCategories = document.querySelector('#events-filter-categories-button');
    var buttonDateApply = document.querySelector('#events-filter-date-apply-button');
    var dropdownFilterDate = document.querySelector('#events-filter-date-dropdown');
    var dropdownFilterLocation = document.querySelector('#dropdown-location');
    var dropdownFilterCategories = document.querySelector('#events-filter-categories-dropdown');
    var statusFilterLocation = document.querySelector('#events-filter-location-status');
    if (buttonFilterDate) {
        buttonFilterDate.addEventListener('click', function () {
            var datePickers = document.querySelectorAll('.datepicker');
            var datePickerArray = Array.from(datePickers);
            (0, utils_1.handleHideElements)(dropdownFilterDate, datePickerArray);
        });
    }
    if (buttonDateApply) {
        buttonDateApply.addEventListener('click', function () {
            dropdownFilterDate.classList.toggle('hidden');
        });
    }
    if (buttonCategories) {
        buttonCategories.addEventListener('click', function () {
            (0, utils_1.handleHideElements)(dropdownFilterCategories);
        });
    }
    if (statusFilterLocation) {
        var dropDownLocationInput_1 = document.querySelector('#dropdown-location-input');
        if (buttonLocation) {
            buttonLocation.addEventListener('click', function () {
                dropDownLocationInput_1.focus();
                (0, utils_1.handleHideElements)(dropdownFilterLocation);
            });
        }
        buttonLocationNames.forEach(function (button) {
            button.addEventListener('click', function () {
                statusFilterLocation.innerHTML = button.innerHTML;
                (0, utils_1.handleHideElements)(dropdownFilterLocation);
            });
        });
        dropDownLocationInput_1.addEventListener('keyup', function () {
            filterDropdownLocation(buttonLocationNames, dropDownLocationInput_1);
        });
    }
});

})();

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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QUFNLENBQUMsUUFBUSxDQUFDLENBQUM7UUFDaEQsQ0FBQyxDQUFDLENBQUM7S0FDSjtJQUVELElBQUksZ0JBQWdCLEVBQUU7UUFDcEIsZ0JBQWdCLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1lBQ3pDLDhCQUFrQixFQUFDLHdCQUF3QixDQUFDLENBQUM7UUFDL0MsQ0FBQyxDQUFDLENBQUM7S0FDSjtJQUVELElBQUksb0JBQW9CLEVBQUU7UUFDeEIsSUFBTSx1QkFBcUIsR0FBcUIsUUFBUSxDQUFDLGFBQWEsQ0FDcEUsMEJBQTBCLENBQzNCLENBQUM7UUFFRixJQUFJLGNBQWMsRUFBRTtZQUNsQixjQUFjLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO2dCQUN2Qyx1QkFBcUIsQ0FBQyxLQUFLLEVBQUUsQ0FBQztnQkFDOUIsOEJBQWtCLEVBQUMsc0JBQXNCLENBQUMsQ0FBQztZQUM3QyxDQUFDLENBQUMsQ0FBQztTQUNKO1FBRUQsbUJBQW1CLENBQUMsT0FBTyxDQUFDLFVBQUMsTUFBc0I7WUFDakQsTUFBTSxDQUFDLGdCQUFnQixDQUFDLE9BQU8sRUFBRTtnQkFDL0Isb0JBQW9CLENBQUMsU0FBUyxHQUFHLE1BQU0sQ0FBQyxTQUFTLENBQUM7Z0JBQ2xELDhCQUFrQixFQUFDLHNCQUFzQixDQUFDLENBQUM7WUFDN0MsQ0FBQyxDQUFDLENBQUM7UUFDTCxDQUFDLENBQUMsQ0FBQztRQUNILHVCQUFxQixDQUFDLGdCQUFnQixDQUFDLE9BQU8sRUFBRTtZQUM5QyxzQkFBc0IsQ0FBQyxtQkFBbUIsRUFBRSx1QkFBcUIsQ0FBQyxDQUFDO1FBQ3JFLENBQUMsQ0FBQyxDQUFDO0tBQ0o7QUFDSCxDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy91dGlscy50cyIsIndlYnBhY2s6Ly9zdGF0aWMvd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL2V2ZW50LnRzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQ6IEhUTUxFbGVtZW50KSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG59XG5cbmZ1bmN0aW9uIGhpZGVFbGVtZW50cyhcbiAgZXZlbnQ6IE1vdXNlRXZlbnQsXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ/OiBIVE1MRWxlbWVudFtdLFxuKSB7XG4gIGlmIChcbiAgICAhZWxlbWVudC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkgJiZcbiAgICAhb3RoZXJFbGVtZW50LnNvbWUoZWwgPT4gZWwuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpKVxuICApIHtcbiAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgfVxufVxuXG4vLyBleHBvcnQgZnVuY3Rpb24gdW5sb2NrU2Nyb2xsKCkge1xuLy8gICBjb25zdCBzY3JvbGxZID0gZG9jdW1lbnQuYm9keS5zdHlsZS50b3A7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucG9zaXRpb24gPSAnJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS50b3AgPSAnJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5sZWZ0ID0gJyc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnJztcbi8vICAgd2luZG93LnNjcm9sbFRvKDAsIHBhcnNlSW50KHNjcm9sbFkgfHwgJzAnKSAqIC0xKTtcblxuLy8gICBjb25zb2xlLmxvZygndW5sb2NrIHNjcm9sbCcpO1xuLy8gfVxuXG4vLyBleHBvcnQgZnVuY3Rpb24gbG9ja1Njcm9sbCgpIHtcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5wb3NpdGlvbiA9ICdmaXhlZCc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUudG9wID0gYC0ke3dpbmRvdy5zY3JvbGxZfXB4YDtcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5sZWZ0ID0gJzAnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnJpZ2h0ID0gJzAnO1xuXG4vLyAgIGNvbnNvbGUubG9nKCdsb2NrIHNjcm9sbCcpO1xuLy8gfVxuXG5leHBvcnQgZnVuY3Rpb24gaGFuZGxlSGlkZUVsZW1lbnRzKFxuICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgb3RoZXJFbGVtZW50OiBIVE1MRWxlbWVudFtdID0gW10sXG4pIHtcbiAgZWxlbWVudC5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ21vdXNldXAnLCAoZXZlbnQ6IE1vdXNlRXZlbnQpID0+IHtcbiAgICBoaWRlRWxlbWVudHMoZXZlbnQsIGVsZW1lbnQsIG90aGVyRWxlbWVudCk7XG4gIH0pO1xuXG4gIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICBpZiAoZXZlbnQua2V5ID09PSAnRXNjYXBlJykge1xuICAgICAgYWRkSGlkZGVuQ2xhc3MoZWxlbWVudCk7XG4gICAgfVxuICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHJlc2l6ZUNoYXQoKSB7XG4gIGNvbnNvbGUubG9nKCdyZXNpemVDaGF0Jyk7XG4gIGNvbnN0IGhlYWRlcjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcuaGVhZGVyJyk7XG4gIGNvbnN0IGNoYXRNYWluOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWJvZHknKTtcbiAgY29uc3QgY2hhdEZvb3RlcjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC1mb290ZXInKTtcbiAgY29uc3QgY2hhdFdpbmRvdzogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC13aW5kb3cnKTtcbiAgY29uc3Qgc2NyZWVuV2l0aDogbnVtYmVyID0gd2luZG93LmlubmVyV2lkdGg7XG4gIGNvbnN0IGhlYWRlckJvdHRvbTogbnVtYmVyID0gaGVhZGVyLm9mZnNldFRvcCArIGhlYWRlci5vZmZzZXRIZWlnaHQ7XG4gIGNvbnN0IGNoYXRXaW5kb3dUb3A6IG51bWJlciA9IGNoYXRXaW5kb3cub2Zmc2V0VG9wO1xuICBjb25zdCBmaXhlZE1pbkRpc3RhbmNlOiBudW1iZXIgPSAyNTA7XG4gIGNvbnN0IG1heENoYXRXaW5kb3dIZWlnaHQ6IG51bWJlciA9IDY1MDtcbiAgY29uc3QgYXZhaWxhYmxlU3BhY2U6IG51bWJlciA9IGNoYXRXaW5kb3dUb3AgLSBoZWFkZXJCb3R0b207XG5cbiAgaWYgKHNjcmVlbldpdGggPCA2NDApIHtcbiAgICBjaGF0TWFpbi5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDAlIC0gJHtjaGF0Rm9vdGVyLm9mZnNldEhlaWdodH1weClgO1xuICAgIHJldHVybjtcbiAgfVxuXG4gIGlmICghaGVhZGVyIHx8ICFjaGF0V2luZG93KSByZXR1cm47XG5cbiAgaWYgKGF2YWlsYWJsZVNwYWNlIDwgZml4ZWRNaW5EaXN0YW5jZSkge1xuICAgIGNoYXRXaW5kb3cuc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwdmggLSAke2ZpeGVkTWluRGlzdGFuY2V9cHgpYDtcbiAgfVxuXG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGlmIChjaGF0V2luZG93Lm9mZnNldEhlaWdodCA+IG1heENoYXRXaW5kb3dIZWlnaHQpIHtcbiAgICAgIGNoYXRXaW5kb3cuc3R5bGUuaGVpZ2h0ID0gYCR7bWF4Q2hhdFdpbmRvd0hlaWdodH1weGA7XG4gICAgfVxuICB9LCA1MDApO1xuXG4gIGlmIChjaGF0TWFpbiAmJiBjaGF0Rm9vdGVyKSB7XG4gICAgY2hhdE1haW4uc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwJSAtICR7Y2hhdEZvb3Rlci5vZmZzZXRIZWlnaHR9cHgpYDtcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gbG9ja1Njcm9sbEJvZHkoKSB7XG4gIGNvbnNvbGUubG9nKCdsb2NrU2Nyb2xsQm9keScpO1xuXG4gIGNvbnN0IHNjcmVlbldpdGg6IG51bWJlciA9IHdpbmRvdy5pbm5lcldpZHRoO1xuICBpZiAoc2NyZWVuV2l0aCA8IDY0MCkge1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUub3ZlcmZsb3cgPSAnaGlkZGVuJztcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gdW5sb2NrU2Nyb2xsQm9keSgpIHtcbiAgY29uc29sZS5sb2coJ3VubG9ja1Njcm9sbEJvZHknKTtcblxuICBjb25zdCBzY3JlZW5XaXRoOiBudW1iZXIgPSB3aW5kb3cuaW5uZXJXaWR0aDtcbiAgaWYgKHNjcmVlbldpdGggPCA2NDApIHtcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLm92ZXJmbG93ID0gJ2F1dG8nO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gIH0pO1xufVxuXG5jb25zdCBzY3JvbGxBbmltYXRpb25EdXJhdGlvbiA9IDIwMDtcbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duU21vb3RoKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgICAgdG9wOiBlbGVtZW50LnNjcm9sbEhlaWdodCxcbiAgICAgIGJlaGF2aW9yOiAnc21vb3RoJyxcbiAgICB9KTtcbiAgfSwgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gc29jaWFsTWVkaWFTaGFyZSgpIHtcbiAgY29uc29sZS5sb2coJ3NvY2lhbE1lZGlhU2hhcmUnKTtcbiAgY29uc3QgZmJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmZiLXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgZmJTaGFyZUljb25zLmZvckVhY2goZmJJY29uID0+IHtcbiAgICBmYkljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGZiSWNvbi5ocmVmID0gYGh0dHBzOi8vd3d3LmZhY2Vib29rLmNvbS9zaGFyZS5waHA/dT0ke2xpbmt9YDtcbiAgICAgIGNvbnNvbGUubG9nKGZiSWNvbi5ocmVmKTtcbiAgICB9KTtcbiAgfSk7XG5cbiAgY29uc3QgaW5zdGFTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmktc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICBpbnN0YVNoYXJlSWNvbnMuZm9yRWFjaChpbnN0YUljb24gPT4ge1xuICAgIGluc3RhSWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgaW5zdGFJY29uLmhyZWYgPSBgaHR0cHM6Ly93d3cuaW5zdGFncmFtLmNvbWA7XG4gICAgICBjb25zb2xlLmxvZyhpbnN0YUljb24uaHJlZik7XG4gICAgfSk7XG4gIH0pO1xuXG4gIGNvbnN0IHR3aXR0ZXJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLngtc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICB0d2l0dGVyU2hhcmVJY29ucy5mb3JFYWNoKHR3aXR0ZXJJY29uID0+IHtcbiAgICB0d2l0dGVySWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgY29uc3QgdGV4dCA9IGVuY29kZVVSSUNvbXBvbmVudChcbiAgICAgICAgJ0NoZWNrIG91dCBjb29sIHRpY2tldHMgZm9yIHNhbGUgb24gRmFuVGlja2V0JyxcbiAgICAgICk7XG4gICAgICBjb25zdCBoYXNodGFncyA9IGVuY29kZVVSSUNvbXBvbmVudCgndGlja2V0cyxmb3JzYWxlJyk7XG4gICAgICB0d2l0dGVySWNvbi5ocmVmID0gYGh0dHBzOi8vdHdpdHRlci5jb20vc2hhcmU/dXJsPSR7bGlua30mdGV4dD0ke3RleHR9Jmhhc2h0YWdzPSR7aGFzaHRhZ3N9YDtcbiAgICAgIGNvbnNvbGUubG9nKHR3aXR0ZXJJY29uLmhyZWYpO1xuICAgIH0pO1xuICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGRpc2FibGVEYXRlRmxvd2JpdGUoKSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGNvbnN0IGFsbERhdGVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXItY2VsbCcpO1xuXG4gICAgY29uc3QgY3VycmVudE1vbnRoID0gbmV3IERhdGUoKS5nZXRNb250aCgpO1xuICAgIGFsbERhdGVzLmZvckVhY2goKGRhdGU6IEhUTUxEaXZFbGVtZW50KSA9PiB7XG4gICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICBjb25zdCBkYXRlTW9udGggPSBuZXcgRGF0ZShwYXJzZUludCh0aW1lU3RhbXApKS5nZXRNb250aCgpO1xuICAgICAgZGF0ZU1vbnRoICE9PSBjdXJyZW50TW9udGhcbiAgICAgICAgPyAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjOTlhMWEzJylcbiAgICAgICAgOiAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjZmZmJyk7XG4gICAgfSk7XG5cbiAgICBjb25zdCBjYWxlbmRhckJ1dHRvbnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcubmV4dC1idG4sIC5wcmV2LWJ0bicpO1xuXG4gICAgY2FsZW5kYXJCdXR0b25zLmZvckVhY2goKGJ1dHRvbjogSFRNTEJ1dHRvbkVsZW1lbnQpID0+IHtcbiAgICAgIGJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChldmVudDogRXZlbnQpID0+IHtcbiAgICAgICAgY29uc3QgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgICAgICBjb25zdCBkYXRlUGlja2VyID0gdGFyZ2V0LmNsb3Nlc3QoJy5kYXRlcGlja2VyLXBpY2tlcicpO1xuXG4gICAgICAgIGlmICghZGF0ZVBpY2tlcikgcmV0dXJuO1xuXG4gICAgICAgIGNvbnN0IG1vbnRoVGl0bGUgPSBkYXRlUGlja2VyLnF1ZXJ5U2VsZWN0b3IoJy52aWV3LXN3aXRjaCcpO1xuICAgICAgICBjb25zdCBtb250aCA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVswXTtcbiAgICAgICAgY29uc3QgeWVhciA9IG1vbnRoVGl0bGUudGV4dENvbnRlbnQuc3BsaXQoJyAnKVsxXTtcbiAgICAgICAgY29uc3QgY3VycmVudERhdGUgPSBuZXcgRGF0ZShgJHttb250aH0gMSwgJHt5ZWFyfWApLmdldE1vbnRoKCk7XG4gICAgICAgIGNvbnN0IGFsbERhdGVzID0gZGF0ZVBpY2tlci5xdWVyeVNlbGVjdG9yQWxsKCcuZGF0ZXBpY2tlci1jZWxsJyk7XG5cbiAgICAgICAgYWxsRGF0ZXMuZm9yRWFjaCgoZGF0ZTogSFRNTERpdkVsZW1lbnQpID0+IHtcbiAgICAgICAgICBjb25zdCB0aW1lU3RhbXAgPSBkYXRlLmdldEF0dHJpYnV0ZSgnZGF0YS1kYXRlJyk7XG4gICAgICAgICAgY29uc3QgZGF0ZU1vbnRoID0gbmV3IERhdGUocGFyc2VJbnQodGltZVN0YW1wKSkuZ2V0TW9udGgoKTtcblxuICAgICAgICAgIGRhdGVNb250aCAhPT0gY3VycmVudERhdGVcbiAgICAgICAgICAgID8gKGRhdGUuc3R5bGUuY29sb3IgPSAnIzk5YTFhMycpXG4gICAgICAgICAgICA6IChkYXRlLnN0eWxlLmNvbG9yID0gJyNmZmYnKTtcbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfSwgMTAwMCk7XG59XG4iLCIvLyBUaGUgbW9kdWxlIGNhY2hlXG52YXIgX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fID0ge307XG5cbi8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG5mdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuXHR2YXIgY2FjaGVkTW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXTtcblx0aWYgKGNhY2hlZE1vZHVsZSAhPT0gdW5kZWZpbmVkKSB7XG5cdFx0cmV0dXJuIGNhY2hlZE1vZHVsZS5leHBvcnRzO1xuXHR9XG5cdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG5cdHZhciBtb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdID0ge1xuXHRcdC8vIG5vIG1vZHVsZS5pZCBuZWVkZWRcblx0XHQvLyBubyBtb2R1bGUubG9hZGVkIG5lZWRlZFxuXHRcdGV4cG9ydHM6IHt9XG5cdH07XG5cblx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG5cdF9fd2VicGFja19tb2R1bGVzX19bbW9kdWxlSWRdKG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG5cdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG5cdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbn1cblxuIiwiaW1wb3J0IHtoYW5kbGVIaWRlRWxlbWVudHN9IGZyb20gJy4vdXRpbHMnO1xuXG5mdW5jdGlvbiBmaWx0ZXJEcm9wZG93bkxvY2F0aW9uKFxuICBkcm9wZG93bkxpc3Q6IE5vZGVMaXN0T2Y8SFRNTERpdkVsZW1lbnQ+LFxuICBkcm9wZG93bklucHV0OiBIVE1MSW5wdXRFbGVtZW50LFxuKSB7XG4gIGNvbnN0IGZpbHRlciA9IGRyb3Bkb3duSW5wdXQudmFsdWUudG9VcHBlckNhc2UoKTtcblxuICBmb3IgKGxldCBpID0gMDsgaSA8IGRyb3Bkb3duTGlzdC5sZW5ndGg7IGkrKykge1xuICAgIGNvbnN0IHR4dFZhbHVlID0gZHJvcGRvd25MaXN0W2ldLnRleHRDb250ZW50IHx8IGRyb3Bkb3duTGlzdFtpXS5pbm5lclRleHQ7XG4gICAgaWYgKHR4dFZhbHVlLnRvVXBwZXJDYXNlKCkuaW5kZXhPZihmaWx0ZXIpID4gLTEpIHtcbiAgICAgIGRyb3Bkb3duTGlzdFtpXS5zdHlsZS5kaXNwbGF5ID0gJyc7XG4gICAgfSBlbHNlIHtcbiAgICAgIGRyb3Bkb3duTGlzdFtpXS5zdHlsZS5kaXNwbGF5ID0gJ25vbmUnO1xuICAgIH1cbiAgfVxufVxuXG5kb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgZnVuY3Rpb24gKCkge1xuICBjb25zdCBidXR0b25GaWx0ZXJEYXRlID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2V2ZW50cy1maWx0ZXItZGF0ZS1idXR0b24nKTtcbiAgY29uc3QgYnV0dG9uTG9jYXRpb246IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24tYnV0dG9uJyxcbiAgKTtcbiAgY29uc3QgYnV0dG9uTG9jYXRpb25OYW1lcyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXG4gICAgJy5kcm9wZG93bi1sb2NhdGlvbi1uYW1lLWJ1dHRvbicsXG4gICkgYXMgTm9kZUxpc3RPZjxIVE1MRGl2RWxlbWVudD47XG5cbiAgY29uc3QgYnV0dG9uQ2F0ZWdvcmllcyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWNhdGVnb3JpZXMtYnV0dG9uJyxcbiAgKTtcbiAgY29uc3QgYnV0dG9uRGF0ZUFwcGx5ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItZGF0ZS1hcHBseS1idXR0b24nLFxuICApO1xuXG4gIGNvbnN0IGRyb3Bkb3duRmlsdGVyRGF0ZTogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1kYXRlLWRyb3Bkb3duJyxcbiAgKTtcbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJMb2NhdGlvbjogSFRNTERpdkVsZW1lbnQgPVxuICAgIGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNkcm9wZG93bi1sb2NhdGlvbicpO1xuICBjb25zdCBkcm9wZG93bkZpbHRlckNhdGVnb3JpZXM6IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItY2F0ZWdvcmllcy1kcm9wZG93bicsXG4gICk7XG5cbiAgY29uc3Qgc3RhdHVzRmlsdGVyTG9jYXRpb24gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1sb2NhdGlvbi1zdGF0dXMnLFxuICApO1xuXG4gIGlmIChidXR0b25GaWx0ZXJEYXRlKSB7XG4gICAgYnV0dG9uRmlsdGVyRGF0ZS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGRhdGVQaWNrZXJzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXInKTtcbiAgICAgIGNvbnN0IGRhdGVQaWNrZXJBcnJheTogSFRNTEVsZW1lbnRbXSA9IEFycmF5LmZyb20oXG4gICAgICAgIGRhdGVQaWNrZXJzLFxuICAgICAgKSBhcyBIVE1MRWxlbWVudFtdO1xuXG4gICAgICBoYW5kbGVIaWRlRWxlbWVudHMoZHJvcGRvd25GaWx0ZXJEYXRlLCBkYXRlUGlja2VyQXJyYXkpO1xuICAgIH0pO1xuICB9XG5cbiAgaWYgKGJ1dHRvbkRhdGVBcHBseSkge1xuICAgIGJ1dHRvbkRhdGVBcHBseS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGRyb3Bkb3duRmlsdGVyRGF0ZS5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChidXR0b25DYXRlZ29yaWVzKSB7XG4gICAgYnV0dG9uQ2F0ZWdvcmllcy5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGhhbmRsZUhpZGVFbGVtZW50cyhkcm9wZG93bkZpbHRlckNhdGVnb3JpZXMpO1xuICAgIH0pO1xuICB9XG5cbiAgaWYgKHN0YXR1c0ZpbHRlckxvY2F0aW9uKSB7XG4gICAgY29uc3QgZHJvcERvd25Mb2NhdGlvbklucHV0OiBIVE1MSW5wdXRFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAgICcjZHJvcGRvd24tbG9jYXRpb24taW5wdXQnLFxuICAgICk7XG5cbiAgICBpZiAoYnV0dG9uTG9jYXRpb24pIHtcbiAgICAgIGJ1dHRvbkxvY2F0aW9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgICBkcm9wRG93bkxvY2F0aW9uSW5wdXQuZm9jdXMoKTtcbiAgICAgICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyTG9jYXRpb24pO1xuICAgICAgfSk7XG4gICAgfVxuXG4gICAgYnV0dG9uTG9jYXRpb25OYW1lcy5mb3JFYWNoKChidXR0b246IEhUTUxEaXZFbGVtZW50KSA9PiB7XG4gICAgICBidXR0b24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICAgIHN0YXR1c0ZpbHRlckxvY2F0aW9uLmlubmVySFRNTCA9IGJ1dHRvbi5pbm5lckhUTUw7XG4gICAgICAgIGhhbmRsZUhpZGVFbGVtZW50cyhkcm9wZG93bkZpbHRlckxvY2F0aW9uKTtcbiAgICAgIH0pO1xuICAgIH0pO1xuICAgIGRyb3BEb3duTG9jYXRpb25JbnB1dC5hZGRFdmVudExpc3RlbmVyKCdrZXl1cCcsICgpID0+IHtcbiAgICAgIGZpbHRlckRyb3Bkb3duTG9jYXRpb24oYnV0dG9uTG9jYXRpb25OYW1lcywgZHJvcERvd25Mb2NhdGlvbklucHV0KTtcbiAgICB9KTtcbiAgfVxufSk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=