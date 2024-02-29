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
    // const screenWith: number = window.innerWidth;
    // if (screenWith < 640) {
    //   return;
    // }
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
    buttonFilterDate.addEventListener('click', function () {
        var datePickers = document.querySelectorAll('.datepicker');
        var datePickerArray = Array.from(datePickers);
        (0, utils_1.handleHideElements)(dropdownFilterDate, datePickerArray);
    });
    buttonDateApply.addEventListener('click', function () {
        dropdownFilterDate.classList.toggle('hidden');
    });
    buttonCategories.addEventListener('click', function () {
        (0, utils_1.handleHideElements)(dropdownFilterCategories);
    });
    var dropDownLocationInput = document.querySelector('#dropdown-location-input');
    buttonLocation.addEventListener('click', function () {
        dropDownLocationInput.focus();
        (0, utils_1.handleHideElements)(dropdownFilterLocation);
    });
    buttonLocationNames.forEach(function (button) {
        button.addEventListener('click', function () {
            statusFilterLocation.innerHTML = button.innerHTML;
            (0, utils_1.handleHideElements)(dropdownFilterLocation);
        });
    });
    dropDownLocationInput.addEventListener('keyup', function () {
        filterDropdownLocation(buttonLocationNames, dropDownLocationInput);
    });
});

})();

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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T0FBTyxFQUFFO1FBQ3pDLDhCQUFrQixFQUFDLHdCQUF3QixDQUFDLENBQUM7SUFDL0MsQ0FBQyxDQUFDLENBQUM7SUFFSCxJQUFNLHFCQUFxQixHQUFxQixRQUFRLENBQUMsYUFBYSxDQUNwRSwwQkFBMEIsQ0FDM0IsQ0FBQztJQUVGLGNBQWMsQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7UUFDdkMscUJBQXFCLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDOUIsOEJBQWtCLEVBQUMsc0JBQXNCLENBQUMsQ0FBQztJQUM3QyxDQUFDLENBQUMsQ0FBQztJQUVILG1CQUFtQixDQUFDLE9BQU8sQ0FBQyxVQUFDLE1BQXNCO1FBQ2pELE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7WUFDL0Isb0JBQW9CLENBQUMsU0FBUyxHQUFHLE1BQU0sQ0FBQyxTQUFTLENBQUM7WUFDbEQsOEJBQWtCLEVBQUMsc0JBQXNCLENBQUMsQ0FBQztRQUM3QyxDQUFDLENBQUMsQ0FBQztJQUNMLENBQUMsQ0FBQyxDQUFDO0lBQ0gscUJBQXFCLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1FBQzlDLHNCQUFzQixDQUFDLG1CQUFtQixFQUFFLHFCQUFxQixDQUFDLENBQUM7SUFDckUsQ0FBQyxDQUFDLENBQUM7QUFDTCxDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy91dGlscy50cyIsIndlYnBhY2s6Ly9zdGF0aWMvd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL2V2ZW50LnRzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQ6IEhUTUxFbGVtZW50KSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG59XG5cbmZ1bmN0aW9uIGhpZGVFbGVtZW50cyhcbiAgZXZlbnQ6IE1vdXNlRXZlbnQsXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ/OiBIVE1MRWxlbWVudFtdLFxuKSB7XG4gIGlmIChcbiAgICAhZWxlbWVudC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkgJiZcbiAgICAhb3RoZXJFbGVtZW50LnNvbWUoZWwgPT4gZWwuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpKVxuICApIHtcbiAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gaGFuZGxlSGlkZUVsZW1lbnRzKFxuICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgb3RoZXJFbGVtZW50OiBIVE1MRWxlbWVudFtdID0gW10sXG4pIHtcbiAgZWxlbWVudC5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ21vdXNldXAnLCAoZXZlbnQ6IE1vdXNlRXZlbnQpID0+IHtcbiAgICBoaWRlRWxlbWVudHMoZXZlbnQsIGVsZW1lbnQsIG90aGVyRWxlbWVudCk7XG4gIH0pO1xuXG4gIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICBpZiAoZXZlbnQua2V5ID09PSAnRXNjYXBlJykge1xuICAgICAgYWRkSGlkZGVuQ2xhc3MoZWxlbWVudCk7XG4gICAgfVxuICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHJlc2l6ZUNoYXQoKSB7XG4gIGNvbnN0IGhlYWRlcjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcuaGVhZGVyJyk7XG4gIGNvbnN0IGNoYXRNYWluOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWJvZHknKTtcbiAgY29uc3QgY2hhdEZvb3RlcjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC1mb290ZXInKTtcbiAgY29uc3QgY2hhdFdpbmRvdzogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC13aW5kb3cnKTtcbiAgLy8gY29uc3Qgc2NyZWVuV2l0aDogbnVtYmVyID0gd2luZG93LmlubmVyV2lkdGg7XG5cbiAgLy8gaWYgKHNjcmVlbldpdGggPCA2NDApIHtcbiAgLy8gICByZXR1cm47XG4gIC8vIH1cblxuICBpZiAoIWhlYWRlciB8fCAhY2hhdFdpbmRvdykgcmV0dXJuO1xuXG4gIGNvbnN0IGhlYWRlckJvdHRvbTogbnVtYmVyID0gaGVhZGVyLm9mZnNldFRvcCArIGhlYWRlci5vZmZzZXRIZWlnaHQ7XG4gIGNvbnN0IGNoYXRXaW5kb3dUb3A6IG51bWJlciA9IGNoYXRXaW5kb3cub2Zmc2V0VG9wO1xuICBjb25zdCBmaXhlZE1pbkRpc3RhbmNlOiBudW1iZXIgPSAyMjA7XG4gIGNvbnN0IG1heENoYXRXaW5kb3dIZWlnaHQ6IG51bWJlciA9IDY1MDtcbiAgY29uc3QgYXZhaWxhYmxlU3BhY2U6IG51bWJlciA9IGNoYXRXaW5kb3dUb3AgLSBoZWFkZXJCb3R0b207XG5cbiAgaWYgKGF2YWlsYWJsZVNwYWNlIDwgZml4ZWRNaW5EaXN0YW5jZSkge1xuICAgIGNoYXRXaW5kb3cuc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwdmggLSAke2ZpeGVkTWluRGlzdGFuY2V9cHgpYDtcbiAgfVxuICBpZiAoY2hhdFdpbmRvdy5vZmZzZXRIZWlnaHQgPiBtYXhDaGF0V2luZG93SGVpZ2h0KSB7XG4gICAgY2hhdFdpbmRvdy5zdHlsZS5oZWlnaHQgPSBgJHttYXhDaGF0V2luZG93SGVpZ2h0fXB4YDtcbiAgfVxuXG4gIGlmIChjaGF0TWFpbiAmJiBjaGF0Rm9vdGVyKSB7XG4gICAgY2hhdE1haW4uc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwJSAtICR7Y2hhdEZvb3Rlci5vZmZzZXRIZWlnaHR9cHgpYDtcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2Nyb2xsRG93bihlbGVtZW50OiBIVE1MRGl2RWxlbWVudCkge1xuICBlbGVtZW50LnNjcm9sbFRvKHtcbiAgICB0b3A6IGVsZW1lbnQuc2Nyb2xsSGVpZ2h0LFxuICB9KTtcbn1cblxuY29uc3Qgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24gPSAyMDA7XG5leHBvcnQgZnVuY3Rpb24gc2Nyb2xsRG93blNtb290aChlbGVtZW50OiBIVE1MRGl2RWxlbWVudCkge1xuICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICBlbGVtZW50LnNjcm9sbFRvKHtcbiAgICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gICAgICBiZWhhdmlvcjogJ3Ntb290aCcsXG4gICAgfSk7XG4gIH0sIHNjcm9sbEFuaW1hdGlvbkR1cmF0aW9uKTtcbn1cbiIsIi8vIFRoZSBtb2R1bGUgY2FjaGVcbnZhciBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX18gPSB7fTtcblxuLy8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbmZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG5cdHZhciBjYWNoZWRNb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdO1xuXHRpZiAoY2FjaGVkTW9kdWxlICE9PSB1bmRlZmluZWQpIHtcblx0XHRyZXR1cm4gY2FjaGVkTW9kdWxlLmV4cG9ydHM7XG5cdH1cblx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcblx0dmFyIG1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF0gPSB7XG5cdFx0Ly8gbm8gbW9kdWxlLmlkIG5lZWRlZFxuXHRcdC8vIG5vIG1vZHVsZS5sb2FkZWQgbmVlZGVkXG5cdFx0ZXhwb3J0czoge31cblx0fTtcblxuXHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cblx0X193ZWJwYWNrX21vZHVsZXNfX1ttb2R1bGVJZF0obW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cblx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcblx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xufVxuXG4iLCJpbXBvcnQge2hhbmRsZUhpZGVFbGVtZW50c30gZnJvbSAnLi91dGlscyc7XG5cbmZ1bmN0aW9uIGZpbHRlckRyb3Bkb3duTG9jYXRpb24oXG4gIGRyb3Bkb3duTGlzdDogTm9kZUxpc3RPZjxIVE1MRGl2RWxlbWVudD4sXG4gIGRyb3Bkb3duSW5wdXQ6IEhUTUxJbnB1dEVsZW1lbnQsXG4pIHtcbiAgY29uc3QgZmlsdGVyID0gZHJvcGRvd25JbnB1dC52YWx1ZS50b1VwcGVyQ2FzZSgpO1xuXG4gIGZvciAobGV0IGkgPSAwOyBpIDwgZHJvcGRvd25MaXN0Lmxlbmd0aDsgaSsrKSB7XG4gICAgY29uc3QgdHh0VmFsdWUgPSBkcm9wZG93bkxpc3RbaV0udGV4dENvbnRlbnQgfHwgZHJvcGRvd25MaXN0W2ldLmlubmVyVGV4dDtcbiAgICBpZiAodHh0VmFsdWUudG9VcHBlckNhc2UoKS5pbmRleE9mKGZpbHRlcikgPiAtMSkge1xuICAgICAgZHJvcGRvd25MaXN0W2ldLnN0eWxlLmRpc3BsYXkgPSAnJztcbiAgICB9IGVsc2Uge1xuICAgICAgZHJvcGRvd25MaXN0W2ldLnN0eWxlLmRpc3BsYXkgPSAnbm9uZSc7XG4gICAgfVxuICB9XG59XG5cbmRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCBmdW5jdGlvbiAoKSB7XG4gIGNvbnN0IGJ1dHRvbkZpbHRlckRhdGUgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjZXZlbnRzLWZpbHRlci1kYXRlLWJ1dHRvbicpO1xuICBjb25zdCBidXR0b25Mb2NhdGlvbjogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1sb2NhdGlvbi1idXR0b24nLFxuICApO1xuICBjb25zdCBidXR0b25Mb2NhdGlvbk5hbWVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgICAnLmRyb3Bkb3duLWxvY2F0aW9uLW5hbWUtYnV0dG9uJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxEaXZFbGVtZW50PjtcblxuICBjb25zdCBidXR0b25DYXRlZ29yaWVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItY2F0ZWdvcmllcy1idXR0b24nLFxuICApO1xuICBjb25zdCBidXR0b25EYXRlQXBwbHkgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1kYXRlLWFwcGx5LWJ1dHRvbicsXG4gICk7XG5cbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJEYXRlOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWRhdGUtZHJvcGRvd24nLFxuICApO1xuICBjb25zdCBkcm9wZG93bkZpbHRlckxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9XG4gICAgZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2Ryb3Bkb3duLWxvY2F0aW9uJyk7XG4gIGNvbnN0IGRyb3Bkb3duRmlsdGVyQ2F0ZWdvcmllczogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1jYXRlZ29yaWVzLWRyb3Bkb3duJyxcbiAgKTtcblxuICBjb25zdCBzdGF0dXNGaWx0ZXJMb2NhdGlvbiA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLXN0YXR1cycsXG4gICk7XG5cbiAgYnV0dG9uRmlsdGVyRGF0ZS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICBjb25zdCBkYXRlUGlja2VycyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5kYXRlcGlja2VyJyk7XG4gICAgY29uc3QgZGF0ZVBpY2tlckFycmF5OiBIVE1MRWxlbWVudFtdID0gQXJyYXkuZnJvbShcbiAgICAgIGRhdGVQaWNrZXJzLFxuICAgICkgYXMgSFRNTEVsZW1lbnRbXTtcblxuICAgIGhhbmRsZUhpZGVFbGVtZW50cyhkcm9wZG93bkZpbHRlckRhdGUsIGRhdGVQaWNrZXJBcnJheSk7XG4gIH0pO1xuXG4gIGJ1dHRvbkRhdGVBcHBseS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICBkcm9wZG93bkZpbHRlckRhdGUuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gIH0pO1xuXG4gIGJ1dHRvbkNhdGVnb3JpZXMuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyQ2F0ZWdvcmllcyk7XG4gIH0pO1xuXG4gIGNvbnN0IGRyb3BEb3duTG9jYXRpb25JbnB1dDogSFRNTElucHV0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNkcm9wZG93bi1sb2NhdGlvbi1pbnB1dCcsXG4gICk7XG5cbiAgYnV0dG9uTG9jYXRpb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgZHJvcERvd25Mb2NhdGlvbklucHV0LmZvY3VzKCk7XG4gICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyTG9jYXRpb24pO1xuICB9KTtcblxuICBidXR0b25Mb2NhdGlvbk5hbWVzLmZvckVhY2goKGJ1dHRvbjogSFRNTERpdkVsZW1lbnQpID0+IHtcbiAgICBidXR0b24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBzdGF0dXNGaWx0ZXJMb2NhdGlvbi5pbm5lckhUTUwgPSBidXR0b24uaW5uZXJIVE1MO1xuICAgICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyTG9jYXRpb24pO1xuICAgIH0pO1xuICB9KTtcbiAgZHJvcERvd25Mb2NhdGlvbklucHV0LmFkZEV2ZW50TGlzdGVuZXIoJ2tleXVwJywgKCkgPT4ge1xuICAgIGZpbHRlckRyb3Bkb3duTG9jYXRpb24oYnV0dG9uTG9jYXRpb25OYW1lcywgZHJvcERvd25Mb2NhdGlvbklucHV0KTtcbiAgfSk7XG59KTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==