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
    var screenWith = window.innerWidth;
    var headerBottom = header.offsetTop + header.offsetHeight;
    var chatWindowTop = chatWindow.offsetTop;
    var fixedMinDistance = 220;
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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L2Jvb3RzdHJhcCIsIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvZXZlbnQudHMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gYWRkSGlkZGVuQ2xhc3MoZWxlbWVudDogSFRNTEVsZW1lbnQpIHtcbiAgZWxlbWVudC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbn1cblxuZnVuY3Rpb24gaGlkZUVsZW1lbnRzKFxuICBldmVudDogTW91c2VFdmVudCxcbiAgZWxlbWVudDogSFRNTEVsZW1lbnQsXG4gIG90aGVyRWxlbWVudD86IEhUTUxFbGVtZW50W10sXG4pIHtcbiAgaWYgKFxuICAgICFlbGVtZW50LmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSAmJlxuICAgICFvdGhlckVsZW1lbnQuc29tZShlbCA9PiBlbC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkpXG4gICkge1xuICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBoYW5kbGVIaWRlRWxlbWVudHMoXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ6IEhUTUxFbGVtZW50W10gPSBbXSxcbikge1xuICBlbGVtZW50LmNsYXNzTGlzdC50b2dnbGUoJ2hpZGRlbicpO1xuICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsIChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICAgIGhpZGVFbGVtZW50cyhldmVudCwgZWxlbWVudCwgb3RoZXJFbGVtZW50KTtcbiAgfSk7XG5cbiAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIGZ1bmN0aW9uIChldmVudCkge1xuICAgIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgICB9XG4gIH0pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVzaXplQ2hhdCgpIHtcbiAgY29uc3QgaGVhZGVyOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5oZWFkZXInKTtcbiAgY29uc3QgY2hhdE1haW46IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtYm9keScpO1xuICBjb25zdCBjaGF0Rm9vdGVyOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWZvb3RlcicpO1xuICBjb25zdCBjaGF0V2luZG93OiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LXdpbmRvdycpO1xuICBjb25zdCBzY3JlZW5XaXRoOiBudW1iZXIgPSB3aW5kb3cuaW5uZXJXaWR0aDtcbiAgY29uc3QgaGVhZGVyQm90dG9tOiBudW1iZXIgPSBoZWFkZXIub2Zmc2V0VG9wICsgaGVhZGVyLm9mZnNldEhlaWdodDtcbiAgY29uc3QgY2hhdFdpbmRvd1RvcDogbnVtYmVyID0gY2hhdFdpbmRvdy5vZmZzZXRUb3A7XG4gIGNvbnN0IGZpeGVkTWluRGlzdGFuY2U6IG51bWJlciA9IDIyMDtcbiAgY29uc3QgbWF4Q2hhdFdpbmRvd0hlaWdodDogbnVtYmVyID0gNjUwO1xuICBjb25zdCBhdmFpbGFibGVTcGFjZTogbnVtYmVyID0gY2hhdFdpbmRvd1RvcCAtIGhlYWRlckJvdHRvbTtcblxuICBpZiAoc2NyZWVuV2l0aCA8IDY0MCkge1xuICAgIGNoYXRNYWluLnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMCUgLSAke2NoYXRGb290ZXIub2Zmc2V0SGVpZ2h0fXB4KWA7XG4gICAgcmV0dXJuO1xuICB9XG5cbiAgaWYgKCFoZWFkZXIgfHwgIWNoYXRXaW5kb3cpIHJldHVybjtcblxuICBpZiAoYXZhaWxhYmxlU3BhY2UgPCBmaXhlZE1pbkRpc3RhbmNlKSB7XG4gICAgY2hhdFdpbmRvdy5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDB2aCAtICR7Zml4ZWRNaW5EaXN0YW5jZX1weClgO1xuICB9XG4gIGlmIChjaGF0V2luZG93Lm9mZnNldEhlaWdodCA+IG1heENoYXRXaW5kb3dIZWlnaHQpIHtcbiAgICBjaGF0V2luZG93LnN0eWxlLmhlaWdodCA9IGAke21heENoYXRXaW5kb3dIZWlnaHR9cHhgO1xuICB9XG5cbiAgaWYgKGNoYXRNYWluICYmIGNoYXRGb290ZXIpIHtcbiAgICBjaGF0TWFpbi5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDAlIC0gJHtjaGF0Rm9vdGVyLm9mZnNldEhlaWdodH1weClgO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gIH0pO1xufVxuXG5jb25zdCBzY3JvbGxBbmltYXRpb25EdXJhdGlvbiA9IDIwMDtcbmV4cG9ydCBmdW5jdGlvbiBzY3JvbGxEb3duU21vb3RoKGVsZW1lbnQ6IEhUTUxEaXZFbGVtZW50KSB7XG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGVsZW1lbnQuc2Nyb2xsVG8oe1xuICAgICAgdG9wOiBlbGVtZW50LnNjcm9sbEhlaWdodCxcbiAgICAgIGJlaGF2aW9yOiAnc21vb3RoJyxcbiAgICB9KTtcbiAgfSwgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24pO1xufVxuIiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXShtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsImltcG9ydCB7aGFuZGxlSGlkZUVsZW1lbnRzfSBmcm9tICcuL3V0aWxzJztcblxuZnVuY3Rpb24gZmlsdGVyRHJvcGRvd25Mb2NhdGlvbihcbiAgZHJvcGRvd25MaXN0OiBOb2RlTGlzdE9mPEhUTUxEaXZFbGVtZW50PixcbiAgZHJvcGRvd25JbnB1dDogSFRNTElucHV0RWxlbWVudCxcbikge1xuICBjb25zdCBmaWx0ZXIgPSBkcm9wZG93bklucHV0LnZhbHVlLnRvVXBwZXJDYXNlKCk7XG5cbiAgZm9yIChsZXQgaSA9IDA7IGkgPCBkcm9wZG93bkxpc3QubGVuZ3RoOyBpKyspIHtcbiAgICBjb25zdCB0eHRWYWx1ZSA9IGRyb3Bkb3duTGlzdFtpXS50ZXh0Q29udGVudCB8fCBkcm9wZG93bkxpc3RbaV0uaW5uZXJUZXh0O1xuICAgIGlmICh0eHRWYWx1ZS50b1VwcGVyQ2FzZSgpLmluZGV4T2YoZmlsdGVyKSA+IC0xKSB7XG4gICAgICBkcm9wZG93bkxpc3RbaV0uc3R5bGUuZGlzcGxheSA9ICcnO1xuICAgIH0gZWxzZSB7XG4gICAgICBkcm9wZG93bkxpc3RbaV0uc3R5bGUuZGlzcGxheSA9ICdub25lJztcbiAgICB9XG4gIH1cbn1cblxuZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsIGZ1bmN0aW9uICgpIHtcbiAgY29uc3QgYnV0dG9uRmlsdGVyRGF0ZSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNldmVudHMtZmlsdGVyLWRhdGUtYnV0dG9uJyk7XG4gIGNvbnN0IGJ1dHRvbkxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGJ1dHRvbkxvY2F0aW9uTmFtZXMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKFxuICAgICcuZHJvcGRvd24tbG9jYXRpb24tbmFtZS1idXR0b24nLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTERpdkVsZW1lbnQ+O1xuXG4gIGNvbnN0IGJ1dHRvbkNhdGVnb3JpZXMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1jYXRlZ29yaWVzLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGJ1dHRvbkRhdGVBcHBseSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWRhdGUtYXBwbHktYnV0dG9uJyxcbiAgKTtcblxuICBjb25zdCBkcm9wZG93bkZpbHRlckRhdGU6IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItZGF0ZS1kcm9wZG93bicsXG4gICk7XG4gIGNvbnN0IGRyb3Bkb3duRmlsdGVyTG9jYXRpb246IEhUTUxEaXZFbGVtZW50ID1cbiAgICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjZHJvcGRvd24tbG9jYXRpb24nKTtcbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWNhdGVnb3JpZXMtZHJvcGRvd24nLFxuICApO1xuXG4gIGNvbnN0IHN0YXR1c0ZpbHRlckxvY2F0aW9uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24tc3RhdHVzJyxcbiAgKTtcblxuICBpZiAoYnV0dG9uRmlsdGVyRGF0ZSkge1xuICAgIGJ1dHRvbkZpbHRlckRhdGUuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBkYXRlUGlja2VycyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5kYXRlcGlja2VyJyk7XG4gICAgICBjb25zdCBkYXRlUGlja2VyQXJyYXk6IEhUTUxFbGVtZW50W10gPSBBcnJheS5mcm9tKFxuICAgICAgICBkYXRlUGlja2VycyxcbiAgICAgICkgYXMgSFRNTEVsZW1lbnRbXTtcblxuICAgICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyRGF0ZSwgZGF0ZVBpY2tlckFycmF5KTtcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChidXR0b25EYXRlQXBwbHkpIHtcbiAgICBidXR0b25EYXRlQXBwbHkuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBkcm9wZG93bkZpbHRlckRhdGUuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gICAgfSk7XG4gIH1cblxuICBpZiAoYnV0dG9uQ2F0ZWdvcmllcykge1xuICAgIGJ1dHRvbkNhdGVnb3JpZXMuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBoYW5kbGVIaWRlRWxlbWVudHMoZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzKTtcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChzdGF0dXNGaWx0ZXJMb2NhdGlvbikge1xuICAgIGNvbnN0IGRyb3BEb3duTG9jYXRpb25JbnB1dDogSFRNTElucHV0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgICAnI2Ryb3Bkb3duLWxvY2F0aW9uLWlucHV0JyxcbiAgICApO1xuXG4gICAgaWYgKGJ1dHRvbkxvY2F0aW9uKSB7XG4gICAgICBidXR0b25Mb2NhdGlvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgICAgZHJvcERvd25Mb2NhdGlvbklucHV0LmZvY3VzKCk7XG4gICAgICAgIGhhbmRsZUhpZGVFbGVtZW50cyhkcm9wZG93bkZpbHRlckxvY2F0aW9uKTtcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGJ1dHRvbkxvY2F0aW9uTmFtZXMuZm9yRWFjaCgoYnV0dG9uOiBIVE1MRGl2RWxlbWVudCkgPT4ge1xuICAgICAgYnV0dG9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgICBzdGF0dXNGaWx0ZXJMb2NhdGlvbi5pbm5lckhUTUwgPSBidXR0b24uaW5uZXJIVE1MO1xuICAgICAgICBoYW5kbGVIaWRlRWxlbWVudHMoZHJvcGRvd25GaWx0ZXJMb2NhdGlvbik7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgICBkcm9wRG93bkxvY2F0aW9uSW5wdXQuYWRkRXZlbnRMaXN0ZW5lcigna2V5dXAnLCAoKSA9PiB7XG4gICAgICBmaWx0ZXJEcm9wZG93bkxvY2F0aW9uKGJ1dHRvbkxvY2F0aW9uTmFtZXMsIGRyb3BEb3duTG9jYXRpb25JbnB1dCk7XG4gICAgfSk7XG4gIH1cbn0pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9