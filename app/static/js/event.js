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
        var datePickers = document.querySelectorAll('.datepicker-picker');
        if (datePickers) {
            datePickers.forEach(function (datePicker) {
                setGreyDates(datePicker);
            });
        }
        var calendarButtons = document.querySelectorAll('.next-btn, .prev-btn');
        calendarButtons.forEach(function (button) {
            button.addEventListener('click', function (event) {
                var target = event.target;
                var datePicker = target.closest('.datepicker-picker');
                if (!datePicker)
                    return;
                setGreyDates(datePicker);
                datePicker.addEventListener('DOMSubtreeModified', function () {
                    setGreyDates(datePicker);
                });
            });
        });
    }, 1000);
}
exports.disableDateFlowbite = disableDateFlowbite;
function setGreyDates(datePicker) {
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
}


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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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LFNBQVMsQ0FBQztnQkFDbEQsOEJBQWtCLEVBQUMsc0JBQXNCLENBQUMsQ0FBQztZQUM3QyxDQUFDLENBQUMsQ0FBQztRQUNMLENBQUMsQ0FBQyxDQUFDO1FBQ0gsdUJBQXFCLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1lBQzlDLHNCQUFzQixDQUFDLG1CQUFtQixFQUFFLHVCQUFxQixDQUFDLENBQUM7UUFDckUsQ0FBQyxDQUFDLENBQUM7S0FDSjtBQUNILENBQUMsQ0FBQyxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL3V0aWxzLnRzIiwid2VicGFjazovL3N0YXRpYy93ZWJwYWNrL2Jvb3RzdHJhcCIsIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvZXZlbnQudHMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gYWRkSGlkZGVuQ2xhc3MoZWxlbWVudDogSFRNTEVsZW1lbnQpIHtcbiAgZWxlbWVudC5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbn1cblxuZnVuY3Rpb24gaGlkZUVsZW1lbnRzKFxuICBldmVudDogTW91c2VFdmVudCxcbiAgZWxlbWVudDogSFRNTEVsZW1lbnQsXG4gIG90aGVyRWxlbWVudD86IEhUTUxFbGVtZW50W10sXG4pIHtcbiAgaWYgKFxuICAgICFlbGVtZW50LmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSAmJlxuICAgICFvdGhlckVsZW1lbnQuc29tZShlbCA9PiBlbC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkpXG4gICkge1xuICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICB9XG59XG5cbi8vIGV4cG9ydCBmdW5jdGlvbiB1bmxvY2tTY3JvbGwoKSB7XG4vLyAgIGNvbnN0IHNjcm9sbFkgPSBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcDtcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5wb3NpdGlvbiA9ICcnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcCA9ICcnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLmxlZnQgPSAnJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5yaWdodCA9ICcnO1xuLy8gICB3aW5kb3cuc2Nyb2xsVG8oMCwgcGFyc2VJbnQoc2Nyb2xsWSB8fCAnMCcpICogLTEpO1xuXG4vLyAgIGNvbnNvbGUubG9nKCd1bmxvY2sgc2Nyb2xsJyk7XG4vLyB9XG5cbi8vIGV4cG9ydCBmdW5jdGlvbiBsb2NrU2Nyb2xsKCkge1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnBvc2l0aW9uID0gJ2ZpeGVkJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS50b3AgPSBgLSR7d2luZG93LnNjcm9sbFl9cHhgO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLmxlZnQgPSAnMCc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnMCc7XG5cbi8vICAgY29uc29sZS5sb2coJ2xvY2sgc2Nyb2xsJyk7XG4vLyB9XG5cbmV4cG9ydCBmdW5jdGlvbiBoYW5kbGVIaWRlRWxlbWVudHMoXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ6IEhUTUxFbGVtZW50W10gPSBbXSxcbikge1xuICBlbGVtZW50LmNsYXNzTGlzdC50b2dnbGUoJ2hpZGRlbicpO1xuICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsIChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICAgIGhpZGVFbGVtZW50cyhldmVudCwgZWxlbWVudCwgb3RoZXJFbGVtZW50KTtcbiAgfSk7XG5cbiAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIGZ1bmN0aW9uIChldmVudCkge1xuICAgIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgICB9XG4gIH0pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVzaXplQ2hhdCgpIHtcbiAgY29uc29sZS5sb2coJ3Jlc2l6ZUNoYXQnKTtcbiAgY29uc3QgaGVhZGVyOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5oZWFkZXInKTtcbiAgY29uc3QgY2hhdE1haW46IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2NoYXQtYm9keScpO1xuICBjb25zdCBjaGF0Rm9vdGVyOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWZvb3RlcicpO1xuICBjb25zdCBjaGF0V2luZG93OiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LXdpbmRvdycpO1xuICBjb25zdCBzY3JlZW5XaXRoOiBudW1iZXIgPSB3aW5kb3cuaW5uZXJXaWR0aDtcbiAgY29uc3QgaGVhZGVyQm90dG9tOiBudW1iZXIgPSBoZWFkZXIub2Zmc2V0VG9wICsgaGVhZGVyLm9mZnNldEhlaWdodDtcbiAgY29uc3QgY2hhdFdpbmRvd1RvcDogbnVtYmVyID0gY2hhdFdpbmRvdy5vZmZzZXRUb3A7XG4gIGNvbnN0IGZpeGVkTWluRGlzdGFuY2U6IG51bWJlciA9IDI1MDtcbiAgY29uc3QgbWF4Q2hhdFdpbmRvd0hlaWdodDogbnVtYmVyID0gNjUwO1xuICBjb25zdCBhdmFpbGFibGVTcGFjZTogbnVtYmVyID0gY2hhdFdpbmRvd1RvcCAtIGhlYWRlckJvdHRvbTtcblxuICBpZiAoc2NyZWVuV2l0aCA8IDY0MCkge1xuICAgIGNoYXRNYWluLnN0eWxlLmhlaWdodCA9IGBjYWxjKDEwMCUgLSAke2NoYXRGb290ZXIub2Zmc2V0SGVpZ2h0fXB4KWA7XG4gICAgcmV0dXJuO1xuICB9XG5cbiAgaWYgKCFoZWFkZXIgfHwgIWNoYXRXaW5kb3cpIHJldHVybjtcblxuICBpZiAoYXZhaWxhYmxlU3BhY2UgPCBmaXhlZE1pbkRpc3RhbmNlKSB7XG4gICAgY2hhdFdpbmRvdy5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDB2aCAtICR7Zml4ZWRNaW5EaXN0YW5jZX1weClgO1xuICB9XG5cbiAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgaWYgKGNoYXRXaW5kb3cub2Zmc2V0SGVpZ2h0ID4gbWF4Q2hhdFdpbmRvd0hlaWdodCkge1xuICAgICAgY2hhdFdpbmRvdy5zdHlsZS5oZWlnaHQgPSBgJHttYXhDaGF0V2luZG93SGVpZ2h0fXB4YDtcbiAgICB9XG4gIH0sIDUwMCk7XG5cbiAgaWYgKGNoYXRNYWluICYmIGNoYXRGb290ZXIpIHtcbiAgICBjaGF0TWFpbi5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDAlIC0gJHtjaGF0Rm9vdGVyLm9mZnNldEhlaWdodH1weClgO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBsb2NrU2Nyb2xsQm9keSgpIHtcbiAgY29uc29sZS5sb2coJ2xvY2tTY3JvbGxCb2R5Jyk7XG5cbiAgY29uc3Qgc2NyZWVuV2l0aDogbnVtYmVyID0gd2luZG93LmlubmVyV2lkdGg7XG4gIGlmIChzY3JlZW5XaXRoIDwgNjQwKSB7XG4gICAgZG9jdW1lbnQuYm9keS5zdHlsZS5wb3NpdGlvbiA9ICdmaXhlZCc7XG4gICAgZG9jdW1lbnQuYm9keS5zdHlsZS50b3AgPSBgLSR7d2luZG93LnNjcm9sbFl9cHhgO1xuICAgIGRvY3VtZW50LmJvZHkuc3R5bGUubGVmdCA9ICcwJztcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLnJpZ2h0ID0gJzAnO1xuICB9XG59XG5cbmV4cG9ydCBmdW5jdGlvbiB1bmxvY2tTY3JvbGxCb2R5KCkge1xuICBjb25zb2xlLmxvZygndW5sb2NrU2Nyb2xsQm9keScpO1xuXG4gIGNvbnN0IHNjcmVlbldpdGg6IG51bWJlciA9IHdpbmRvdy5pbm5lcldpZHRoO1xuICBpZiAoc2NyZWVuV2l0aCA8IDY0MCkge1xuICAgIGNvbnN0IHNjcm9sbFkgPSBkb2N1bWVudC5ib2R5LnN0eWxlLnRvcDtcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLnBvc2l0aW9uID0gJyc7XG4gICAgZG9jdW1lbnQuYm9keS5zdHlsZS50b3AgPSAnJztcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLmxlZnQgPSAnJztcbiAgICBkb2N1bWVudC5ib2R5LnN0eWxlLnJpZ2h0ID0gJyc7XG4gICAgd2luZG93LnNjcm9sbFRvKDAsIHBhcnNlSW50KHNjcm9sbFkgfHwgJzAnKSAqIC0xKTtcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2Nyb2xsRG93bihlbGVtZW50OiBIVE1MRGl2RWxlbWVudCkge1xuICBlbGVtZW50LnNjcm9sbFRvKHtcbiAgICB0b3A6IGVsZW1lbnQuc2Nyb2xsSGVpZ2h0LFxuICB9KTtcbn1cblxuY29uc3Qgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24gPSAyMDA7XG5leHBvcnQgZnVuY3Rpb24gc2Nyb2xsRG93blNtb290aChlbGVtZW50OiBIVE1MRGl2RWxlbWVudCkge1xuICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICBlbGVtZW50LnNjcm9sbFRvKHtcbiAgICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gICAgICBiZWhhdmlvcjogJ3Ntb290aCcsXG4gICAgfSk7XG4gIH0sIHNjcm9sbEFuaW1hdGlvbkR1cmF0aW9uKTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNvY2lhbE1lZGlhU2hhcmUoKSB7XG4gIGNvbnNvbGUubG9nKCdzb2NpYWxNZWRpYVNoYXJlJyk7XG4gIGNvbnN0IGZiU2hhcmVJY29ucyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXG4gICAgJy5mYi1zaGFyZScsXG4gICkgYXMgTm9kZUxpc3RPZjxIVE1MQW5jaG9yRWxlbWVudD47XG4gIGZiU2hhcmVJY29ucy5mb3JFYWNoKGZiSWNvbiA9PiB7XG4gICAgZmJJY29uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgY29uc3QgbGluayA9IGVuY29kZVVSSUNvbXBvbmVudCh3aW5kb3cubG9jYXRpb24uaHJlZik7XG4gICAgICBmYkljb24uaHJlZiA9IGBodHRwczovL3d3dy5mYWNlYm9vay5jb20vc2hhcmUucGhwP3U9JHtsaW5rfWA7XG4gICAgICBjb25zb2xlLmxvZyhmYkljb24uaHJlZik7XG4gICAgfSk7XG4gIH0pO1xuXG4gIGNvbnN0IGluc3RhU2hhcmVJY29ucyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXG4gICAgJy5pLXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgaW5zdGFTaGFyZUljb25zLmZvckVhY2goaW5zdGFJY29uID0+IHtcbiAgICBpbnN0YUljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGluc3RhSWNvbi5ocmVmID0gYGh0dHBzOi8vd3d3Lmluc3RhZ3JhbS5jb21gO1xuICAgICAgY29uc29sZS5sb2coaW5zdGFJY29uLmhyZWYpO1xuICAgIH0pO1xuICB9KTtcblxuICBjb25zdCB0d2l0dGVyU2hhcmVJY29ucyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXG4gICAgJy54LXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgdHdpdHRlclNoYXJlSWNvbnMuZm9yRWFjaCh0d2l0dGVySWNvbiA9PiB7XG4gICAgdHdpdHRlckljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGNvbnN0IHRleHQgPSBlbmNvZGVVUklDb21wb25lbnQoXG4gICAgICAgICdDaGVjayBvdXQgY29vbCB0aWNrZXRzIGZvciBzYWxlIG9uIEZhblRpY2tldCcsXG4gICAgICApO1xuICAgICAgY29uc3QgaGFzaHRhZ3MgPSBlbmNvZGVVUklDb21wb25lbnQoJ3RpY2tldHMsZm9yc2FsZScpO1xuICAgICAgdHdpdHRlckljb24uaHJlZiA9IGBodHRwczovL3R3aXR0ZXIuY29tL3NoYXJlP3VybD0ke2xpbmt9JnRleHQ9JHt0ZXh0fSZoYXNodGFncz0ke2hhc2h0YWdzfWA7XG4gICAgICBjb25zb2xlLmxvZyh0d2l0dGVySWNvbi5ocmVmKTtcbiAgICB9KTtcbiAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBkaXNhYmxlRGF0ZUZsb3diaXRlKCkge1xuICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICBjb25zdCBkYXRlUGlja2VycyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5kYXRlcGlja2VyLXBpY2tlcicpO1xuXG4gICAgaWYgKGRhdGVQaWNrZXJzKSB7XG4gICAgICBkYXRlUGlja2Vycy5mb3JFYWNoKChkYXRlUGlja2VyOiBIVE1MRGl2RWxlbWVudCkgPT4ge1xuICAgICAgICBzZXRHcmV5RGF0ZXMoZGF0ZVBpY2tlcik7XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBjb25zdCBjYWxlbmRhckJ1dHRvbnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcubmV4dC1idG4sIC5wcmV2LWJ0bicpO1xuXG4gICAgY2FsZW5kYXJCdXR0b25zLmZvckVhY2goKGJ1dHRvbjogSFRNTEJ1dHRvbkVsZW1lbnQpID0+IHtcbiAgICAgIGJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIChldmVudDogRXZlbnQpID0+IHtcbiAgICAgICAgY29uc3QgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgICAgICBjb25zdCBkYXRlUGlja2VyID0gdGFyZ2V0LmNsb3Nlc3QoXG4gICAgICAgICAgJy5kYXRlcGlja2VyLXBpY2tlcicsXG4gICAgICAgICkgYXMgSFRNTERpdkVsZW1lbnQ7XG5cbiAgICAgICAgaWYgKCFkYXRlUGlja2VyKSByZXR1cm47XG5cbiAgICAgICAgc2V0R3JleURhdGVzKGRhdGVQaWNrZXIpO1xuXG4gICAgICAgIGRhdGVQaWNrZXIuYWRkRXZlbnRMaXN0ZW5lcignRE9NU3VidHJlZU1vZGlmaWVkJywgKCkgPT4ge1xuICAgICAgICAgIHNldEdyZXlEYXRlcyhkYXRlUGlja2VyKTtcbiAgICAgICAgfSk7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgfSwgMTAwMCk7XG59XG5cbmZ1bmN0aW9uIHNldEdyZXlEYXRlcyhkYXRlUGlja2VyOiBIVE1MRGl2RWxlbWVudCkge1xuICBjb25zdCBtb250aFRpdGxlID0gZGF0ZVBpY2tlci5xdWVyeVNlbGVjdG9yKCcudmlldy1zd2l0Y2gnKTtcbiAgY29uc3QgbW9udGggPSBtb250aFRpdGxlLnRleHRDb250ZW50LnNwbGl0KCcgJylbMF07XG4gIGNvbnN0IHllYXIgPSBtb250aFRpdGxlLnRleHRDb250ZW50LnNwbGl0KCcgJylbMV07XG4gIGNvbnN0IGN1cnJlbnREYXRlID0gbmV3IERhdGUoYCR7bW9udGh9IDEsICR7eWVhcn1gKS5nZXRNb250aCgpO1xuICBjb25zdCBhbGxEYXRlcyA9IGRhdGVQaWNrZXIucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXItY2VsbCcpO1xuXG4gIGFsbERhdGVzLmZvckVhY2goKGRhdGU6IEhUTUxEaXZFbGVtZW50KSA9PiB7XG4gICAgY29uc3QgdGltZVN0YW1wID0gZGF0ZS5nZXRBdHRyaWJ1dGUoJ2RhdGEtZGF0ZScpO1xuICAgIGNvbnN0IGRhdGVNb250aCA9IG5ldyBEYXRlKHBhcnNlSW50KHRpbWVTdGFtcCkpLmdldE1vbnRoKCk7XG5cbiAgICBkYXRlTW9udGggIT09IGN1cnJlbnREYXRlXG4gICAgICA/IChkYXRlLnN0eWxlLmNvbG9yID0gJyM5OWExYTMnKVxuICAgICAgOiAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjZmZmJyk7XG4gIH0pO1xufVxuIiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXShtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsImltcG9ydCB7aGFuZGxlSGlkZUVsZW1lbnRzfSBmcm9tICcuL3V0aWxzJztcblxuZnVuY3Rpb24gZmlsdGVyRHJvcGRvd25Mb2NhdGlvbihcbiAgZHJvcGRvd25MaXN0OiBOb2RlTGlzdE9mPEhUTUxEaXZFbGVtZW50PixcbiAgZHJvcGRvd25JbnB1dDogSFRNTElucHV0RWxlbWVudCxcbikge1xuICBjb25zdCBmaWx0ZXIgPSBkcm9wZG93bklucHV0LnZhbHVlLnRvVXBwZXJDYXNlKCk7XG5cbiAgZm9yIChsZXQgaSA9IDA7IGkgPCBkcm9wZG93bkxpc3QubGVuZ3RoOyBpKyspIHtcbiAgICBjb25zdCB0eHRWYWx1ZSA9IGRyb3Bkb3duTGlzdFtpXS50ZXh0Q29udGVudCB8fCBkcm9wZG93bkxpc3RbaV0uaW5uZXJUZXh0O1xuICAgIGlmICh0eHRWYWx1ZS50b1VwcGVyQ2FzZSgpLmluZGV4T2YoZmlsdGVyKSA+IC0xKSB7XG4gICAgICBkcm9wZG93bkxpc3RbaV0uc3R5bGUuZGlzcGxheSA9ICcnO1xuICAgIH0gZWxzZSB7XG4gICAgICBkcm9wZG93bkxpc3RbaV0uc3R5bGUuZGlzcGxheSA9ICdub25lJztcbiAgICB9XG4gIH1cbn1cblxuZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsIGZ1bmN0aW9uICgpIHtcbiAgY29uc3QgYnV0dG9uRmlsdGVyRGF0ZSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNldmVudHMtZmlsdGVyLWRhdGUtYnV0dG9uJyk7XG4gIGNvbnN0IGJ1dHRvbkxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGJ1dHRvbkxvY2F0aW9uTmFtZXMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKFxuICAgICcuZHJvcGRvd24tbG9jYXRpb24tbmFtZS1idXR0b24nLFxuICApIGFzIE5vZGVMaXN0T2Y8SFRNTERpdkVsZW1lbnQ+O1xuXG4gIGNvbnN0IGJ1dHRvbkNhdGVnb3JpZXMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1jYXRlZ29yaWVzLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGJ1dHRvbkRhdGVBcHBseSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWRhdGUtYXBwbHktYnV0dG9uJyxcbiAgKTtcblxuICBjb25zdCBkcm9wZG93bkZpbHRlckRhdGU6IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItZGF0ZS1kcm9wZG93bicsXG4gICk7XG4gIGNvbnN0IGRyb3Bkb3duRmlsdGVyTG9jYXRpb246IEhUTUxEaXZFbGVtZW50ID1cbiAgICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjZHJvcGRvd24tbG9jYXRpb24nKTtcbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWNhdGVnb3JpZXMtZHJvcGRvd24nLFxuICApO1xuXG4gIGNvbnN0IHN0YXR1c0ZpbHRlckxvY2F0aW9uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24tc3RhdHVzJyxcbiAgKTtcblxuICBpZiAoYnV0dG9uRmlsdGVyRGF0ZSkge1xuICAgIGJ1dHRvbkZpbHRlckRhdGUuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBkYXRlUGlja2VycyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5kYXRlcGlja2VyJyk7XG4gICAgICBjb25zdCBkYXRlUGlja2VyQXJyYXk6IEhUTUxFbGVtZW50W10gPSBBcnJheS5mcm9tKFxuICAgICAgICBkYXRlUGlja2VycyxcbiAgICAgICkgYXMgSFRNTEVsZW1lbnRbXTtcblxuICAgICAgaGFuZGxlSGlkZUVsZW1lbnRzKGRyb3Bkb3duRmlsdGVyRGF0ZSwgZGF0ZVBpY2tlckFycmF5KTtcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChidXR0b25EYXRlQXBwbHkpIHtcbiAgICBidXR0b25EYXRlQXBwbHkuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBkcm9wZG93bkZpbHRlckRhdGUuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gICAgfSk7XG4gIH1cblxuICBpZiAoYnV0dG9uQ2F0ZWdvcmllcykge1xuICAgIGJ1dHRvbkNhdGVnb3JpZXMuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBoYW5kbGVIaWRlRWxlbWVudHMoZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzKTtcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChzdGF0dXNGaWx0ZXJMb2NhdGlvbikge1xuICAgIGNvbnN0IGRyb3BEb3duTG9jYXRpb25JbnB1dDogSFRNTElucHV0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgICAnI2Ryb3Bkb3duLWxvY2F0aW9uLWlucHV0JyxcbiAgICApO1xuXG4gICAgaWYgKGJ1dHRvbkxvY2F0aW9uKSB7XG4gICAgICBidXR0b25Mb2NhdGlvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICAgICAgZHJvcERvd25Mb2NhdGlvbklucHV0LmZvY3VzKCk7XG4gICAgICAgIGhhbmRsZUhpZGVFbGVtZW50cyhkcm9wZG93bkZpbHRlckxvY2F0aW9uKTtcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGJ1dHRvbkxvY2F0aW9uTmFtZXMuZm9yRWFjaCgoYnV0dG9uOiBIVE1MRGl2RWxlbWVudCkgPT4ge1xuICAgICAgYnV0dG9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgICBzdGF0dXNGaWx0ZXJMb2NhdGlvbi5pbm5lckhUTUwgPSBidXR0b24uaW5uZXJIVE1MO1xuICAgICAgICBoYW5kbGVIaWRlRWxlbWVudHMoZHJvcGRvd25GaWx0ZXJMb2NhdGlvbik7XG4gICAgICB9KTtcbiAgICB9KTtcbiAgICBkcm9wRG93bkxvY2F0aW9uSW5wdXQuYWRkRXZlbnRMaXN0ZW5lcigna2V5dXAnLCAoKSA9PiB7XG4gICAgICBmaWx0ZXJEcm9wZG93bkxvY2F0aW9uKGJ1dHRvbkxvY2F0aW9uTmFtZXMsIGRyb3BEb3duTG9jYXRpb25JbnB1dCk7XG4gICAgfSk7XG4gIH1cbn0pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9