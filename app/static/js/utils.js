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
exports.disableDateFlowbite = exports.socialMediaShare = exports.scrollDownSmooth = exports.scrollDown = exports.resizeChat = exports.handleHideElements = void 0;
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
        console.log('body hidden', document.body);
        document.body.style.overflow = 'hidden';
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvdXRpbHMuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7O0FBQUEsU0FBUyxjQUFjLENBQUMsT0FBb0I7SUFDMUMsT0FBTyxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsUUFBUSxDQUFDLENBQUM7QUFDbEMsQ0FBQztBQUVELFNBQVMsWUFBWSxDQUNuQixLQUFpQixFQUNqQixPQUFvQixFQUNwQixZQUE0QjtJQUU1QixJQUNFLENBQUMsT0FBTyxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsTUFBYyxDQUFDO1FBQ3ZDLENBQUMsWUFBWSxDQUFDLElBQUksQ0FBQyxZQUFFLElBQUksU0FBRSxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsTUFBYyxDQUFDLEVBQWpDLENBQWlDLENBQUMsRUFDM0Q7UUFDQSxjQUFjLENBQUMsT0FBTyxDQUFDLENBQUM7S0FDekI7QUFDSCxDQUFDO0FBRUQsbUNBQW1DO0FBQ25DLDZDQUE2QztBQUM3Qyx1Q0FBdUM7QUFDdkMsa0NBQWtDO0FBQ2xDLG1DQUFtQztBQUNuQyxvQ0FBb0M7QUFDcEMsdURBQXVEO0FBRXZELGtDQUFrQztBQUNsQyxJQUFJO0FBRUosaUNBQWlDO0FBQ2pDLDRDQUE0QztBQUM1QyxzREFBc0Q7QUFDdEQsb0NBQW9DO0FBQ3BDLHFDQUFxQztBQUVyQyxnQ0FBZ0M7QUFDaEMsSUFBSTtBQUVKLFNBQWdCLGtCQUFrQixDQUNoQyxPQUFvQixFQUNwQixZQUFnQztJQUFoQyxnREFBZ0M7SUFFaEMsT0FBTyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUM7SUFDbkMsTUFBTSxDQUFDLGdCQUFnQixDQUFDLFNBQVMsRUFBRSxVQUFDLEtBQWlCO1FBQ25ELFlBQVksQ0FBQyxLQUFLLEVBQUUsT0FBTyxFQUFFLFlBQVksQ0FBQyxDQUFDO0lBQzdDLENBQUMsQ0FBQyxDQUFDO0lBRUgsUUFBUSxDQUFDLGdCQUFnQixDQUFDLFNBQVMsRUFBRSxVQUFVLEtBQUs7UUFDbEQsSUFBSSxLQUFLLENBQUMsR0FBRyxLQUFLLFFBQVEsRUFBRTtZQUMxQixjQUFjLENBQUMsT0FBTyxDQUFDLENBQUM7U0FDekI7SUFDSCxDQUFDLENBQUMsQ0FBQztBQUNMLENBQUM7QUFkRCxnREFjQztBQUVELFNBQWdCLFVBQVU7SUFDeEIsSUFBTSxNQUFNLEdBQWdCLFFBQVEsQ0FBQyxhQUFhLENBQUMsU0FBUyxDQUFDLENBQUM7SUFDOUQsSUFBTSxRQUFRLEdBQWdCLFFBQVEsQ0FBQyxhQUFhLENBQUMsWUFBWSxDQUFDLENBQUM7SUFDbkUsSUFBTSxVQUFVLEdBQWdCLFFBQVEsQ0FBQyxhQUFhLENBQUMsY0FBYyxDQUFDLENBQUM7SUFDdkUsSUFBTSxVQUFVLEdBQWdCLFFBQVEsQ0FBQyxhQUFhLENBQUMsY0FBYyxDQUFDLENBQUM7SUFDdkUsSUFBTSxVQUFVLEdBQVcsTUFBTSxDQUFDLFVBQVUsQ0FBQztJQUM3QyxJQUFNLFlBQVksR0FBVyxNQUFNLENBQUMsU0FBUyxHQUFHLE1BQU0sQ0FBQyxZQUFZLENBQUM7SUFDcEUsSUFBTSxhQUFhLEdBQVcsVUFBVSxDQUFDLFNBQVMsQ0FBQztJQUNuRCxJQUFNLGdCQUFnQixHQUFXLEdBQUcsQ0FBQztJQUNyQyxJQUFNLG1CQUFtQixHQUFXLEdBQUcsQ0FBQztJQUN4QyxJQUFNLGNBQWMsR0FBVyxhQUFhLEdBQUcsWUFBWSxDQUFDO0lBRTVELElBQUksVUFBVSxHQUFHLEdBQUcsRUFBRTtRQUNwQixRQUFRLENBQUMsS0FBSyxDQUFDLE1BQU0sR0FBRyxzQkFBZSxVQUFVLENBQUMsWUFBWSxRQUFLLENBQUM7UUFDcEUsT0FBTyxDQUFDLEdBQUcsQ0FBQyxhQUFhLEVBQUUsUUFBUSxDQUFDLElBQUksQ0FBQyxDQUFDO1FBRTFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLFFBQVEsR0FBRyxRQUFRLENBQUM7UUFDeEMsT0FBTztLQUNSO0lBRUQsSUFBSSxDQUFDLE1BQU0sSUFBSSxDQUFDLFVBQVU7UUFBRSxPQUFPO0lBRW5DLElBQUksY0FBYyxHQUFHLGdCQUFnQixFQUFFO1FBQ3JDLFVBQVUsQ0FBQyxLQUFLLENBQUMsTUFBTSxHQUFHLHVCQUFnQixnQkFBZ0IsUUFBSyxDQUFDO0tBQ2pFO0lBRUQsVUFBVSxDQUFDO1FBQ1QsSUFBSSxVQUFVLENBQUMsWUFBWSxHQUFHLG1CQUFtQixFQUFFO1lBQ2pELFVBQVUsQ0FBQyxLQUFLLENBQUMsTUFBTSxHQUFHLFVBQUcsbUJBQW1CLE9BQUksQ0FBQztTQUN0RDtJQUNILENBQUMsRUFBRSxHQUFHLENBQUMsQ0FBQztJQUVSLElBQUksUUFBUSxJQUFJLFVBQVUsRUFBRTtRQUMxQixRQUFRLENBQUMsS0FBSyxDQUFDLE1BQU0sR0FBRyxzQkFBZSxVQUFVLENBQUMsWUFBWSxRQUFLLENBQUM7S0FDckU7QUFDSCxDQUFDO0FBbkNELGdDQW1DQztBQUVELFNBQWdCLFVBQVUsQ0FBQyxPQUF1QjtJQUNoRCxPQUFPLENBQUMsUUFBUSxDQUFDO1FBQ2YsR0FBRyxFQUFFLE9BQU8sQ0FBQyxZQUFZO0tBQzFCLENBQUMsQ0FBQztBQUNMLENBQUM7QUFKRCxnQ0FJQztBQUVELElBQU0sdUJBQXVCLEdBQUcsR0FBRyxDQUFDO0FBQ3BDLFNBQWdCLGdCQUFnQixDQUFDLE9BQXVCO0lBQ3RELFVBQVUsQ0FBQztRQUNULE9BQU8sQ0FBQyxRQUFRLENBQUM7WUFDZixHQUFHLEVBQUUsT0FBTyxDQUFDLFlBQVk7WUFDekIsUUFBUSxFQUFFLFFBQVE7U0FDbkIsQ0FBQyxDQUFDO0lBQ0wsQ0FBQyxFQUFFLHVCQUF1QixDQUFDLENBQUM7QUFDOUIsQ0FBQztBQVBELDRDQU9DO0FBRUQsU0FBZ0IsZ0JBQWdCO0lBQzlCLE9BQU8sQ0FBQyxHQUFHLENBQUMsa0JBQWtCLENBQUMsQ0FBQztJQUNoQyxJQUFNLFlBQVksR0FBRyxRQUFRLENBQUMsZ0JBQWdCLENBQzVDLFdBQVcsQ0FDcUIsQ0FBQztJQUNuQyxZQUFZLENBQUMsT0FBTyxDQUFDLGdCQUFNO1FBQ3pCLE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7WUFDL0IsSUFBTSxJQUFJLEdBQUcsa0JBQWtCLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUN0RCxNQUFNLENBQUMsSUFBSSxHQUFHLCtDQUF3QyxJQUFJLENBQUUsQ0FBQztZQUM3RCxPQUFPLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUMzQixDQUFDLENBQUMsQ0FBQztJQUNMLENBQUMsQ0FBQyxDQUFDO0lBRUgsSUFBTSxlQUFlLEdBQUcsUUFBUSxDQUFDLGdCQUFnQixDQUMvQyxVQUFVLENBQ3NCLENBQUM7SUFDbkMsZUFBZSxDQUFDLE9BQU8sQ0FBQyxtQkFBUztRQUMvQixTQUFTLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1lBQ2xDLElBQU0sSUFBSSxHQUFHLGtCQUFrQixDQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsSUFBSSxDQUFDLENBQUM7WUFDdEQsU0FBUyxDQUFDLElBQUksR0FBRywyQkFBMkIsQ0FBQztZQUM3QyxPQUFPLENBQUMsR0FBRyxDQUFDLFNBQVMsQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUM5QixDQUFDLENBQUMsQ0FBQztJQUNMLENBQUMsQ0FBQyxDQUFDO0lBRUgsSUFBTSxpQkFBaUIsR0FBRyxRQUFRLENBQUMsZ0JBQWdCLENBQ2pELFVBQVUsQ0FDc0IsQ0FBQztJQUNuQyxpQkFBaUIsQ0FBQyxPQUFPLENBQUMscUJBQVc7UUFDbkMsV0FBVyxDQUFDLGdCQUFnQixDQUFDLE9BQU8sRUFBRTtZQUNwQyxJQUFNLElBQUksR0FBRyxrQkFBa0IsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLElBQUksQ0FBQyxDQUFDO1lBQ3RELElBQU0sSUFBSSxHQUFHLGtCQUFrQixDQUM3Qiw4Q0FBOEMsQ0FDL0MsQ0FBQztZQUNGLElBQU0sUUFBUSxHQUFHLGtCQUFrQixDQUFDLGlCQUFpQixDQUFDLENBQUM7WUFDdkQsV0FBVyxDQUFDLElBQUksR0FBRyx3Q0FBaUMsSUFBSSxtQkFBUyxJQUFJLHVCQUFhLFFBQVEsQ0FBRSxDQUFDO1lBQzdGLE9BQU8sQ0FBQyxHQUFHLENBQUMsV0FBVyxDQUFDLElBQUksQ0FBQyxDQUFDO1FBQ2hDLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQyxDQUFDLENBQUM7QUFDTCxDQUFDO0FBdENELDRDQXNDQztBQUVELFNBQWdCLG1CQUFtQjtJQUNqQyxVQUFVLENBQUM7UUFDVCxJQUFNLFFBQVEsR0FBRyxRQUFRLENBQUMsZ0JBQWdCLENBQUMsa0JBQWtCLENBQUMsQ0FBQztRQUUvRCxJQUFNLFlBQVksR0FBRyxJQUFJLElBQUksRUFBRSxDQUFDLFFBQVEsRUFBRSxDQUFDO1FBQzNDLFFBQVEsQ0FBQyxPQUFPLENBQUMsVUFBQyxJQUFvQjtZQUNwQyxJQUFNLFNBQVMsR0FBRyxJQUFJLENBQUMsWUFBWSxDQUFDLFdBQVcsQ0FBQyxDQUFDO1lBQ2pELElBQU0sU0FBUyxHQUFHLElBQUksSUFBSSxDQUFDLFFBQVEsQ0FBQyxTQUFTLENBQUMsQ0FBQyxDQUFDLFFBQVEsRUFBRSxDQUFDO1lBQzNELFNBQVMsS0FBSyxZQUFZO2dCQUN4QixDQUFDLENBQUMsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLEtBQUssR0FBRyxTQUFTLENBQUM7Z0JBQ2hDLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsS0FBSyxHQUFHLE1BQU0sQ0FBQyxDQUFDO1FBQ2xDLENBQUMsQ0FBQyxDQUFDO1FBRUgsSUFBTSxlQUFlLEdBQUcsUUFBUSxDQUFDLGdCQUFnQixDQUFDLHNCQUFzQixDQUFDLENBQUM7UUFFMUUsZUFBZSxDQUFDLE9BQU8sQ0FBQyxVQUFDLE1BQXlCO1lBQ2hELE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUUsVUFBQyxLQUFZO2dCQUM1QyxJQUFNLE1BQU0sR0FBRyxLQUFLLENBQUMsTUFBcUIsQ0FBQztnQkFDM0MsSUFBTSxVQUFVLEdBQUcsTUFBTSxDQUFDLE9BQU8sQ0FBQyxvQkFBb0IsQ0FBQyxDQUFDO2dCQUV4RCxJQUFJLENBQUMsVUFBVTtvQkFBRSxPQUFPO2dCQUV4QixJQUFNLFVBQVUsR0FBRyxVQUFVLENBQUMsYUFBYSxDQUFDLGNBQWMsQ0FBQyxDQUFDO2dCQUM1RCxJQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsV0FBVyxDQUFDLEtBQUssQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQztnQkFDbkQsSUFBTSxJQUFJLEdBQUcsVUFBVSxDQUFDLFdBQVcsQ0FBQyxLQUFLLENBQUMsR0FBRyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7Z0JBQ2xELElBQU0sV0FBVyxHQUFHLElBQUksSUFBSSxDQUFDLFVBQUcsS0FBSyxpQkFBTyxJQUFJLENBQUUsQ0FBQyxDQUFDLFFBQVEsRUFBRSxDQUFDO2dCQUMvRCxJQUFNLFFBQVEsR0FBRyxVQUFVLENBQUMsZ0JBQWdCLENBQUMsa0JBQWtCLENBQUMsQ0FBQztnQkFFakUsUUFBUSxDQUFDLE9BQU8sQ0FBQyxVQUFDLElBQW9CO29CQUNwQyxJQUFNLFNBQVMsR0FBRyxJQUFJLENBQUMsWUFBWSxDQUFDLFdBQVcsQ0FBQyxDQUFDO29CQUNqRCxJQUFNLFNBQVMsR0FBRyxJQUFJLElBQUksQ0FBQyxRQUFRLENBQUMsU0FBUyxDQUFDLENBQUMsQ0FBQyxRQUFRLEVBQUUsQ0FBQztvQkFFM0QsU0FBUyxLQUFLLFdBQVc7d0JBQ3ZCLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsS0FBSyxHQUFHLFNBQVMsQ0FBQzt3QkFDaEMsQ0FBQyxDQUFDLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxLQUFLLEdBQUcsTUFBTSxDQUFDLENBQUM7Z0JBQ2xDLENBQUMsQ0FBQyxDQUFDO1lBQ0wsQ0FBQyxDQUFDLENBQUM7UUFDTCxDQUFDLENBQUMsQ0FBQztJQUNMLENBQUMsRUFBRSxJQUFJLENBQUMsQ0FBQztBQUNYLENBQUM7QUF2Q0Qsa0RBdUNDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL3V0aWxzLnRzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQ6IEhUTUxFbGVtZW50KSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG59XG5cbmZ1bmN0aW9uIGhpZGVFbGVtZW50cyhcbiAgZXZlbnQ6IE1vdXNlRXZlbnQsXG4gIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICBvdGhlckVsZW1lbnQ/OiBIVE1MRWxlbWVudFtdLFxuKSB7XG4gIGlmIChcbiAgICAhZWxlbWVudC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkgJiZcbiAgICAhb3RoZXJFbGVtZW50LnNvbWUoZWwgPT4gZWwuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpKVxuICApIHtcbiAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgfVxufVxuXG4vLyBleHBvcnQgZnVuY3Rpb24gdW5sb2NrU2Nyb2xsKCkge1xuLy8gICBjb25zdCBzY3JvbGxZID0gZG9jdW1lbnQuYm9keS5zdHlsZS50b3A7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucG9zaXRpb24gPSAnJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS50b3AgPSAnJztcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5sZWZ0ID0gJyc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUucmlnaHQgPSAnJztcbi8vICAgd2luZG93LnNjcm9sbFRvKDAsIHBhcnNlSW50KHNjcm9sbFkgfHwgJzAnKSAqIC0xKTtcblxuLy8gICBjb25zb2xlLmxvZygndW5sb2NrIHNjcm9sbCcpO1xuLy8gfVxuXG4vLyBleHBvcnQgZnVuY3Rpb24gbG9ja1Njcm9sbCgpIHtcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5wb3NpdGlvbiA9ICdmaXhlZCc7XG4vLyAgIGRvY3VtZW50LmJvZHkuc3R5bGUudG9wID0gYC0ke3dpbmRvdy5zY3JvbGxZfXB4YDtcbi8vICAgZG9jdW1lbnQuYm9keS5zdHlsZS5sZWZ0ID0gJzAnO1xuLy8gICBkb2N1bWVudC5ib2R5LnN0eWxlLnJpZ2h0ID0gJzAnO1xuXG4vLyAgIGNvbnNvbGUubG9nKCdsb2NrIHNjcm9sbCcpO1xuLy8gfVxuXG5leHBvcnQgZnVuY3Rpb24gaGFuZGxlSGlkZUVsZW1lbnRzKFxuICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgb3RoZXJFbGVtZW50OiBIVE1MRWxlbWVudFtdID0gW10sXG4pIHtcbiAgZWxlbWVudC5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ21vdXNldXAnLCAoZXZlbnQ6IE1vdXNlRXZlbnQpID0+IHtcbiAgICBoaWRlRWxlbWVudHMoZXZlbnQsIGVsZW1lbnQsIG90aGVyRWxlbWVudCk7XG4gIH0pO1xuXG4gIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICBpZiAoZXZlbnQua2V5ID09PSAnRXNjYXBlJykge1xuICAgICAgYWRkSGlkZGVuQ2xhc3MoZWxlbWVudCk7XG4gICAgfVxuICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHJlc2l6ZUNoYXQoKSB7XG4gIGNvbnN0IGhlYWRlcjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcuaGVhZGVyJyk7XG4gIGNvbnN0IGNoYXRNYWluOiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWJvZHknKTtcbiAgY29uc3QgY2hhdEZvb3RlcjogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC1mb290ZXInKTtcbiAgY29uc3QgY2hhdFdpbmRvdzogSFRNTEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjY2hhdC13aW5kb3cnKTtcbiAgY29uc3Qgc2NyZWVuV2l0aDogbnVtYmVyID0gd2luZG93LmlubmVyV2lkdGg7XG4gIGNvbnN0IGhlYWRlckJvdHRvbTogbnVtYmVyID0gaGVhZGVyLm9mZnNldFRvcCArIGhlYWRlci5vZmZzZXRIZWlnaHQ7XG4gIGNvbnN0IGNoYXRXaW5kb3dUb3A6IG51bWJlciA9IGNoYXRXaW5kb3cub2Zmc2V0VG9wO1xuICBjb25zdCBmaXhlZE1pbkRpc3RhbmNlOiBudW1iZXIgPSAyNTA7XG4gIGNvbnN0IG1heENoYXRXaW5kb3dIZWlnaHQ6IG51bWJlciA9IDY1MDtcbiAgY29uc3QgYXZhaWxhYmxlU3BhY2U6IG51bWJlciA9IGNoYXRXaW5kb3dUb3AgLSBoZWFkZXJCb3R0b207XG5cbiAgaWYgKHNjcmVlbldpdGggPCA2NDApIHtcbiAgICBjaGF0TWFpbi5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDAlIC0gJHtjaGF0Rm9vdGVyLm9mZnNldEhlaWdodH1weClgO1xuICAgIGNvbnNvbGUubG9nKCdib2R5IGhpZGRlbicsIGRvY3VtZW50LmJvZHkpO1xuXG4gICAgZG9jdW1lbnQuYm9keS5zdHlsZS5vdmVyZmxvdyA9ICdoaWRkZW4nO1xuICAgIHJldHVybjtcbiAgfVxuXG4gIGlmICghaGVhZGVyIHx8ICFjaGF0V2luZG93KSByZXR1cm47XG5cbiAgaWYgKGF2YWlsYWJsZVNwYWNlIDwgZml4ZWRNaW5EaXN0YW5jZSkge1xuICAgIGNoYXRXaW5kb3cuc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwdmggLSAke2ZpeGVkTWluRGlzdGFuY2V9cHgpYDtcbiAgfVxuXG4gIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgIGlmIChjaGF0V2luZG93Lm9mZnNldEhlaWdodCA+IG1heENoYXRXaW5kb3dIZWlnaHQpIHtcbiAgICAgIGNoYXRXaW5kb3cuc3R5bGUuaGVpZ2h0ID0gYCR7bWF4Q2hhdFdpbmRvd0hlaWdodH1weGA7XG4gICAgfVxuICB9LCA1MDApO1xuXG4gIGlmIChjaGF0TWFpbiAmJiBjaGF0Rm9vdGVyKSB7XG4gICAgY2hhdE1haW4uc3R5bGUuaGVpZ2h0ID0gYGNhbGMoMTAwJSAtICR7Y2hhdEZvb3Rlci5vZmZzZXRIZWlnaHR9cHgpYDtcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gc2Nyb2xsRG93bihlbGVtZW50OiBIVE1MRGl2RWxlbWVudCkge1xuICBlbGVtZW50LnNjcm9sbFRvKHtcbiAgICB0b3A6IGVsZW1lbnQuc2Nyb2xsSGVpZ2h0LFxuICB9KTtcbn1cblxuY29uc3Qgc2Nyb2xsQW5pbWF0aW9uRHVyYXRpb24gPSAyMDA7XG5leHBvcnQgZnVuY3Rpb24gc2Nyb2xsRG93blNtb290aChlbGVtZW50OiBIVE1MRGl2RWxlbWVudCkge1xuICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICBlbGVtZW50LnNjcm9sbFRvKHtcbiAgICAgIHRvcDogZWxlbWVudC5zY3JvbGxIZWlnaHQsXG4gICAgICBiZWhhdmlvcjogJ3Ntb290aCcsXG4gICAgfSk7XG4gIH0sIHNjcm9sbEFuaW1hdGlvbkR1cmF0aW9uKTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHNvY2lhbE1lZGlhU2hhcmUoKSB7XG4gIGNvbnNvbGUubG9nKCdzb2NpYWxNZWRpYVNoYXJlJyk7XG4gIGNvbnN0IGZiU2hhcmVJY29ucyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXG4gICAgJy5mYi1zaGFyZScsXG4gICkgYXMgTm9kZUxpc3RPZjxIVE1MQW5jaG9yRWxlbWVudD47XG4gIGZiU2hhcmVJY29ucy5mb3JFYWNoKGZiSWNvbiA9PiB7XG4gICAgZmJJY29uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgY29uc3QgbGluayA9IGVuY29kZVVSSUNvbXBvbmVudCh3aW5kb3cubG9jYXRpb24uaHJlZik7XG4gICAgICBmYkljb24uaHJlZiA9IGBodHRwczovL3d3dy5mYWNlYm9vay5jb20vc2hhcmUucGhwP3U9JHtsaW5rfWA7XG4gICAgICBjb25zb2xlLmxvZyhmYkljb24uaHJlZik7XG4gICAgfSk7XG4gIH0pO1xuXG4gIGNvbnN0IGluc3RhU2hhcmVJY29ucyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXG4gICAgJy5pLXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgaW5zdGFTaGFyZUljb25zLmZvckVhY2goaW5zdGFJY29uID0+IHtcbiAgICBpbnN0YUljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGluc3RhSWNvbi5ocmVmID0gYGh0dHBzOi8vd3d3Lmluc3RhZ3JhbS5jb21gO1xuICAgICAgY29uc29sZS5sb2coaW5zdGFJY29uLmhyZWYpO1xuICAgIH0pO1xuICB9KTtcblxuICBjb25zdCB0d2l0dGVyU2hhcmVJY29ucyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXG4gICAgJy54LXNoYXJlJyxcbiAgKSBhcyBOb2RlTGlzdE9mPEhUTUxBbmNob3JFbGVtZW50PjtcbiAgdHdpdHRlclNoYXJlSWNvbnMuZm9yRWFjaCh0d2l0dGVySWNvbiA9PiB7XG4gICAgdHdpdHRlckljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgICBjb25zdCBsaW5rID0gZW5jb2RlVVJJQ29tcG9uZW50KHdpbmRvdy5sb2NhdGlvbi5ocmVmKTtcbiAgICAgIGNvbnN0IHRleHQgPSBlbmNvZGVVUklDb21wb25lbnQoXG4gICAgICAgICdDaGVjayBvdXQgY29vbCB0aWNrZXRzIGZvciBzYWxlIG9uIEZhblRpY2tldCcsXG4gICAgICApO1xuICAgICAgY29uc3QgaGFzaHRhZ3MgPSBlbmNvZGVVUklDb21wb25lbnQoJ3RpY2tldHMsZm9yc2FsZScpO1xuICAgICAgdHdpdHRlckljb24uaHJlZiA9IGBodHRwczovL3R3aXR0ZXIuY29tL3NoYXJlP3VybD0ke2xpbmt9JnRleHQ9JHt0ZXh0fSZoYXNodGFncz0ke2hhc2h0YWdzfWA7XG4gICAgICBjb25zb2xlLmxvZyh0d2l0dGVySWNvbi5ocmVmKTtcbiAgICB9KTtcbiAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBkaXNhYmxlRGF0ZUZsb3diaXRlKCkge1xuICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICBjb25zdCBhbGxEYXRlcyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5kYXRlcGlja2VyLWNlbGwnKTtcblxuICAgIGNvbnN0IGN1cnJlbnRNb250aCA9IG5ldyBEYXRlKCkuZ2V0TW9udGgoKTtcbiAgICBhbGxEYXRlcy5mb3JFYWNoKChkYXRlOiBIVE1MRGl2RWxlbWVudCkgPT4ge1xuICAgICAgY29uc3QgdGltZVN0YW1wID0gZGF0ZS5nZXRBdHRyaWJ1dGUoJ2RhdGEtZGF0ZScpO1xuICAgICAgY29uc3QgZGF0ZU1vbnRoID0gbmV3IERhdGUocGFyc2VJbnQodGltZVN0YW1wKSkuZ2V0TW9udGgoKTtcbiAgICAgIGRhdGVNb250aCAhPT0gY3VycmVudE1vbnRoXG4gICAgICAgID8gKGRhdGUuc3R5bGUuY29sb3IgPSAnIzk5YTFhMycpXG4gICAgICAgIDogKGRhdGUuc3R5bGUuY29sb3IgPSAnI2ZmZicpO1xuICAgIH0pO1xuXG4gICAgY29uc3QgY2FsZW5kYXJCdXR0b25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLm5leHQtYnRuLCAucHJldi1idG4nKTtcblxuICAgIGNhbGVuZGFyQnV0dG9ucy5mb3JFYWNoKChidXR0b246IEhUTUxCdXR0b25FbGVtZW50KSA9PiB7XG4gICAgICBidXR0b24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoZXZlbnQ6IEV2ZW50KSA9PiB7XG4gICAgICAgIGNvbnN0IHRhcmdldCA9IGV2ZW50LnRhcmdldCBhcyBIVE1MRWxlbWVudDtcbiAgICAgICAgY29uc3QgZGF0ZVBpY2tlciA9IHRhcmdldC5jbG9zZXN0KCcuZGF0ZXBpY2tlci1waWNrZXInKTtcblxuICAgICAgICBpZiAoIWRhdGVQaWNrZXIpIHJldHVybjtcblxuICAgICAgICBjb25zdCBtb250aFRpdGxlID0gZGF0ZVBpY2tlci5xdWVyeVNlbGVjdG9yKCcudmlldy1zd2l0Y2gnKTtcbiAgICAgICAgY29uc3QgbW9udGggPSBtb250aFRpdGxlLnRleHRDb250ZW50LnNwbGl0KCcgJylbMF07XG4gICAgICAgIGNvbnN0IHllYXIgPSBtb250aFRpdGxlLnRleHRDb250ZW50LnNwbGl0KCcgJylbMV07XG4gICAgICAgIGNvbnN0IGN1cnJlbnREYXRlID0gbmV3IERhdGUoYCR7bW9udGh9IDEsICR7eWVhcn1gKS5nZXRNb250aCgpO1xuICAgICAgICBjb25zdCBhbGxEYXRlcyA9IGRhdGVQaWNrZXIucXVlcnlTZWxlY3RvckFsbCgnLmRhdGVwaWNrZXItY2VsbCcpO1xuXG4gICAgICAgIGFsbERhdGVzLmZvckVhY2goKGRhdGU6IEhUTUxEaXZFbGVtZW50KSA9PiB7XG4gICAgICAgICAgY29uc3QgdGltZVN0YW1wID0gZGF0ZS5nZXRBdHRyaWJ1dGUoJ2RhdGEtZGF0ZScpO1xuICAgICAgICAgIGNvbnN0IGRhdGVNb250aCA9IG5ldyBEYXRlKHBhcnNlSW50KHRpbWVTdGFtcCkpLmdldE1vbnRoKCk7XG5cbiAgICAgICAgICBkYXRlTW9udGggIT09IGN1cnJlbnREYXRlXG4gICAgICAgICAgICA/IChkYXRlLnN0eWxlLmNvbG9yID0gJyM5OWExYTMnKVxuICAgICAgICAgICAgOiAoZGF0ZS5zdHlsZS5jb2xvciA9ICcjZmZmJyk7XG4gICAgICAgIH0pO1xuICAgICAgfSk7XG4gICAgfSk7XG4gIH0sIDEwMDApO1xufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9