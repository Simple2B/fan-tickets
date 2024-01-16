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

})();

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvdXRpbHMuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7O0FBQUEsU0FBUyxjQUFjLENBQUMsT0FBb0I7SUFDMUMsT0FBTyxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsUUFBUSxDQUFDLENBQUM7QUFDbEMsQ0FBQztBQUVELFNBQVMsWUFBWSxDQUNuQixLQUFpQixFQUNqQixPQUFvQixFQUNwQixZQUE0QjtJQUU1QixJQUNFLENBQUMsT0FBTyxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsTUFBYyxDQUFDO1FBQ3ZDLENBQUMsWUFBWSxDQUFDLElBQUksQ0FBQyxZQUFFLElBQUksU0FBRSxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsTUFBYyxDQUFDLEVBQWpDLENBQWlDLENBQUMsRUFDM0Q7UUFDQSxjQUFjLENBQUMsT0FBTyxDQUFDLENBQUM7S0FDekI7QUFDSCxDQUFDO0FBRUQsU0FBZ0Isa0JBQWtCLENBQ2hDLE9BQW9CLEVBQ3BCLFlBQWdDO0lBQWhDLGdEQUFnQztJQUVoQyxPQUFPLENBQUMsU0FBUyxDQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsQ0FBQztJQUNuQyxNQUFNLENBQUMsZ0JBQWdCLENBQUMsU0FBUyxFQUFFLFVBQUMsS0FBaUI7UUFDbkQsWUFBWSxDQUFDLEtBQUssRUFBRSxPQUFPLEVBQUUsWUFBWSxDQUFDLENBQUM7SUFDN0MsQ0FBQyxDQUFDLENBQUM7SUFFSCxRQUFRLENBQUMsZ0JBQWdCLENBQUMsU0FBUyxFQUFFLFVBQVUsS0FBSztRQUNsRCxJQUFJLEtBQUssQ0FBQyxHQUFHLEtBQUssUUFBUSxFQUFFO1lBQzFCLGNBQWMsQ0FBQyxPQUFPLENBQUMsQ0FBQztTQUN6QjtJQUNILENBQUMsQ0FBQyxDQUFDO0FBQ0wsQ0FBQztBQWRELGdEQWNDO0FBRUQsU0FBZ0IsVUFBVTtJQUN4QixJQUFNLE1BQU0sR0FBZ0IsUUFBUSxDQUFDLGFBQWEsQ0FBQyxTQUFTLENBQUMsQ0FBQztJQUM5RCxJQUFNLFVBQVUsR0FBZ0IsUUFBUSxDQUFDLGFBQWEsQ0FBQyxjQUFjLENBQUMsQ0FBQztJQUV2RSxJQUFJLENBQUMsTUFBTSxJQUFJLENBQUMsVUFBVTtRQUFFLE9BQU87SUFFbkMsSUFBTSxZQUFZLEdBQVcsTUFBTSxDQUFDLFNBQVMsR0FBRyxNQUFNLENBQUMsWUFBWSxDQUFDO0lBQ3BFLElBQU0sYUFBYSxHQUFXLFVBQVUsQ0FBQyxTQUFTLENBQUM7SUFDbkQsSUFBTSxnQkFBZ0IsR0FBVyxHQUFHLENBQUM7SUFDckMsSUFBTSxtQkFBbUIsR0FBVyxHQUFHLENBQUM7SUFDeEMsSUFBTSxjQUFjLEdBQVcsYUFBYSxHQUFHLFlBQVksQ0FBQztJQUU1RCxJQUFJLGNBQWMsR0FBRyxnQkFBZ0IsRUFBRTtRQUNyQyxVQUFVLENBQUMsS0FBSyxDQUFDLE1BQU0sR0FBRyx1QkFBZ0IsZ0JBQWdCLFFBQUssQ0FBQztLQUNqRTtJQUNELElBQUksVUFBVSxDQUFDLFlBQVksR0FBRyxtQkFBbUIsRUFBRTtRQUNqRCxVQUFVLENBQUMsS0FBSyxDQUFDLE1BQU0sR0FBRyxVQUFHLG1CQUFtQixPQUFJLENBQUM7S0FDdEQ7QUFDSCxDQUFDO0FBbEJELGdDQWtCQyIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy91dGlscy50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiBhZGRIaWRkZW5DbGFzcyhlbGVtZW50OiBIVE1MRWxlbWVudCkge1xuICBlbGVtZW50LmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xufVxuXG5mdW5jdGlvbiBoaWRlRWxlbWVudHMoXG4gIGV2ZW50OiBNb3VzZUV2ZW50LFxuICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgb3RoZXJFbGVtZW50PzogSFRNTEVsZW1lbnRbXSxcbikge1xuICBpZiAoXG4gICAgIWVsZW1lbnQuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIE5vZGUpICYmXG4gICAgIW90aGVyRWxlbWVudC5zb21lKGVsID0+IGVsLmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSlcbiAgKSB7XG4gICAgYWRkSGlkZGVuQ2xhc3MoZWxlbWVudCk7XG4gIH1cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGhhbmRsZUhpZGVFbGVtZW50cyhcbiAgZWxlbWVudDogSFRNTEVsZW1lbnQsXG4gIG90aGVyRWxlbWVudDogSFRNTEVsZW1lbnRbXSA9IFtdLFxuKSB7XG4gIGVsZW1lbnQuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gIHdpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdtb3VzZXVwJywgKGV2ZW50OiBNb3VzZUV2ZW50KSA9PiB7XG4gICAgaGlkZUVsZW1lbnRzKGV2ZW50LCBlbGVtZW50LCBvdGhlckVsZW1lbnQpO1xuICB9KTtcblxuICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdrZXlkb3duJywgZnVuY3Rpb24gKGV2ZW50KSB7XG4gICAgaWYgKGV2ZW50LmtleSA9PT0gJ0VzY2FwZScpIHtcbiAgICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICAgIH1cbiAgfSk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZXNpemVDaGF0KCkge1xuICBjb25zdCBoZWFkZXI6IEhUTUxFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignLmhlYWRlcicpO1xuICBjb25zdCBjaGF0V2luZG93OiBIVE1MRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LXdpbmRvdycpO1xuXG4gIGlmICghaGVhZGVyIHx8ICFjaGF0V2luZG93KSByZXR1cm47XG5cbiAgY29uc3QgaGVhZGVyQm90dG9tOiBudW1iZXIgPSBoZWFkZXIub2Zmc2V0VG9wICsgaGVhZGVyLm9mZnNldEhlaWdodDtcbiAgY29uc3QgY2hhdFdpbmRvd1RvcDogbnVtYmVyID0gY2hhdFdpbmRvdy5vZmZzZXRUb3A7XG4gIGNvbnN0IGZpeGVkTWluRGlzdGFuY2U6IG51bWJlciA9IDIyMDtcbiAgY29uc3QgbWF4Q2hhdFdpbmRvd0hlaWdodDogbnVtYmVyID0gNjUwO1xuICBjb25zdCBhdmFpbGFibGVTcGFjZTogbnVtYmVyID0gY2hhdFdpbmRvd1RvcCAtIGhlYWRlckJvdHRvbTtcblxuICBpZiAoYXZhaWxhYmxlU3BhY2UgPCBmaXhlZE1pbkRpc3RhbmNlKSB7XG4gICAgY2hhdFdpbmRvdy5zdHlsZS5oZWlnaHQgPSBgY2FsYygxMDB2aCAtICR7Zml4ZWRNaW5EaXN0YW5jZX1weClgO1xuICB9XG4gIGlmIChjaGF0V2luZG93Lm9mZnNldEhlaWdodCA+IG1heENoYXRXaW5kb3dIZWlnaHQpIHtcbiAgICBjaGF0V2luZG93LnN0eWxlLmhlaWdodCA9IGAke21heENoYXRXaW5kb3dIZWlnaHR9cHhgO1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=