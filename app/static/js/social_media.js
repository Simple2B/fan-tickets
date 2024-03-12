/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!*****************************!*\
  !*** ./src/social_media.ts ***!
  \*****************************/
console.log('socialMedia.ts');
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

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvc29jaWFsX21lZGlhLmpzIiwibWFwcGluZ3MiOiI7Ozs7O0FBQUEsT0FBTyxDQUFDLEdBQUcsQ0FBQyxnQkFBZ0IsQ0FBQyxDQUFDO0FBQzlCLElBQU0sWUFBWSxHQUFHLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FDNUMsV0FBVyxDQUNxQixDQUFDO0FBQ25DLFlBQVksQ0FBQyxPQUFPLENBQUMsZ0JBQU07SUFDekIsTUFBTSxDQUFDLGdCQUFnQixDQUFDLE9BQU8sRUFBRTtRQUMvQixJQUFNLElBQUksR0FBRyxrQkFBa0IsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLElBQUksQ0FBQyxDQUFDO1FBQ3RELE1BQU0sQ0FBQyxJQUFJLEdBQUcsK0NBQXdDLElBQUksQ0FBRSxDQUFDO1FBQzdELE9BQU8sQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQzNCLENBQUMsQ0FBQyxDQUFDO0FBQ0wsQ0FBQyxDQUFDLENBQUM7QUFFSCxJQUFNLGVBQWUsR0FBRyxRQUFRLENBQUMsZ0JBQWdCLENBQy9DLFVBQVUsQ0FDc0IsQ0FBQztBQUNuQyxlQUFlLENBQUMsT0FBTyxDQUFDLG1CQUFTO0lBQy9CLFNBQVMsQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7UUFDbEMsSUFBTSxJQUFJLEdBQUcsa0JBQWtCLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUN0RCxTQUFTLENBQUMsSUFBSSxHQUFHLDJCQUEyQixDQUFDO1FBQzdDLE9BQU8sQ0FBQyxHQUFHLENBQUMsU0FBUyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQzlCLENBQUMsQ0FBQyxDQUFDO0FBQ0wsQ0FBQyxDQUFDLENBQUM7QUFFSCxJQUFNLGlCQUFpQixHQUFHLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FDakQsVUFBVSxDQUNzQixDQUFDO0FBQ25DLGlCQUFpQixDQUFDLE9BQU8sQ0FBQyxxQkFBVztJQUNuQyxXQUFXLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1FBQ3BDLElBQU0sSUFBSSxHQUFHLGtCQUFrQixDQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsSUFBSSxDQUFDLENBQUM7UUFDdEQsSUFBTSxJQUFJLEdBQUcsa0JBQWtCLENBQzdCLDhDQUE4QyxDQUMvQyxDQUFDO1FBQ0YsSUFBTSxRQUFRLEdBQUcsa0JBQWtCLENBQUMsaUJBQWlCLENBQUMsQ0FBQztRQUN2RCxXQUFXLENBQUMsSUFBSSxHQUFHLHdDQUFpQyxJQUFJLG1CQUFTLElBQUksdUJBQWEsUUFBUSxDQUFFLENBQUM7UUFDN0YsT0FBTyxDQUFDLEdBQUcsQ0FBQyxXQUFXLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDaEMsQ0FBQyxDQUFDLENBQUM7QUFDTCxDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy9zb2NpYWxfbWVkaWEudHMiXSwic291cmNlc0NvbnRlbnQiOlsiY29uc29sZS5sb2coJ3NvY2lhbE1lZGlhLnRzJyk7XG5jb25zdCBmYlNoYXJlSWNvbnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKFxuICAnLmZiLXNoYXJlJyxcbikgYXMgTm9kZUxpc3RPZjxIVE1MQW5jaG9yRWxlbWVudD47XG5mYlNoYXJlSWNvbnMuZm9yRWFjaChmYkljb24gPT4ge1xuICBmYkljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgY29uc3QgbGluayA9IGVuY29kZVVSSUNvbXBvbmVudCh3aW5kb3cubG9jYXRpb24uaHJlZik7XG4gICAgZmJJY29uLmhyZWYgPSBgaHR0cHM6Ly93d3cuZmFjZWJvb2suY29tL3NoYXJlLnBocD91PSR7bGlua31gO1xuICAgIGNvbnNvbGUubG9nKGZiSWNvbi5ocmVmKTtcbiAgfSk7XG59KTtcblxuY29uc3QgaW5zdGFTaGFyZUljb25zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcbiAgJy5pLXNoYXJlJyxcbikgYXMgTm9kZUxpc3RPZjxIVE1MQW5jaG9yRWxlbWVudD47XG5pbnN0YVNoYXJlSWNvbnMuZm9yRWFjaChpbnN0YUljb24gPT4ge1xuICBpbnN0YUljb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgY29uc3QgbGluayA9IGVuY29kZVVSSUNvbXBvbmVudCh3aW5kb3cubG9jYXRpb24uaHJlZik7XG4gICAgaW5zdGFJY29uLmhyZWYgPSBgaHR0cHM6Ly93d3cuaW5zdGFncmFtLmNvbWA7XG4gICAgY29uc29sZS5sb2coaW5zdGFJY29uLmhyZWYpO1xuICB9KTtcbn0pO1xuXG5jb25zdCB0d2l0dGVyU2hhcmVJY29ucyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoXG4gICcueC1zaGFyZScsXG4pIGFzIE5vZGVMaXN0T2Y8SFRNTEFuY2hvckVsZW1lbnQ+O1xudHdpdHRlclNoYXJlSWNvbnMuZm9yRWFjaCh0d2l0dGVySWNvbiA9PiB7XG4gIHR3aXR0ZXJJY29uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgIGNvbnN0IGxpbmsgPSBlbmNvZGVVUklDb21wb25lbnQod2luZG93LmxvY2F0aW9uLmhyZWYpO1xuICAgIGNvbnN0IHRleHQgPSBlbmNvZGVVUklDb21wb25lbnQoXG4gICAgICAnQ2hlY2sgb3V0IGNvb2wgdGlja2V0cyBmb3Igc2FsZSBvbiBGYW5UaWNrZXQnLFxuICAgICk7XG4gICAgY29uc3QgaGFzaHRhZ3MgPSBlbmNvZGVVUklDb21wb25lbnQoJ3RpY2tldHMsZm9yc2FsZScpO1xuICAgIHR3aXR0ZXJJY29uLmhyZWYgPSBgaHR0cHM6Ly90d2l0dGVyLmNvbS9zaGFyZT91cmw9JHtsaW5rfSZ0ZXh0PSR7dGV4dH0maGFzaHRhZ3M9JHtoYXNodGFnc31gO1xuICAgIGNvbnNvbGUubG9nKHR3aXR0ZXJJY29uLmhyZWYpO1xuICB9KTtcbn0pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9