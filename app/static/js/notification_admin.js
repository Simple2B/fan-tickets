/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it uses a non-standard name for the exports (exports).
(() => {
var exports = __webpack_exports__;
/*!************************************************!*\
  !*** ./src/notification/notification_admin.ts ***!
  \************************************************/

Object.defineProperty(exports, "__esModule", ({ value: true }));
document.addEventListener('DOMContentLoaded', function () {
    var channelQueryParameters = new URLSearchParams({
        channel: "admin",
    });
    var eventSource = new EventSource('/sse'.concat("?", channelQueryParameters.toString()));
    var newNotificationInput = document.querySelector('input[name="notification_uuid"]');
    eventSource.onmessage = function (evt) {
        var notificationData = JSON.parse(evt.data);
        newNotificationInput.value = notificationData.uuid;
        htmx.trigger('#notification_loader', "load_notification");
    };
});

})();

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvbm90aWZpY2F0aW9uX2FkbWluLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7O0FBRUEsUUFBUSxDQUFDLGdCQUFnQixDQUFDLGtCQUFrQixFQUFFO0lBQzFDLElBQU0sc0JBQXNCLEdBQUcsSUFBSSxlQUFlLENBQUM7UUFDL0MsT0FBTyxFQUFFLE9BQU87S0FDbkIsQ0FBQyxDQUFDO0lBRUgsSUFBTSxXQUFXLEdBQUcsSUFBSSxXQUFXLENBQUMsTUFBTSxDQUFDLE1BQU0sQ0FBQyxHQUFHLEVBQUUsc0JBQXNCLENBQUMsUUFBUSxFQUFFLENBQUMsQ0FBQyxDQUFDO0lBRTNGLElBQU0sb0JBQW9CLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyxpQ0FBaUMsQ0FBcUIsQ0FBQztJQUMzRyxXQUFXLENBQUMsU0FBUyxHQUFHLFVBQUMsR0FBRztRQUN4QixJQUFNLGdCQUFnQixHQUFpQixJQUFJLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUM1RCxvQkFBb0IsQ0FBQyxLQUFLLEdBQUcsZ0JBQWdCLENBQUMsSUFBSSxDQUFDO1FBQ25ELElBQUksQ0FBQyxPQUFPLENBQUMsc0JBQXNCLEVBQUUsbUJBQW1CLENBQUMsQ0FBQztJQUM5RCxDQUFDO0FBQ0wsQ0FBQyxDQUFDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvbm90aWZpY2F0aW9uL25vdGlmaWNhdGlvbl9hZG1pbi50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgeyBOb3RpZmljYXRpb24gfSBmcm9tICcuL3NjaGVtYSc7XG5cbmRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCAoKSA9PiB7XG4gICAgY29uc3QgY2hhbm5lbFF1ZXJ5UGFyYW1ldGVycyA9IG5ldyBVUkxTZWFyY2hQYXJhbXMoe1xuICAgICAgICBjaGFubmVsOiBcImFkbWluXCIsXG4gICAgfSk7XG5cbiAgICBjb25zdCBldmVudFNvdXJjZSA9IG5ldyBFdmVudFNvdXJjZSgnL3NzZScuY29uY2F0KFwiP1wiLCBjaGFubmVsUXVlcnlQYXJhbWV0ZXJzLnRvU3RyaW5nKCkpKTtcblxuICAgIGNvbnN0IG5ld05vdGlmaWNhdGlvbklucHV0ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignaW5wdXRbbmFtZT1cIm5vdGlmaWNhdGlvbl91dWlkXCJdJykgYXMgSFRNTElucHV0RWxlbWVudDtcbiAgICBldmVudFNvdXJjZS5vbm1lc3NhZ2UgPSAoZXZ0KSA9PiB7XG4gICAgICAgIGNvbnN0IG5vdGlmaWNhdGlvbkRhdGE6IE5vdGlmaWNhdGlvbiA9IEpTT04ucGFyc2UoZXZ0LmRhdGEpO1xuICAgICAgICBuZXdOb3RpZmljYXRpb25JbnB1dC52YWx1ZSA9IG5vdGlmaWNhdGlvbkRhdGEudXVpZDtcbiAgICAgICAgaHRteC50cmlnZ2VyKCcjbm90aWZpY2F0aW9uX2xvYWRlcicsIFwibG9hZF9ub3RpZmljYXRpb25cIik7XG4gICAgfVxufSk7Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9