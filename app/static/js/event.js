/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/utils.ts":
/*!**********************!*\
  !*** ./src/utils.ts ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.resizeChat = exports.handleHideElements = void 0;
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
}
exports.resizeChat = resizeChat;


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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvZXZlbnQuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7OztBQUFBLFNBQVMsY0FBYyxDQUFDLE9BQW9CO0lBQzFDLE9BQU8sQ0FBQyxTQUFTLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxDQUFDO0FBQ2xDLENBQUM7QUFFRCxTQUFTLFlBQVksQ0FDbkIsS0FBaUIsRUFDakIsT0FBb0IsRUFDcEIsWUFBNEI7SUFFNUIsSUFDRSxDQUFDLE9BQU8sQ0FBQyxRQUFRLENBQUMsS0FBSyxDQUFDLE1BQWMsQ0FBQztRQUN2QyxDQUFDLFlBQVksQ0FBQyxJQUFJLENBQUMsWUFBRSxJQUFJLFNBQUUsQ0FBQyxRQUFRLENBQUMsS0FBSyxDQUFDLE1BQWMsQ0FBQyxFQUFqQyxDQUFpQyxDQUFDLEVBQzNEO1FBQ0EsY0FBYyxDQUFDLE9BQU8sQ0FBQyxDQUFDO0tBQ3pCO0FBQ0gsQ0FBQztBQUVELFNBQWdCLGtCQUFrQixDQUNoQyxPQUFvQixFQUNwQixZQUFnQztJQUFoQyxnREFBZ0M7SUFFaEMsT0FBTyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUM7SUFDbkMsTUFBTSxDQUFDLGdCQUFnQixDQUFDLFNBQVMsRUFBRSxVQUFDLEtBQWlCO1FBQ25ELFlBQVksQ0FBQyxLQUFLLEVBQUUsT0FBTyxFQUFFLFlBQVksQ0FBQyxDQUFDO0lBQzdDLENBQUMsQ0FBQyxDQUFDO0lBRUgsUUFBUSxDQUFDLGdCQUFnQixDQUFDLFNBQVMsRUFBRSxVQUFVLEtBQUs7UUFDbEQsSUFBSSxLQUFLLENBQUMsR0FBRyxLQUFLLFFBQVEsRUFBRTtZQUMxQixjQUFjLENBQUMsT0FBTyxDQUFDLENBQUM7U0FDekI7SUFDSCxDQUFDLENBQUMsQ0FBQztBQUNMLENBQUM7QUFkRCxnREFjQztBQUVELFNBQWdCLFVBQVU7SUFDeEIsSUFBTSxNQUFNLEdBQWdCLFFBQVEsQ0FBQyxhQUFhLENBQUMsU0FBUyxDQUFDLENBQUM7SUFDOUQsSUFBTSxVQUFVLEdBQWdCLFFBQVEsQ0FBQyxhQUFhLENBQUMsY0FBYyxDQUFDLENBQUM7SUFFdkUsSUFBSSxDQUFDLE1BQU0sSUFBSSxDQUFDLFVBQVU7UUFBRSxPQUFPO0lBRW5DLElBQU0sWUFBWSxHQUFXLE1BQU0sQ0FBQyxTQUFTLEdBQUcsTUFBTSxDQUFDLFlBQVksQ0FBQztJQUNwRSxJQUFNLGFBQWEsR0FBVyxVQUFVLENBQUMsU0FBUyxDQUFDO0lBQ25ELElBQU0sZ0JBQWdCLEdBQVcsR0FBRyxDQUFDO0lBQ3JDLElBQU0sbUJBQW1CLEdBQVcsR0FBRyxDQUFDO0lBQ3hDLElBQU0sY0FBYyxHQUFXLGFBQWEsR0FBRyxZQUFZLENBQUM7SUFFNUQsSUFBSSxjQUFjLEdBQUcsZ0JBQWdCLEVBQUU7UUFDckMsVUFBVSxDQUFDLEtBQUssQ0FBQyxNQUFNLEdBQUcsdUJBQWdCLGdCQUFnQixRQUFLLENBQUM7S0FDakU7SUFDRCxJQUFJLFVBQVUsQ0FBQyxZQUFZLEdBQUcsbUJBQW1CLEVBQUU7UUFDakQsVUFBVSxDQUFDLEtBQUssQ0FBQyxNQUFNLEdBQUcsVUFBRyxtQkFBbUIsT0FBSSxDQUFDO0tBQ3REO0FBQ0gsQ0FBQztBQWxCRCxnQ0FrQkM7Ozs7Ozs7VUNuREQ7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTs7VUFFQTtVQUNBOztVQUVBO1VBQ0E7VUFDQTs7Ozs7Ozs7Ozs7O0FDdEJBLG1FQUEyQztBQUUzQyxTQUFTLHNCQUFzQixDQUM3QixZQUF3QyxFQUN4QyxhQUErQjtJQUUvQixJQUFNLE1BQU0sR0FBRyxhQUFhLENBQUMsS0FBSyxDQUFDLFdBQVcsRUFBRSxDQUFDO0lBRWpELEtBQUssSUFBSSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsR0FBRyxZQUFZLENBQUMsTUFBTSxFQUFFLENBQUMsRUFBRSxFQUFFO1FBQzVDLElBQU0sUUFBUSxHQUFHLFlBQVksQ0FBQyxDQUFDLENBQUMsQ0FBQyxXQUFXLElBQUksWUFBWSxDQUFDLENBQUMsQ0FBQyxDQUFDLFNBQVMsQ0FBQztRQUMxRSxJQUFJLFFBQVEsQ0FBQyxXQUFXLEVBQUUsQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLEdBQUcsQ0FBQyxDQUFDLEVBQUU7WUFDL0MsWUFBWSxDQUFDLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxPQUFPLEdBQUcsRUFBRSxDQUFDO1NBQ3BDO2FBQU07WUFDTCxZQUFZLENBQUMsQ0FBQyxDQUFDLENBQUMsS0FBSyxDQUFDLE9BQU8sR0FBRyxNQUFNLENBQUM7U0FDeEM7S0FDRjtBQUNILENBQUM7QUFFRCxRQUFRLENBQUMsZ0JBQWdCLENBQUMsa0JBQWtCLEVBQUU7SUFDNUMsSUFBTSxnQkFBZ0IsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLDRCQUE0QixDQUFDLENBQUM7SUFDOUUsSUFBTSxjQUFjLEdBQW1CLFFBQVEsQ0FBQyxhQUFhLENBQzNELGdDQUFnQyxDQUNqQyxDQUFDO0lBQ0YsSUFBTSxtQkFBbUIsR0FBRyxRQUFRLENBQUMsZ0JBQWdCLENBQ25ELGdDQUFnQyxDQUNILENBQUM7SUFFaEMsSUFBTSxnQkFBZ0IsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUM3QyxrQ0FBa0MsQ0FDbkMsQ0FBQztJQUNGLElBQU0sZUFBZSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQzVDLGtDQUFrQyxDQUNuQyxDQUFDO0lBRUYsSUFBTSxrQkFBa0IsR0FBbUIsUUFBUSxDQUFDLGFBQWEsQ0FDL0QsOEJBQThCLENBQy9CLENBQUM7SUFDRixJQUFNLHNCQUFzQixHQUMxQixRQUFRLENBQUMsYUFBYSxDQUFDLG9CQUFvQixDQUFDLENBQUM7SUFDL0MsSUFBTSx3QkFBd0IsR0FBbUIsUUFBUSxDQUFDLGFBQWEsQ0FDckUsb0NBQW9DLENBQ3JDLENBQUM7SUFFRixJQUFNLG9CQUFvQixHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQ2pELGdDQUFnQyxDQUNqQyxDQUFDO0lBRUYsZ0JBQWdCLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1FBQ3pDLElBQU0sV0FBVyxHQUFHLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxhQUFhLENBQUMsQ0FBQztRQUM3RCxJQUFNLGVBQWUsR0FBa0IsS0FBSyxDQUFDLElBQUksQ0FDL0MsV0FBVyxDQUNLLENBQUM7UUFFbkIsOEJBQWtCLEVBQUMsa0JBQWtCLEVBQUUsZUFBZSxDQUFDLENBQUM7SUFDMUQsQ0FBQyxDQUFDLENBQUM7SUFFSCxlQUFlLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1FBQ3hDLGtCQUFrQixDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUM7SUFDaEQsQ0FBQyxDQUFDLENBQUM7SUFFSCxnQkFBZ0IsQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7UUFDekMsOEJBQWtCLEVBQUMsd0JBQXdCLENBQUMsQ0FBQztJQUMvQyxDQUFDLENBQUMsQ0FBQztJQUVILElBQU0scUJBQXFCLEdBQXFCLFFBQVEsQ0FBQyxhQUFhLENBQ3BFLDBCQUEwQixDQUMzQixDQUFDO0lBRUYsY0FBYyxDQUFDLGdCQUFnQixDQUFDLE9BQU8sRUFBRTtRQUN2QyxxQkFBcUIsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUM5Qiw4QkFBa0IsRUFBQyxzQkFBc0IsQ0FBQyxDQUFDO0lBQzdDLENBQUMsQ0FBQyxDQUFDO0lBRUgsbUJBQW1CLENBQUMsT0FBTyxDQUFDLFVBQUMsTUFBc0I7UUFDakQsTUFBTSxDQUFDLGdCQUFnQixDQUFDLE9BQU8sRUFBRTtZQUMvQixvQkFBb0IsQ0FBQyxTQUFTLEdBQUcsTUFBTSxDQUFDLFNBQVMsQ0FBQztZQUNsRCw4QkFBa0IsRUFBQyxzQkFBc0IsQ0FBQyxDQUFDO1FBQzdDLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQyxDQUFDLENBQUM7SUFDSCxxQkFBcUIsQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7UUFDOUMsc0JBQXNCLENBQUMsbUJBQW1CLEVBQUUscUJBQXFCLENBQUMsQ0FBQztJQUNyRSxDQUFDLENBQUMsQ0FBQztBQUNMLENBQUMsQ0FBQyxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL3V0aWxzLnRzIiwid2VicGFjazovL3N0YXRpYy93ZWJwYWNrL2Jvb3RzdHJhcCIsIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvZXZlbnQudHMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gYWRkSGlkZGVuQ2xhc3MoZWxlbWVudDogSFRNTEVsZW1lbnQpIHtcbiAgZWxlbWVudC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbn1cblxuZnVuY3Rpb24gaGlkZUVsZW1lbnRzKFxuICBldmVudDogTW91c2VFdmVudCxcbiAgZWxlbWVudDogSFRNTEVsZW1lbnQsXG4gIG90aGVyRWxlbWVudD86IEhUTUxFbGVtZW50W10sXG4pIHtcbiAgaWYgKFxuICAgICFlbGVtZW50LmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSAmJlxuICAgICFvdGhlckVsZW1lbnQuc29tZShlbCA9PiBlbC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkpXG4gICkge1xuICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBoYW5kbGVIaWRlRWxlbWVudHMoXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ6IEhUTUxFbGVtZW50W10gPSBbXSxcbikge1xuICBlbGVtZW50LmNsYXNzTGlzdC50b2dnbGUoJ2hpZGRlbicpO1xuICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsIChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICAgIGhpZGVFbGVtZW50cyhldmVudCwgZWxlbWVudCwgb3RoZXJFbGVtZW50KTtcbiAgfSk7XG5cbiAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIGZ1bmN0aW9uIChldmVudCkge1xuICAgIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgICB9XG4gIH0pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVzaXplQ2hhdCgpIHtcbiAgY29uc3QgaGVhZGVyOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5oZWFkZXInKTtcbiAgY29uc3QgY2hhdFdpbmRvdzogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC13aW5kb3cnKTtcblxuICBpZiAoIWhlYWRlciB8fCAhY2hhdFdpbmRvdykgcmV0dXJuO1xuXG4gIGNvbnN0IGhlYWRlckJvdHRvbTogbnVtYmVyID0gaGVhZGVyLm9mZnNldFRvcCArIGhlYWRlci5vZmZzZXRIZWlnaHQ7XG4gIGNvbnN0IGNoYXRXaW5kb3dUb3A6IG51bWJlciA9IGNoYXRXaW5kb3cub2Zmc2V0VG9wO1xuICBjb25zdCBmaXhlZE1pbkRpc3RhbmNlOiBudW1iZXIgPSAyMjA7XG4gIGNvbnN0IG1heENoYXRXaW5kb3dIZWlnaHQ6IG51bWJlciA9IDY1MDtcbiAgY29uc3QgYXZhaWxhYmxlU3BhY2U6IG51bWJlciA9IGNoYXRXaW5kb3dUb3AgLSBoZWFkZXJCb3R0b207XG5cbiAgaWYgKGF2YWlsYWJsZVNwYWNlIDwgZml4ZWRNaW5EaXN0YW5jZSkge1xuICAgIGNoYXRXaW5kb3cuc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwdmggLSAke2ZpeGVkTWluRGlzdGFuY2V9cHgpYDtcbiAgfVxuICBpZiAoY2hhdFdpbmRvdy5vZmZzZXRIZWlnaHQgPiBtYXhDaGF0V2luZG93SGVpZ2h0KSB7XG4gICAgY2hhdFdpbmRvdy5zdHlsZS5oZWlnaHQgPSBgJHttYXhDaGF0V2luZG93SGVpZ2h0fXB4YDtcbiAgfVxufVxuIiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXShtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsImltcG9ydCB7aGFuZGxlSGlkZUVsZW1lbnRzfSBmcm9tICcuL3V0aWxzJztcblxuZnVuY3Rpb24gZmlsdGVyRHJvcGRvd25Mb2NhdGlvbihcbiAgZHJvcGRvd25MaXN0OiBOb2RlTGlzdE9mPEhUTUxEaXZFbGVtZW50PixcbiAgZHJvcGRvd25JbnB1dDogSFRNTElucHV0RWxlbWVudCxcbikge1xuICBjb25zdCBmaWx0ZXIgPSBkcm9wZG93bklucHV0LnZhbHVlLnRvVXBwZXJDYXNlKCk7XG5cbiAgZm9yIChsZXQgaSA9IDA7IGkgPCBkcm9wZG93bkxpc3QubGVuZ3RoOyBpKyspIHtcbiAgICBjb25zdCB0eHRWYWx1ZSA9IGRyb3Bkb3duTGlzdFtpXS50ZXh0Q29udGVudCB8fCBkcm9wZG93bkxpc3RbaV0uaW5uZXJUZXh0O1xuICAgIGlmICh0eHRWYWx1ZS50b1VwcGVyQ2FzZSgpLmluZGV4T2YoZmlsdGVyKSA+IC0xKSB7XG4gICAgICBkcm9wZG93bkxpc3RbaV0uc3R5bGUuZGlzcGxheSA9ICcnO1xuICAgIH0gZWxzZSB7XG4gICAgICBkcm9wZG93bkxpc3RbaV0uc3R5bGUuZGlzcGxheSA9ICdub25lJztcbiAgICB9XG4gIH1cbn1cblxuZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsIGZ1bmN0aW9uICgpIHtcbiAgY29uc3QgYnV0dG9uRmlsdGVyRGF0ZSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNldmVudHMtZmlsdGVyLWRhdGUtYnV0dG9uJyk7XG4gIGNvbnN0IGJ1dHRvbkxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGJ1dHRvbkxvY2F0aW9uTmFtZXMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKFxuICAgICcuZHJvcGRvd24tbG9jYXRpb24tbmFtZS1idXR0b24nLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTERpdkVsZW1lbnQ+O1xuXG4gIGNvbnN0IGJ1dHRvbkNhdGVnb3JpZXMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1jYXRlZ29yaWVzLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGJ1dHRvbkRhdGVBcHBseSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWRhdGUtYXBwbHktYnV0dG9uJyxcbiAgKTtcblxuICBjb25zdCBkcm9wZG93bkZpbHRlckRhdGU6IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItZGF0ZS1kcm9wZG93bicsXG4gICk7XG4gIGNvbnN0IGRyb3Bkb3duRmlsdGVyTG9jYXRpb246IEhUTUxEaXZFbGVtZW50ID1cbiAgICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjZHJvcGRvd24tbG9jYXRpb24nKTtcbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWNhdGVnb3JpZXMtZHJvcGRvd24nLFxuICApO1xuXG4gIGNvbnN0IHN0YXR1c0ZpbHRlckxvY2F0aW9uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24tc3RhdHVzJyxcbiAgKTtcblxuICBidXR0b25GaWx0ZXJEYXRlLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgIGNvbnN0IGRhdGVQaWNrZXJzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXInKTtcbiAgICBjb25zdCBkYXRlUGlja2VyQXJyYXk6IEhUTUxFbGVtZW50W10gPSBBcnJheS5mcm9tKFxuICAgICAgZGF0ZVBpY2tlcnMsXG4gICAgKSBhcyBIVE1MRWxlbWVudFtdO1xuXG4gICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyRGF0ZSwgZGF0ZVBpY2tlckFycmF5KTtcbiAgfSk7XG5cbiAgYnV0dG9uRGF0ZUFwcGx5LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgIGRyb3Bkb3duRmlsdGVyRGF0ZS5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgfSk7XG5cbiAgYnV0dG9uQ2F0ZWdvcmllcy5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICBoYW5kbGVIaWRlRWxlbWVudHMoZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzKTtcbiAgfSk7XG5cbiAgY29uc3QgZHJvcERvd25Mb2NhdGlvbklucHV0OiBIVE1MSW5wdXRFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2Ryb3Bkb3duLWxvY2F0aW9uLWlucHV0JyxcbiAgKTtcblxuICBidXR0b25Mb2NhdGlvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICBkcm9wRG93bkxvY2F0aW9uSW5wdXQuZm9jdXMoKTtcbiAgICBoYW5kbGVIaWRlRWxlbWVudHMoZHJvcGRvd25GaWx0ZXJMb2NhdGlvbik7XG4gIH0pO1xuXG4gIGJ1dHRvbkxvY2F0aW9uTmFtZXMuZm9yRWFjaCgoYnV0dG9uOiBIVE1MRGl2RWxlbWVudCkgPT4ge1xuICAgIGJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgIHN0YXR1c0ZpbHRlckxvY2F0aW9uLmlubmVySFRNTCA9IGJ1dHRvbi5pbm5lckhUTUw7XG4gICAgICBoYW5kbGVIaWRlRWxlbWVudHMoZHJvcGRvd25GaWx0ZXJMb2NhdGlvbik7XG4gICAgfSk7XG4gIH0pO1xuICBkcm9wRG93bkxvY2F0aW9uSW5wdXQuYWRkRXZlbnRMaXN0ZW5lcigna2V5dXAnLCAoKSA9PiB7XG4gICAgZmlsdGVyRHJvcGRvd25Mb2NhdGlvbihidXR0b25Mb2NhdGlvbk5hbWVzLCBkcm9wRG93bkxvY2F0aW9uSW5wdXQpO1xuICB9KTtcbn0pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9
