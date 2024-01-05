/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!**********************!*\
  !*** ./src/admin.ts ***!
  \**********************/
console.log('file admin.ts loaded');
console.log('admin.ts loaded 5 row');
var chatIcon = document.querySelector('#chat-icon');
if (chatIcon) {
    chatIcon.classList.add('hidden');
}
var datesButton = document.querySelector('#event-dates');
var datesDropdown = document.querySelector('#event-dates-dropdown');
if (datesButton && datesDropdown) {
    datesButton.addEventListener('click', function () {
        datesDropdown.classList.toggle('hidden');
        window.addEventListener('mouseup', function (event) {
            if (!datesDropdown.contains(event.target)) {
                datesDropdown.classList.add('hidden');
            }
        });
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                datesDropdown.classList.add('hidden');
            }
        });
    });
}

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvYWRtaW4uanMiLCJtYXBwaW5ncyI6Ijs7Ozs7QUFBQSxPQUFPLENBQUMsR0FBRyxDQUFDLHNCQUFzQixDQUFDLENBQUM7QUFDcEMsT0FBTyxDQUFDLEdBQUcsQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDO0FBRXJDLElBQU0sUUFBUSxHQUFtQixRQUFRLENBQUMsYUFBYSxDQUFDLFlBQVksQ0FBQyxDQUFDO0FBQ3RFLElBQUksUUFBUSxFQUFFO0lBQ1osUUFBUSxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsUUFBUSxDQUFDLENBQUM7Q0FDbEM7QUFFRCxJQUFNLFdBQVcsR0FBbUIsUUFBUSxDQUFDLGFBQWEsQ0FBQyxjQUFjLENBQUMsQ0FBQztBQUMzRSxJQUFNLGFBQWEsR0FBc0IsUUFBUSxDQUFDLGFBQWEsQ0FDN0QsdUJBQXVCLENBQ3hCLENBQUM7QUFDRixJQUFJLFdBQVcsSUFBSSxhQUFhLEVBQUU7SUFDaEMsV0FBVyxDQUFDLGdCQUFnQixDQUFDLE9BQU8sRUFBRTtRQUNwQyxhQUFhLENBQUMsU0FBUyxDQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsQ0FBQztRQUV6QyxNQUFNLENBQUMsZ0JBQWdCLENBQUMsU0FBUyxFQUFFLFVBQUMsS0FBaUI7WUFDbkQsSUFBSSxDQUFDLGFBQWEsQ0FBQyxRQUFRLENBQUMsS0FBSyxDQUFDLE1BQWMsQ0FBQyxFQUFFO2dCQUNqRCxhQUFhLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQzthQUN2QztRQUNILENBQUMsQ0FBQyxDQUFDO1FBQ0gsUUFBUSxDQUFDLGdCQUFnQixDQUFDLFNBQVMsRUFBRSxVQUFVLEtBQUs7WUFDbEQsSUFBSSxLQUFLLENBQUMsR0FBRyxLQUFLLFFBQVEsRUFBRTtnQkFDMUIsYUFBYSxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsUUFBUSxDQUFDLENBQUM7YUFDdkM7UUFDSCxDQUFDLENBQUMsQ0FBQztJQUNMLENBQUMsQ0FBQyxDQUFDO0NBQ0oiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvYWRtaW4udHMiXSwic291cmNlc0NvbnRlbnQiOlsiY29uc29sZS5sb2coJ2ZpbGUgYWRtaW4udHMgbG9hZGVkJyk7XG5jb25zb2xlLmxvZygnYWRtaW4udHMgbG9hZGVkIDUgcm93Jyk7XG5cbmNvbnN0IGNoYXRJY29uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNjaGF0LWljb24nKTtcbmlmIChjaGF0SWNvbikge1xuICBjaGF0SWNvbi5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbn1cblxuY29uc3QgZGF0ZXNCdXR0b246IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2V2ZW50LWRhdGVzJyk7XG5jb25zdCBkYXRlc0Ryb3Bkb3duOiBIVE1MU2VsZWN0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICcjZXZlbnQtZGF0ZXMtZHJvcGRvd24nLFxuKTtcbmlmIChkYXRlc0J1dHRvbiAmJiBkYXRlc0Ryb3Bkb3duKSB7XG4gIGRhdGVzQnV0dG9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgIGRhdGVzRHJvcGRvd24uY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG5cbiAgICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsIChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICAgICAgaWYgKCFkYXRlc0Ryb3Bkb3duLmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSkge1xuICAgICAgICBkYXRlc0Ryb3Bkb3duLmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuICAgICAgfVxuICAgIH0pO1xuICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICAgIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICAgIGRhdGVzRHJvcGRvd24uY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG4gICAgICB9XG4gICAgfSk7XG4gIH0pO1xufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9