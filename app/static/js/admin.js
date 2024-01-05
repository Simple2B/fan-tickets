/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!**********************!*\
  !*** ./src/admin.ts ***!
  \**********************/
console.log('file admin.ts loaded');
console.log('admin.ts loaded 5 row');
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvYWRtaW4uanMiLCJtYXBwaW5ncyI6Ijs7Ozs7QUFBQSxPQUFPLENBQUMsR0FBRyxDQUFDLHNCQUFzQixDQUFDLENBQUM7QUFDcEMsT0FBTyxDQUFDLEdBQUcsQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDO0FBRXJDLElBQU0sV0FBVyxHQUFtQixRQUFRLENBQUMsYUFBYSxDQUFDLGNBQWMsQ0FBQyxDQUFDO0FBQzNFLElBQU0sYUFBYSxHQUFzQixRQUFRLENBQUMsYUFBYSxDQUM3RCx1QkFBdUIsQ0FDeEIsQ0FBQztBQUNGLElBQUksV0FBVyxJQUFJLGFBQWEsRUFBRTtJQUNoQyxXQUFXLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1FBQ3BDLGFBQWEsQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBRXpDLE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxTQUFTLEVBQUUsVUFBQyxLQUFpQjtZQUNuRCxJQUFJLENBQUMsYUFBYSxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsTUFBYyxDQUFDLEVBQUU7Z0JBQ2pELGFBQWEsQ0FBQyxTQUFTLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxDQUFDO2FBQ3ZDO1FBQ0gsQ0FBQyxDQUFDLENBQUM7UUFDSCxRQUFRLENBQUMsZ0JBQWdCLENBQUMsU0FBUyxFQUFFLFVBQVUsS0FBSztZQUNsRCxJQUFJLEtBQUssQ0FBQyxHQUFHLEtBQUssUUFBUSxFQUFFO2dCQUMxQixhQUFhLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQzthQUN2QztRQUNILENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQyxDQUFDLENBQUM7Q0FDSiIsInNvdXJjZXMiOlsid2VicGFjazovL3N0YXRpYy8uL3NyYy9hZG1pbi50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJjb25zb2xlLmxvZygnZmlsZSBhZG1pbi50cyBsb2FkZWQnKTtcbmNvbnNvbGUubG9nKCdhZG1pbi50cyBsb2FkZWQgNSByb3cnKTtcblxuY29uc3QgZGF0ZXNCdXR0b246IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignI2V2ZW50LWRhdGVzJyk7XG5jb25zdCBkYXRlc0Ryb3Bkb3duOiBIVE1MU2VsZWN0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICcjZXZlbnQtZGF0ZXMtZHJvcGRvd24nLFxuKTtcbmlmIChkYXRlc0J1dHRvbiAmJiBkYXRlc0Ryb3Bkb3duKSB7XG4gIGRhdGVzQnV0dG9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgIGRhdGVzRHJvcGRvd24uY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG5cbiAgICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsIChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICAgICAgaWYgKCFkYXRlc0Ryb3Bkb3duLmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBOb2RlKSkge1xuICAgICAgICBkYXRlc0Ryb3Bkb3duLmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuICAgICAgfVxuICAgIH0pO1xuICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICAgIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICAgIGRhdGVzRHJvcGRvd24uY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG4gICAgICB9XG4gICAgfSk7XG4gIH0pO1xufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9