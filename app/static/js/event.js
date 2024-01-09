/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/utils.ts":
/*!**********************!*\
  !*** ./src/utils.ts ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.handleHideElements = void 0;
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
document.addEventListener('DOMContentLoaded', function () {
    var buttonFilterDate = document.querySelector('#events-filter-date-button');
    var buttonLocation = document.querySelector('#events-filter-location-button');
    var buttonCategories = document.querySelector('#events-filter-categories-button');
    var buttonDateApply = document.querySelector('#events-filter-date-apply-button');
    var dropdownFilterDate = document.querySelector('#events-filter-date-dropdown');
    var dropdownFilterLocation = document.querySelector('#events-filter-location-dropdown');
    var dropdownFilterCategories = document.querySelector('#events-filter-categories-dropdown');
    var statusFilterLocation = document.querySelector('#events-filter-location-status');
    var inputLocation = document.querySelector('#events-filter-location-input');
    var datalistLocation = document.querySelector('#events-filter-location-list');
    buttonFilterDate.addEventListener('click', function () {
        var datePickers = document.querySelectorAll('.datepicker');
        var datePickerArray = Array.from(datePickers);
        (0, utils_1.handleHideElements)(dropdownFilterDate, datePickerArray);
    });
    buttonDateApply.addEventListener('click', function () {
        dropdownFilterDate.classList.toggle('hidden');
    });
    buttonLocation.addEventListener('click', function () {
        (0, utils_1.handleHideElements)(dropdownFilterLocation);
        inputLocation.focus();
    });
    buttonCategories.addEventListener('click', function () {
        (0, utils_1.handleHideElements)(dropdownFilterCategories);
    });
    inputLocation.onfocus = function () {
        datalistLocation.style.display = 'block';
        inputLocation.style.borderRadius = '5px 5px 0 0';
    };
    var _loop_1 = function (index) {
        var option = datalistLocation.options[index];
        option.onclick = function () {
            inputLocation.value = option.value;
            statusFilterLocation.innerHTML = option.value;
            datalistLocation.style.display = 'none';
            inputLocation.style.borderRadius = '5px';
        };
    };
    for (var index in datalistLocation.options) {
        _loop_1(index);
    }
    inputLocation.oninput = function () {
        currentFocus = -1;
        var text = inputLocation.value.toUpperCase();
        for (var index in datalistLocation.options) {
            var option = datalistLocation.options[index];
            option.value.toUpperCase().indexOf(text) > -1
                ? (option.style.display = 'block')
                : (option.style.display = 'none');
        }
    };
    var currentFocus = -1;
    inputLocation.onkeydown = function (e) {
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(datalistLocation.options);
        }
        else if (e.keyCode == 38) {
            currentFocus--;
            addActive(datalistLocation.options);
        }
        else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (datalistLocation.options) {
                    datalistLocation.options[currentFocus].click();
                }
            }
        }
    };
    function addActive(x) {
        if (!x)
            return;
        false;
        removeActive(x);
        if (currentFocus >= x.length)
            currentFocus = 0;
        if (currentFocus < 0)
            currentFocus = x.length - 1;
        x[currentFocus].classList.add('active');
    }
    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove('active');
        }
    }
});

})();

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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UyxTQUFTLENBQUMsQ0FBc0M7UUFDdkQsSUFBSSxDQUFDLENBQUM7WUFBRSxPQUFPO1FBRWYsS0FBSyxDQUFDO1FBQ04sWUFBWSxDQUFDLENBQUMsQ0FBQyxDQUFDO1FBQ2hCLElBQUksWUFBWSxJQUFJLENBQUMsQ0FBQyxNQUFNO1lBQUUsWUFBWSxHQUFHLENBQUMsQ0FBQztRQUMvQyxJQUFJLFlBQVksR0FBRyxDQUFDO1lBQUUsWUFBWSxHQUFHLENBQUMsQ0FBQyxNQUFNLEdBQUcsQ0FBQyxDQUFDO1FBQ2xELENBQUMsQ0FBQyxZQUFZLENBQUMsQ0FBQyxTQUFTLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxDQUFDO0lBQzFDLENBQUM7SUFFRCxTQUFTLFlBQVksQ0FBQyxDQUFzQztRQUMxRCxLQUFLLElBQUksQ0FBQyxHQUFHLENBQUMsRUFBRSxDQUFDLEdBQUcsQ0FBQyxDQUFDLE1BQU0sRUFBRSxDQUFDLEVBQUUsRUFBRTtZQUNqQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsU0FBUyxDQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsQ0FBQztTQUNqQztJQUNILENBQUM7QUFDSCxDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy91dGlscy50cyIsIndlYnBhY2s6Ly9zdGF0aWMvd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL2V2ZW50LnRzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQ6IEhUTUxFbGVtZW50KSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG59XG5cbmZ1bmN0aW9uIGhpZGVFbGVtZW50cyhcbiAgZXZlbnQ6IE1vdXNlRXZlbnQsXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ/OiBIVE1MRWxlbWVudFtdLFxuKSB7XG4gIGlmIChcbiAgICAhZWxlbWVudC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkgJiZcbiAgICAhb3RoZXJFbGVtZW50LnNvbWUoZWwgPT4gZWwuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpKVxuICApIHtcbiAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gaGFuZGxlSGlkZUVsZW1lbnRzKFxuICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgb3RoZXJFbGVtZW50OiBIVE1MRWxlbWVudFtdID0gW10sXG4pIHtcbiAgZWxlbWVudC5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ21vdXNldXAnLCAoZXZlbnQ6IE1vdXNlRXZlbnQpID0+IHtcbiAgICBoaWRlRWxlbWVudHMoZXZlbnQsIGVsZW1lbnQsIG90aGVyRWxlbWVudCk7XG4gIH0pO1xuXG4gIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICBpZiAoZXZlbnQua2V5ID09PSAnRXNjYXBlJykge1xuICAgICAgYWRkSGlkZGVuQ2xhc3MoZWxlbWVudCk7XG4gICAgfVxuICB9KTtcbn1cbiIsIi8vIFRoZSBtb2R1bGUgY2FjaGVcbnZhciBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX18gPSB7fTtcblxuLy8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbmZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG5cdHZhciBjYWNoZWRNb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdO1xuXHRpZiAoY2FjaGVkTW9kdWxlICE9PSB1bmRlZmluZWQpIHtcblx0XHRyZXR1cm4gY2FjaGVkTW9kdWxlLmV4cG9ydHM7XG5cdH1cblx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcblx0dmFyIG1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF0gPSB7XG5cdFx0Ly8gbm8gbW9kdWxlLmlkIG5lZWRlZFxuXHRcdC8vIG5vIG1vZHVsZS5sb2FkZWQgbmVlZGVkXG5cdFx0ZXhwb3J0czoge31cblx0fTtcblxuXHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cblx0X193ZWJwYWNrX21vZHVsZXNfX1ttb2R1bGVJZF0obW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cblx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcblx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xufVxuXG4iLCJpbXBvcnQge2hhbmRsZUhpZGVFbGVtZW50c30gZnJvbSAnLi91dGlscyc7XG5cbmRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCBmdW5jdGlvbiAoKSB7XG4gIGNvbnN0IGJ1dHRvbkZpbHRlckRhdGUgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjZXZlbnRzLWZpbHRlci1kYXRlLWJ1dHRvbicpO1xuICBjb25zdCBidXR0b25Mb2NhdGlvbjogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1sb2NhdGlvbi1idXR0b24nLFxuICApO1xuICBjb25zdCBidXR0b25DYXRlZ29yaWVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItY2F0ZWdvcmllcy1idXR0b24nLFxuICApO1xuICBjb25zdCBidXR0b25EYXRlQXBwbHkgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1kYXRlLWFwcGx5LWJ1dHRvbicsXG4gICk7XG5cbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJEYXRlOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWRhdGUtZHJvcGRvd24nLFxuICApO1xuICBjb25zdCBkcm9wZG93bkZpbHRlckxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWRyb3Bkb3duJyxcbiAgKTtcbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWNhdGVnb3JpZXMtZHJvcGRvd24nLFxuICApO1xuXG4gIGNvbnN0IHN0YXR1c0ZpbHRlckxvY2F0aW9uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24tc3RhdHVzJyxcbiAgKTtcbiAgY29uc3QgaW5wdXRMb2NhdGlvbjogSFRNTElucHV0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWlucHV0JyxcbiAgKTtcbiAgY29uc3QgZGF0YWxpc3RMb2NhdGlvbjogSFRNTERhdGFMaXN0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWxpc3QnLFxuICApIGFzIEhUTUxEYXRhTGlzdEVsZW1lbnQ7XG5cbiAgYnV0dG9uRmlsdGVyRGF0ZS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICBjb25zdCBkYXRlUGlja2VycyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5kYXRlcGlja2VyJyk7XG4gICAgY29uc3QgZGF0ZVBpY2tlckFycmF5OiBIVE1MRWxlbWVudFtdID0gQXJyYXkuZnJvbShcbiAgICAgIGRhdGVQaWNrZXJzLFxuICAgICkgYXMgSFRNTEVsZW1lbnRbXTtcblxuICAgIGhhbmRsZUhpZGVFbGVtZW50cyhkcm9wZG93bkZpbHRlckRhdGUsIGRhdGVQaWNrZXJBcnJheSk7XG4gIH0pO1xuXG4gIGJ1dHRvbkRhdGVBcHBseS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICBkcm9wZG93bkZpbHRlckRhdGUuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gIH0pO1xuXG4gIGJ1dHRvbkxvY2F0aW9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgIGhhbmRsZUhpZGVFbGVtZW50cyhkcm9wZG93bkZpbHRlckxvY2F0aW9uKTtcbiAgICBpbnB1dExvY2F0aW9uLmZvY3VzKCk7XG4gIH0pO1xuXG4gIGJ1dHRvbkNhdGVnb3JpZXMuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyQ2F0ZWdvcmllcyk7XG4gIH0pO1xuXG4gIGlucHV0TG9jYXRpb24ub25mb2N1cyA9IGZ1bmN0aW9uICgpIHtcbiAgICBkYXRhbGlzdExvY2F0aW9uLnN0eWxlLmRpc3BsYXkgPSAnYmxvY2snO1xuICAgIGlucHV0TG9jYXRpb24uc3R5bGUuYm9yZGVyUmFkaXVzID0gJzVweCA1cHggMCAwJztcbiAgfTtcbiAgZm9yIChsZXQgaW5kZXggaW4gZGF0YWxpc3RMb2NhdGlvbi5vcHRpb25zKSB7XG4gICAgY29uc3Qgb3B0aW9uOiBIVE1MT3B0aW9uRWxlbWVudCA9IGRhdGFsaXN0TG9jYXRpb24ub3B0aW9uc1tpbmRleF07XG4gICAgb3B0aW9uLm9uY2xpY2sgPSBmdW5jdGlvbiAoKSB7XG4gICAgICBpbnB1dExvY2F0aW9uLnZhbHVlID0gb3B0aW9uLnZhbHVlO1xuICAgICAgc3RhdHVzRmlsdGVyTG9jYXRpb24uaW5uZXJIVE1MID0gb3B0aW9uLnZhbHVlO1xuICAgICAgZGF0YWxpc3RMb2NhdGlvbi5zdHlsZS5kaXNwbGF5ID0gJ25vbmUnO1xuICAgICAgaW5wdXRMb2NhdGlvbi5zdHlsZS5ib3JkZXJSYWRpdXMgPSAnNXB4JztcbiAgICB9O1xuICB9XG5cbiAgaW5wdXRMb2NhdGlvbi5vbmlucHV0ID0gZnVuY3Rpb24gKCkge1xuICAgIGN1cnJlbnRGb2N1cyA9IC0xO1xuICAgIGNvbnN0IHRleHQgPSBpbnB1dExvY2F0aW9uLnZhbHVlLnRvVXBwZXJDYXNlKCk7XG4gICAgZm9yIChsZXQgaW5kZXggaW4gZGF0YWxpc3RMb2NhdGlvbi5vcHRpb25zKSB7XG4gICAgICBjb25zdCBvcHRpb246IEhUTUxPcHRpb25FbGVtZW50ID0gZGF0YWxpc3RMb2NhdGlvbi5vcHRpb25zW2luZGV4XTtcbiAgICAgIG9wdGlvbi52YWx1ZS50b1VwcGVyQ2FzZSgpLmluZGV4T2YodGV4dCkgPiAtMVxuICAgICAgICA/IChvcHRpb24uc3R5bGUuZGlzcGxheSA9ICdibG9jaycpXG4gICAgICAgIDogKG9wdGlvbi5zdHlsZS5kaXNwbGF5ID0gJ25vbmUnKTtcbiAgICB9XG4gIH07XG5cbiAgbGV0IGN1cnJlbnRGb2N1cyA9IC0xO1xuICBpbnB1dExvY2F0aW9uLm9ua2V5ZG93biA9IGZ1bmN0aW9uIChlKSB7XG4gICAgaWYgKGUua2V5Q29kZSA9PSA0MCkge1xuICAgICAgY3VycmVudEZvY3VzKys7XG4gICAgICBhZGRBY3RpdmUoZGF0YWxpc3RMb2NhdGlvbi5vcHRpb25zKTtcbiAgICB9IGVsc2UgaWYgKGUua2V5Q29kZSA9PSAzOCkge1xuICAgICAgY3VycmVudEZvY3VzLS07XG4gICAgICBhZGRBY3RpdmUoZGF0YWxpc3RMb2NhdGlvbi5vcHRpb25zKTtcbiAgICB9IGVsc2UgaWYgKGUua2V5Q29kZSA9PSAxMykge1xuICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgaWYgKGN1cnJlbnRGb2N1cyA+IC0xKSB7XG4gICAgICAgIGlmIChkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnMpIHtcbiAgICAgICAgICBkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnNbY3VycmVudEZvY3VzXS5jbGljaygpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9O1xuXG4gIGZ1bmN0aW9uIGFkZEFjdGl2ZSh4OiBIVE1MQ29sbGVjdGlvbk9mPEhUTUxPcHRpb25FbGVtZW50Pikge1xuICAgIGlmICgheCkgcmV0dXJuO1xuXG4gICAgZmFsc2U7XG4gICAgcmVtb3ZlQWN0aXZlKHgpO1xuICAgIGlmIChjdXJyZW50Rm9jdXMgPj0geC5sZW5ndGgpIGN1cnJlbnRGb2N1cyA9IDA7XG4gICAgaWYgKGN1cnJlbnRGb2N1cyA8IDApIGN1cnJlbnRGb2N1cyA9IHgubGVuZ3RoIC0gMTtcbiAgICB4W2N1cnJlbnRGb2N1c10uY2xhc3NMaXN0LmFkZCgnYWN0aXZlJyk7XG4gIH1cblxuICBmdW5jdGlvbiByZW1vdmVBY3RpdmUoeDogSFRNTENvbGxlY3Rpb25PZjxIVE1MT3B0aW9uRWxlbWVudD4pIHtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IHgubGVuZ3RoOyBpKyspIHtcbiAgICAgIHhbaV0uY2xhc3NMaXN0LnJlbW92ZSgnYWN0aXZlJyk7XG4gICAgfVxuICB9XG59KTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==
