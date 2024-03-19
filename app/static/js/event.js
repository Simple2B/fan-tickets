/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/utils.ts":
/*!**********************!*\
  !*** ./src/utils.ts ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.socialMediaShare = exports.scrollDownSmooth = exports.scrollDown = exports.resizeChat = exports.handleHideElements = exports.lockScroll = exports.unlockScroll = void 0;
function addHiddenClass(element) {
    element.classList.add('hidden');
}
function hideElements(event, element, otherElement) {
    if (!element.contains(event.target) &&
        !otherElement.some(function (el) { return el.contains(event.target); })) {
        addHiddenClass(element);
    }
}
function unlockScroll() {
    var scrollY = this.body.style.top;
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    window.scrollTo(0, parseInt(scrollY || '0') * -1);
    console.log('unlock scroll');
}
exports.unlockScroll = unlockScroll;
function lockScroll() {
    document.body.style.position = 'fixed';
    document.body.style.top = "-".concat(window.scrollY, "px");
    document.body.style.left = '0';
    document.body.style.right = '0';
    console.log('lock scroll');
}
exports.lockScroll = lockScroll;
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
    var header = document.querySelector('.header');
    var chatMain = document.querySelector('#chat-body');
    var chatFooter = document.querySelector('#chat-footer');
    var chatWindow = document.querySelector('#chat-window');
    var screenWith = window.innerWidth;
    var headerBottom = header.offsetTop + header.offsetHeight;
    var chatWindowTop = chatWindow.offsetTop;
    var fixedMinDistance = 220;
    var maxChatWindowHeight = 650;
    var availableSpace = chatWindowTop - headerBottom;
    if (screenWith < 640) {
        chatMain.style.height = "calc(100% - ".concat(chatFooter.offsetHeight, "px)");
        lockScroll();
        return;
    }
    if (!header || !chatWindow)
        return;
    if (availableSpace < fixedMinDistance) {
        chatWindow.style.height = "calc(100vh - ".concat(fixedMinDistance, "px)");
    }
    if (chatWindow.offsetHeight > maxChatWindowHeight) {
        chatWindow.style.height = "".concat(maxChatWindowHeight, "px");
    }
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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QUMsQ0FBQztRQUNILHVCQUFxQixDQUFDLGdCQUFnQixDQUFDLE9BQU8sRUFBRTtZQUM5QyxzQkFBc0IsQ0FBQyxtQkFBbUIsRUFBRSx1QkFBcUIsQ0FBQyxDQUFDO1FBQ3JFLENBQUMsQ0FBQyxDQUFDO0tBQ0o7QUFDSCxDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy91dGlscy50cyIsIndlYnBhY2s6Ly9zdGF0aWMvd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL2V2ZW50LnRzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQ6IEhUTUxFbGVtZW50KSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG59XG5cbmZ1bmN0aW9uIGhpZGVFbGVtZW50cyhcbiAgZXZlbnQ6IE1vdXNlRXZlbnQsXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ/OiBIVE1MRWxlbWVudFtdLFxuKSB7XG4gIGlmIChcbiAgICAhZWxlbWVudC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkgJiZcbiAgICAhb3RoZXJFbGVtZW50LnNvbWUoZWwgPT4gZWwuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpKVxuICApIHtcbiAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gdW5sb2NrU2Nyb2xsKCkge1xuICBjb25zdCBzY3JvbGxZID0gdGhpcy5ib2R5LnN0eWxlLnRvcDtcbiAgZG9jdW1lbnQuYm9keS5zdHlsZS5wb3NpdGlvbiA9ICcnO1xuICBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcCA9ICcnO1xuICBkb2N1bWVudC5ib2R5LnN0eWxlLmxlZnQgPSAnJztcbiAgZG9jdW1lbnQuYm9keS5zdHlsZS5yaWdodCA9ICcnO1xuICB3aW5kb3cuc2Nyb2xsVG8oMCwgcGFyc2VJbnQoc2Nyb2xsWSB8fCAnMCcpICogLTEpO1xuXG4gIGNvbnNvbGUubG9nKCd1bmxvY2sgc2Nyb2xsJyk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBsb2NrU2Nyb2xsKCkge1xuICBkb2N1bWVudC5ib2R5LnN0eWxlLnBvc2l0aW9uID0gJ2ZpeGVkJztcbiAgZG9jdW1lbnQuYm9keS5zdHlsZS50b3AgPSBgLSR7d2luZG93LnNjcm9sbFl9cHhgO1xuICBkb2N1bWVudC5ib2R5LnN0eWxlLmxlZnQgPSAnMCc7XG4gIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnMCc7XG5cbiAgY29uc29sZS5sb2coJ2xvY2sgc2Nyb2xsJyk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBoYW5kbGVIaWRlRWxlbWVudHMoXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ6IEhUTUxFbGVtZW50W10gPSBbXSxcbikge1xuICBlbGVtZW50LmNsYXNzTGlzdC50b2dnbGUoJ2hpZGRlbicpO1xuICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsIChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICAgIGhpZGVFbGVtZW50cyhldmVudCwgZWxlbWVudCwgb3RoZXJFbGVtZW50KTtcbiAgfSk7XG5cbiAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIGZ1bmN0aW9uIChldmVudCkge1xuICAgIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgICB9XG4gIH0pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVzaXplQ2hhdCgpIHtcbiAgY29uc3QgaGVhZGVyOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5oZWFkZXInKTtcbiAgY29uc3QgY2hhdE1haW46IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtYm9keScpO1xuICBjb25zdCBjaGF0Rm9vdGVyOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWZvb3RlcicpO1xuICBjb25zdCBjaGF0V2luZG93OiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LXdpbmRvdycpO1xuICBjb25zdCBzY3JlZW5XaXRoOiBudW1iZXIgPSB3aW5kb3cuaW5uZXJXaWR0aDtcbiAgY29uc3QgaGVhZGVyQm90dG9tOiBudW1iZXIgPSBoZWFkZXIub2Zmc2V0VG9wICsgaGVhZGVyLm9mZnNldEhlaWdodDtcbiAgY29uc3QgY2hhdFdpbmRvd1RvcDogbnVtYmVyID0gY2hhdFdpbmRvdy5vZmZzZXRUb3A7XG4gIGNvbnN0IGZpeGVkTWluRGlzdGFuY2U6IG51bWJlciA9IDIyMDtcbiAgY29uc3QgbWF4Q2hhdFdpbmRvd0hlaWdodDogbnVtYmVyID0gNjUwO1xuICBjb25zdCBhdmFpbGFibGVTcGFjZTogbnVtYmVyID0gY2hhdFdpbmRvd1RvcCAtIGhlYWRlckJvdHRvbTtcblxuICBpZiAoc2NyZWVuV2l0aCA8IDY0MCkge1xuICAgIGNoYXRNYWluLnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMCUgLSAke2NoYXRGb290ZXIub2Zmc2V0SGVpZ2h0fXB4KWA7XG5cbiAgICBsb2NrU2Nyb2xsKCk7XG4gICAgcmV0dXJuO1xuICB9XG5cbiAgaWYgKCFoZWFkZXIgfHwgIWNoYXRXaW5kb3cpIHJldHVybjtcblxuICBpZiAoYXZhaWxhYmxlU3BhY2UgPCBmaXhlZE1pbkRpc3RhbmNlKSB7XG4gICAgY2hhdFdpbmRvdy5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDB2aCAtICR7Zml4ZWRNaW5EaXN0YW5jZX1weClgO1xuICB9XG4gIGlmIChjaGF0V2luZG93Lm9mZnNldEhlaWdodCA+IG1heENoYXRXaW5kb3dIZWlnaHQpIHtcbiAgICBjaGF0V2luZG93LnN0eWxlLmhlaWdodCA9IGAke21heENoYXRXaW5kb3dIZWlnaHR9cHhgO1xuICB9XG5cbiAgaWYgKGNoYXRNYWluICYmIGNoYXRGb290ZXIpIHtcbiAgICBjaGF0TWFpbi5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDAlIC0gJHtjaGF0Rm9vdGVyLm9mZnNldEhlaWdodH1weClgO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gIH0pO1xufVxuXG5jb25zdCBzY3JvbGxBbmltYXRpb25EdXJhdGlvbiA9IDIwMDtcbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duU21vb3RoKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgICAgdG9wOiBlbGVtZW50LnNjcm9sbEhlaWdodCxcbiAgICAgIGJlaGF2aW9yOiAnc21vb3RoJyxcbiAgICB9KTtcbiAgfSwgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gc29jaWFsTWVkaWFTaGFyZSgpIHtcbiAgY29uc29sZS5sb2coJ3NvY2lhbE1lZGlhU2hhcmUnKTtcbiAgY29uc3QgZmJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmZiLXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgZmJTaGFyZUljb25zLmZvckVhY2goZmJJY29uID0+IHtcbiAgICBmYkljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGZiSWNvbi5ocmVmID0gYGh0dHBzOi8vd3d3LmZhY2Vib29rLmNvbS9zaGFyZS5waHA/dT0ke2xpbmt9YDtcbiAgICAgIGNvbnNvbGUubG9nKGZiSWNvbi5ocmVmKTtcbiAgICB9KTtcbiAgfSk7XG5cbiAgY29uc3QgaW5zdGFTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmktc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICBpbnN0YVNoYXJlSWNvbnMuZm9yRWFjaChpbnN0YUljb24gPT4ge1xuICAgIGluc3RhSWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgaW5zdGFJY29uLmhyZWYgPSBgaHR0cHM6Ly93d3cuaW5zdGFncmFtLmNvbWA7XG4gICAgICBjb25zb2xlLmxvZyhpbnN0YUljb24uaHJlZik7XG4gICAgfSk7XG4gIH0pO1xuXG4gIGNvbnN0IHR3aXR0ZXJTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLngtc2hhcmUnLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xuICB0d2l0dGVyU2hhcmVJY29ucy5mb3JFYWNoKHR3aXR0ZXJJY29uID0+IHtcbiAgICB0d2l0dGVySWNvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgICAgY29uc3QgdGV4dCA9IGVuY29kZVVSSUNvbXBvbmVudChcbiAgICAgICAgJ0NoZWNrIG91dCBjb29sIHRpY2tldHMgZm9yIHNhbGUgb24gRmFuVGlja2V0JyxcbiAgICAgICk7XG4gICAgICBjb25zdCBoYXNodGFncyA9IGVuY29kZVVSSUNvbXBvbmVudCgndGlja2V0cyxmb3JzYWxlJyk7XG4gICAgICB0d2l0dGVySWNvbi5ocmVmID0gYGh0dHBzOi8vdHdpdHRlci5jb20vc2hhcmU/dXJsPSR7bGlua30mdGV4dD0ke3RleHR9Jmhhc2h0YWdzPSR7aGFzaHRhZ3N9YDtcbiAgICAgIGNvbnNvbGUubG9nKHR3aXR0ZXJJY29uLmhyZWYpO1xuICAgIH0pO1xuICB9KTtcbn1cbiIsIi8vIFRoZSBtb2R1bGUgY2FjaGVcbnZhciBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX18gPSB7fTtcblxuLy8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbmZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG5cdHZhciBjYWNoZWRNb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdO1xuXHRpZiAoY2FjaGVkTW9kdWxlICE9PSB1bmRlZmluZWQpIHtcblx0XHRyZXR1cm4gY2FjaGVkTW9kdWxlLmV4cG9ydHM7XG5cdH1cblx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcblx0dmFyIG1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF0gPSB7XG5cdFx0Ly8gbm8gbW9kdWxlLmlkIG5lZWRlZFxuXHRcdC8vIG5vIG1vZHVsZS5sb2FkZWQgbmVlZGVkXG5cdFx0ZXhwb3J0czoge31cblx0fTtcblxuXHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cblx0X193ZWJwYWNrX21vZHVsZXNfX1ttb2R1bGVJZF0obW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cblx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcblx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xufVxuXG4iLCJpbXBvcnQge2hhbmRsZUhpZGVFbGVtZW50c30gZnJvbSAnLi91dGlscyc7XG5cbmZ1bmN0aW9uIGZpbHRlckRyb3Bkb3duTG9jYXRpb24oXG4gIGRyb3Bkb3duTGlzdDogTm9kZUxpc3RPZjxIVE1MRGl2RWxlbWVudD4sXG4gIGRyb3Bkb3duSW5wdXQ6IEhUTUxJbnB1dEVsZW1lbnQsXG4pIHtcbiAgY29uc3QgZmlsdGVyID0gZHJvcGRvd25JbnB1dC52YWx1ZS50b1VwcGVyQ2FzZSgpO1xuXG4gIGZvciAobGV0IGkgPSAwOyBpIDwgZHJvcGRvd25MaXN0Lmxlbmd0aDsgaSsrKSB7XG4gICAgY29uc3QgdHh0VmFsdWUgPSBkcm9wZG93bkxpc3RbaV0udGV4dENvbnRlbnQgfHwgZHJvcGRvd25MaXN0W2ldLmlubmVyVGV4dDtcbiAgICBpZiAodHh0VmFsdWUudG9VcHBlckNhc2UoKS5pbmRleE9mKGZpbHRlcikgPiAtMSkge1xuICAgICAgZHJvcGRvd25MaXN0W2ldLnN0eWxlLmRpc3BsYXkgPSAnJztcbiAgICB9IGVsc2Uge1xuICAgICAgZHJvcGRvd25MaXN0W2ldLnN0eWxlLmRpc3BsYXkgPSAnbm9uZSc7XG4gICAgfVxuICB9XG59XG5cbmRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCBmdW5jdGlvbiAoKSB7XG4gIGNvbnN0IGJ1dHRvbkZpbHRlckRhdGUgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjZXZlbnRzLWZpbHRlci1kYXRlLWJ1dHRvbicpO1xuICBjb25zdCBidXR0b25Mb2NhdGlvbjogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1sb2NhdGlvbi1idXR0b24nLFxuICApO1xuICBjb25zdCBidXR0b25Mb2NhdGlvbk5hbWVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmRyb3Bkb3duLWxvY2F0aW9uLW5hbWUtYnV0dG9uJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxEaXZFbGVtZW50PjtcblxuICBjb25zdCBidXR0b25DYXRlZ29yaWVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItY2F0ZWdvcmllcy1idXR0b24nLFxuICApO1xuICBjb25zdCBidXR0b25EYXRlQXBwbHkgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1kYXRlLWFwcGx5LWJ1dHRvbicsXG4gICk7XG5cbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJEYXRlOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWRhdGUtZHJvcGRvd24nLFxuICApO1xuICBjb25zdCBkcm9wZG93bkZpbHRlckxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9XG4gICAgZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2Ryb3Bkb3duLWxvY2F0aW9uJyk7XG4gIGNvbnN0IGRyb3Bkb3duRmlsdGVyQ2F0ZWdvcmllczogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1jYXRlZ29yaWVzLWRyb3Bkb3duJyxcbiAgKTtcblxuICBjb25zdCBzdGF0dXNGaWx0ZXJMb2NhdGlvbiA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLXN0YXR1cycsXG4gICk7XG5cbiAgaWYgKGJ1dHRvbkZpbHRlckRhdGUpIHtcbiAgICBidXR0b25GaWx0ZXJEYXRlLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgY29uc3QgZGF0ZVBpY2tlcnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcuZGF0ZXBpY2tlcicpO1xuICAgICAgY29uc3QgZGF0ZVBpY2tlckFycmF5OiBIVE1MRWxlbWVudFtdID0gQXJyYXkuZnJvbShcbiAgICAgICAgZGF0ZVBpY2tlcnMsXG4gICAgICApIGFzIEhUTUxFbGVtZW50W107XG5cbiAgICAgIGhhbmRsZUhpZGVFbGVtZW50cyhkcm9wZG93bkZpbHRlckRhdGUsIGRhdGVQaWNrZXJBcnJheSk7XG4gICAgfSk7XG4gIH1cblxuICBpZiAoYnV0dG9uRGF0ZUFwcGx5KSB7XG4gICAgYnV0dG9uRGF0ZUFwcGx5LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgZHJvcGRvd25GaWx0ZXJEYXRlLmNsYXNzTGlzdC50b2dnbGUoJ2hpZGRlbicpO1xuICAgIH0pO1xuICB9XG5cbiAgaWYgKGJ1dHRvbkNhdGVnb3JpZXMpIHtcbiAgICBidXR0b25DYXRlZ29yaWVzLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyQ2F0ZWdvcmllcyk7XG4gICAgfSk7XG4gIH1cblxuICBpZiAoc3RhdHVzRmlsdGVyTG9jYXRpb24pIHtcbiAgICBjb25zdCBkcm9wRG93bkxvY2F0aW9uSW5wdXQ6IEhUTUxJbnB1dEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICAgJyNkcm9wZG93bi1sb2NhdGlvbi1pbnB1dCcsXG4gICAgKTtcblxuICAgIGlmIChidXR0b25Mb2NhdGlvbikge1xuICAgICAgYnV0dG9uTG9jYXRpb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICAgIGRyb3BEb3duTG9jYXRpb25JbnB1dC5mb2N1cygpO1xuICAgICAgICBoYW5kbGVIaWRlRWxlbWVudHMoZHJvcGRvd25GaWx0ZXJMb2NhdGlvbik7XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBidXR0b25Mb2NhdGlvbk5hbWVzLmZvckVhY2goKGJ1dHRvbjogSFRNTERpdkVsZW1lbnQpID0+IHtcbiAgICAgIGJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgICAgc3RhdHVzRmlsdGVyTG9jYXRpb24uaW5uZXJIVE1MID0gYnV0dG9uLmlubmVySFRNTDtcbiAgICAgICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyTG9jYXRpb24pO1xuICAgICAgfSk7XG4gICAgfSk7XG4gICAgZHJvcERvd25Mb2NhdGlvbklucHV0LmFkZEV2ZW50TGlzdGVuZXIoJ2tleXVwJywgKCkgPT4ge1xuICAgICAgZmlsdGVyRHJvcGRvd25Mb2NhdGlvbihidXR0b25Mb2NhdGlvbk5hbWVzLCBkcm9wRG93bkxvY2F0aW9uSW5wdXQpO1xuICAgIH0pO1xuICB9XG59KTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==