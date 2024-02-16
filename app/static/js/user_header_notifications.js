/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!******************************************!*\
  !*** ./src/user_header_notifications.ts ***!
  \******************************************/
document.addEventListener('DOMContentLoaded', function () {
    var userUuidInput = document.getElementById('user-uuid');
    var userUuid = userUuidInput.value;
    var channelQueryParameters = new URLSearchParams({
        channel: "notification:".concat(userUuid),
    });
    var sseEventSource = new EventSource('/sse'.concat("?", channelQueryParameters.toString()));
    var unreadNotificationCountDiv = document.getElementById('unread-notifications-count');
    var unreadNotificationCount = parseInt(unreadNotificationCountDiv.innerText);
    sseEventSource.onmessage = function (evt) {
        unreadNotificationCount += 1;
        unreadNotificationCountDiv.innerText = unreadNotificationCount.toString();
    };
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvdXNlcl9oZWFkZXJfbm90aWZpY2F0aW9ucy5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsRUFBRTtJQUMxQyxJQUFNLGFBQWEsR0FBRyxRQUFRLENBQUMsY0FBYyxDQUFDLFdBQVcsQ0FBcUIsQ0FBQztJQUMvRSxJQUFNLFFBQVEsR0FBRyxhQUFhLENBQUMsS0FBSyxDQUFDO0lBRXJDLElBQU0sc0JBQXNCLEdBQUcsSUFBSSxlQUFlLENBQUM7UUFDL0MsT0FBTyxFQUFFLGVBQWUsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDO0tBQzVDLENBQUMsQ0FBQztJQUVILElBQU0sY0FBYyxHQUFHLElBQUksV0FBVyxDQUFDLE1BQU0sQ0FBQyxNQUFNLENBQUMsR0FBRyxFQUFFLHNCQUFzQixDQUFDLFFBQVEsRUFBRSxDQUFDLENBQUMsQ0FBQztJQUM5RixJQUFNLDBCQUEwQixHQUFHLFFBQVEsQ0FBQyxjQUFjLENBQUMsNEJBQTRCLENBQW1CLENBQUM7SUFFM0csSUFBSSx1QkFBdUIsR0FBRyxRQUFRLENBQUMsMEJBQTBCLENBQUMsU0FBUyxDQUFDLENBQUM7SUFFN0UsY0FBYyxDQUFDLFNBQVMsR0FBRyxVQUFDLEdBQUc7UUFDM0IsdUJBQXVCLElBQUksQ0FBQyxDQUFDO1FBQzdCLDBCQUEwQixDQUFDLFNBQVMsR0FBRyx1QkFBdUIsQ0FBQyxRQUFRLEVBQUUsQ0FBQztJQUM5RSxDQUFDO0FBQ0wsQ0FBQyxDQUFDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvdXNlcl9oZWFkZXJfbm90aWZpY2F0aW9ucy50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgKCkgPT4ge1xuICAgIGNvbnN0IHVzZXJVdWlkSW5wdXQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndXNlci11dWlkJykgYXMgSFRNTElucHV0RWxlbWVudDtcbiAgICBjb25zdCB1c2VyVXVpZCA9IHVzZXJVdWlkSW5wdXQudmFsdWU7XG4gICAgXG4gICAgY29uc3QgY2hhbm5lbFF1ZXJ5UGFyYW1ldGVycyA9IG5ldyBVUkxTZWFyY2hQYXJhbXMoe1xuICAgICAgICBjaGFubmVsOiBcIm5vdGlmaWNhdGlvbjpcIi5jb25jYXQodXNlclV1aWQpLFxuICAgIH0pO1xuXG4gICAgY29uc3Qgc3NlRXZlbnRTb3VyY2UgPSBuZXcgRXZlbnRTb3VyY2UoJy9zc2UnLmNvbmNhdChcIj9cIiwgY2hhbm5lbFF1ZXJ5UGFyYW1ldGVycy50b1N0cmluZygpKSk7XG4gICAgY29uc3QgdW5yZWFkTm90aWZpY2F0aW9uQ291bnREaXYgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndW5yZWFkLW5vdGlmaWNhdGlvbnMtY291bnQnKSBhcyBIVE1MRGl2RWxlbWVudDtcblxuICAgIGxldCB1bnJlYWROb3RpZmljYXRpb25Db3VudCA9IHBhcnNlSW50KHVucmVhZE5vdGlmaWNhdGlvbkNvdW50RGl2LmlubmVyVGV4dCk7XG5cbiAgICBzc2VFdmVudFNvdXJjZS5vbm1lc3NhZ2UgPSAoZXZ0KSA9PiB7XG4gICAgICAgIHVucmVhZE5vdGlmaWNhdGlvbkNvdW50ICs9IDE7XG4gICAgICAgIHVucmVhZE5vdGlmaWNhdGlvbkNvdW50RGl2LmlubmVyVGV4dCA9IHVucmVhZE5vdGlmaWNhdGlvbkNvdW50LnRvU3RyaW5nKCk7XG4gICAgfVxufSk7Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9