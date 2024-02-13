/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/utils.ts":
/*!**********************!*\
  !*** ./src/utils.ts ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.scrollDownSmooth = exports.scrollDown = exports.resizeChat = exports.handleHideElements = void 0;
function addHiddenClass(element) {
    element.classList.add('hidden');
}
function hideElements(event, element, otherElement) {
    if (!element.contains(event.target) &&
        !otherElement.some(function (el) { return el.contains(event.target); })) {
        addHiddenClass(element);
    }
}
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
    if (!header || !chatWindow)
        return;
    var headerBottom = header.offsetTop + header.offsetHeight;
    var chatWindowTop = chatWindow.offsetTop;
    var fixedMinDistance = 220;
    var maxChatWindowHeight = 650;
    var availableSpace = chatWindowTop - headerBottom;
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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Z0IsQ0FBQyxPQUFPLEVBQUU7UUFDMUMsV0FBVyxDQUFDLEtBQUssR0FBRyxFQUFFLENBQUM7UUFDdkIsV0FBVyxDQUFDLEtBQUssRUFBRSxDQUFDO0lBQ3RCLENBQUMsQ0FBQyxDQUFDO0NBQ0oiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvdXRpbHMudHMiLCJ3ZWJwYWNrOi8vc3RhdGljL3dlYnBhY2svYm9vdHN0cmFwIiwid2VicGFjazovL3N0YXRpYy8uL3NyYy9hZG1pbi50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiBhZGRIaWRkZW5DbGFzcyhlbGVtZW50OiBIVE1MRWxlbWVudCkge1xuICBlbGVtZW50LmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xufVxuXG5mdW5jdGlvbiBoaWRlRWxlbWVudHMoXG4gIGV2ZW50OiBNb3VzZUV2ZW50LFxuICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgb3RoZXJFbGVtZW50PzogSFRNTEVsZW1lbnRbXSxcbikge1xuICBpZiAoXG4gICAgIWVsZW1lbnQuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpICYmXG4gICAgIW90aGVyRWxlbWVudC5zb21lKGVsID0+IGVsLmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSlcbiAgKSB7XG4gICAgYWRkSGlkZGVuQ2xhc3MoZWxlbWVudCk7XG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGhhbmRsZUhpZGVFbGVtZW50cyhcbiAgZWxlbWVudDogSFRNTEVsZW1lbnQsXG4gIG90aGVyRWxlbWVudDogSFRNTEVsZW1lbnRbXSA9IFtdLFxuKSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gIHdpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdtb3VzZXVwJywgKGV2ZW50OiBNb3VzZUV2ZW50KSA9PiB7XG4gICAgaGlkZUVsZW1lbnRzKGV2ZW50LCBlbGVtZW50LCBvdGhlckVsZW1lbnQpO1xuICB9KTtcblxuICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdrZXlkb3duJywgZnVuY3Rpb24gKGV2ZW50KSB7XG4gICAgaWYgKGV2ZW50LmtleSA9PT0gJ0VzY2FwZScpIHtcbiAgICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICAgIH1cbiAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZXNpemVDaGF0KCkge1xuICBjb25zdCBoZWFkZXI6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLmhlYWRlcicpO1xuICBjb25zdCBjaGF0TWFpbjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC1ib2R5Jyk7XG4gIGNvbnN0IGNoYXRGb290ZXI6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtZm9vdGVyJyk7XG4gIGNvbnN0IGNoYXRXaW5kb3c6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtd2luZG93Jyk7XG5cbiAgaWYgKCFoZWFkZXIgfHwgIWNoYXRXaW5kb3cpIHJldHVybjtcblxuICBjb25zdCBoZWFkZXJCb3R0b206IG51bWJlciA9IGhlYWRlci5vZmZzZXRUb3AgKyBoZWFkZXIub2Zmc2V0SGVpZ2h0O1xuICBjb25zdCBjaGF0V2luZG93VG9wOiBudW1iZXIgPSBjaGF0V2luZG93Lm9mZnNldFRvcDtcbiAgY29uc3QgZml4ZWRNaW5EaXN0YW5jZTogbnVtYmVyID0gMjIwO1xuICBjb25zdCBtYXhDaGF0V2luZG93SGVpZ2h0OiBudW1iZXIgPSA2NTA7XG4gIGNvbnN0IGF2YWlsYWJsZVNwYWNlOiBudW1iZXIgPSBjaGF0V2luZG93VG9wIC0gaGVhZGVyQm90dG9tO1xuXG4gIGlmIChhdmFpbGFibGVTcGFjZSA8IGZpeGVkTWluRGlzdGFuY2UpIHtcbiAgICBjaGF0V2luZG93LnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMHZoIC0gJHtmaXhlZE1pbkRpc3RhbmNlfXB4KWA7XG4gIH1cbiAgaWYgKGNoYXRXaW5kb3cub2Zmc2V0SGVpZ2h0ID4gbWF4Q2hhdFdpbmRvd0hlaWdodCkge1xuICAgIGNoYXRXaW5kb3cuc3R5bGUuaGVpZ2h0ID0gYCR7bWF4Q2hhdFdpbmRvd0hlaWdodH1weGA7XG4gIH1cblxuICBpZiAoY2hhdE1haW4gJiYgY2hhdEZvb3Rlcikge1xuICAgIGNoYXRNYWluLnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMCUgLSAke2NoYXRGb290ZXIub2Zmc2V0SGVpZ2h0fXB4KWA7XG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNjcm9sbERvd24oZWxlbWVudDogSFRNTERpdkVsZW1lbnQpIHtcbiAgZWxlbWVudC5zY3JvbGxUbyh7XG4gICAgdG9wOiBlbGVtZW50LnNjcm9sbEhlaWdodCxcbiAgfSk7XG59XG5cbmNvbnN0IHNjcm9sbEFuaW1hdGlvbkR1cmF0aW9uID0gMjAwO1xuZXhwb3J0IGZ1bmN0aW9uIHNjcm9sbERvd25TbW9vdGgoZWxlbWVudDogSFRNTERpdkVsZW1lbnQpIHtcbiAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgZWxlbWVudC5zY3JvbGxUbyh7XG4gICAgICB0b3A6IGVsZW1lbnQuc2Nyb2xsSGVpZ2h0LFxuICAgICAgYmVoYXZpb3I6ICdzbW9vdGgnLFxuICAgIH0pO1xuICB9LCBzY3JvbGxBbmltYXRpb25EdXJhdGlvbik7XG59IiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXShtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsImltcG9ydCB7aGFuZGxlSGlkZUVsZW1lbnRzfSBmcm9tICcuL3V0aWxzJztcblxuY29uc29sZS5sb2coJ2ZpbGUgYWRtaW4udHMgbG9hZGVkJyk7XG5jb25zb2xlLmxvZygnYWRtaW4udHMgbG9hZGVkIDUgcm93Jyk7XG5cbmNvbnN0IGRhdGVzQnV0dG9uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNldmVudC1kYXRlcycpO1xuY29uc3QgZGF0ZXNEcm9wZG93bjogSFRNTFNlbGVjdEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAnI2V2ZW50LWRhdGVzLWRyb3Bkb3duJyxcbik7XG5cbmRhdGVzQnV0dG9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICBjb25zdCBkYXRlUGlja2VycyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5kYXRlcGlja2VyJyk7XG4gIGNvbnN0IGRhdGVQaWNrZXJBcnJheTogSFRNTEVsZW1lbnRbXSA9IEFycmF5LmZyb20oXG4gICAgZGF0ZVBpY2tlcnMsXG4gICkgYXMgSFRNTEVsZW1lbnRbXTtcblxuICBoYW5kbGVIaWRlRWxlbWVudHMoZGF0ZXNEcm9wZG93biwgZGF0ZVBpY2tlckFycmF5KTtcbn0pO1xuXG5jb25zdCBzZWFyY2hJbnB1dDogSFRNTElucHV0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICcjdGFibGUtc2VhcmNoLWV2ZW50cycsXG4pO1xuY29uc3Qgc2VhcmNoSW5wdXRCdXR0b24gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjdGFibGUtc2VhcmNoLWV2ZW50cy1idXR0b24nKTtcbmlmIChzZWFyY2hJbnB1dEJ1dHRvbiAmJiBzZWFyY2hJbnB1dCkge1xuICBzZWFyY2hJbnB1dEJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICBzZWFyY2hJbnB1dC52YWx1ZSA9ICcnO1xuICAgIHNlYXJjaElucHV0LmNsaWNrKCk7XG4gIH0pO1xufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9