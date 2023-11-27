/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!*********************!*\
  !*** ./src/home.ts ***!
  \*********************/
// function to limit the number of events shown on the home page for mobile devices
var eventContainer = document.querySelector('#home-event-container');
var eventItems = eventContainer.querySelectorAll('.event-item');
var limitEventItems = 4;
var toggleScreenSize = 1024;
function showLimitEvents() {
    var screenWidth = window.innerWidth;
    var maxVisibleItems = screenWidth < toggleScreenSize ? limitEventItems : eventItems.length;
    eventItems.forEach(function (item, index) {
        index < maxVisibleItems
            ? item.classList.remove('hidden')
            : item.classList.add('hidden');
    });
}
showLimitEvents();
window.addEventListener('resize', showLimitEvents);

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvaG9tZS5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLG1GQUFtRjtBQUNuRixJQUFNLGNBQWMsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLHVCQUF1QixDQUFDLENBQUM7QUFDdkUsSUFBTSxVQUFVLEdBQUcsY0FBYyxDQUFDLGdCQUFnQixDQUFDLGFBQWEsQ0FBQyxDQUFDO0FBQ2xFLElBQU0sZUFBZSxHQUFHLENBQUMsQ0FBQztBQUMxQixJQUFNLGdCQUFnQixHQUFHLElBQUksQ0FBQztBQUU5QixTQUFTLGVBQWU7SUFDdEIsSUFBTSxXQUFXLEdBQUcsTUFBTSxDQUFDLFVBQVUsQ0FBQztJQUN0QyxJQUFNLGVBQWUsR0FDbkIsV0FBVyxHQUFHLGdCQUFnQixDQUFDLENBQUMsQ0FBQyxlQUFlLENBQUMsQ0FBQyxDQUFDLFVBQVUsQ0FBQyxNQUFNLENBQUM7SUFFdkUsVUFBVSxDQUFDLE9BQU8sQ0FBQyxVQUFDLElBQUksRUFBRSxLQUFLO1FBQzdCLEtBQUssR0FBRyxlQUFlO1lBQ3JCLENBQUMsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUM7WUFDakMsQ0FBQyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxDQUFDO0lBQ25DLENBQUMsQ0FBQyxDQUFDO0FBQ0wsQ0FBQztBQUVELGVBQWUsRUFBRSxDQUFDO0FBQ2xCLE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxRQUFRLEVBQUUsZUFBZSxDQUFDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvaG9tZS50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBmdW5jdGlvbiB0byBsaW1pdCB0aGUgbnVtYmVyIG9mIGV2ZW50cyBzaG93biBvbiB0aGUgaG9tZSBwYWdlIGZvciBtb2JpbGUgZGV2aWNlc1xuY29uc3QgZXZlbnRDb250YWluZXIgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjaG9tZS1ldmVudC1jb250YWluZXInKTtcbmNvbnN0IGV2ZW50SXRlbXMgPSBldmVudENvbnRhaW5lci5xdWVyeVNlbGVjdG9yQWxsKCcuZXZlbnQtaXRlbScpO1xuY29uc3QgbGltaXRFdmVudEl0ZW1zID0gNDtcbmNvbnN0IHRvZ2dsZVNjcmVlblNpemUgPSAxMDI0O1xuXG5mdW5jdGlvbiBzaG93TGltaXRFdmVudHMoKSB7XG4gIGNvbnN0IHNjcmVlbldpZHRoID0gd2luZG93LmlubmVyV2lkdGg7XG4gIGNvbnN0IG1heFZpc2libGVJdGVtcyA9XG4gICAgc2NyZWVuV2lkdGggPCB0b2dnbGVTY3JlZW5TaXplID8gbGltaXRFdmVudEl0ZW1zIDogZXZlbnRJdGVtcy5sZW5ndGg7XG5cbiAgZXZlbnRJdGVtcy5mb3JFYWNoKChpdGVtLCBpbmRleCkgPT4ge1xuICAgIGluZGV4IDwgbWF4VmlzaWJsZUl0ZW1zXG4gICAgICA/IGl0ZW0uY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJylcbiAgICAgIDogaXRlbS5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgfSk7XG59XG5cbnNob3dMaW1pdEV2ZW50cygpO1xud2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ3Jlc2l6ZScsIHNob3dMaW1pdEV2ZW50cyk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=