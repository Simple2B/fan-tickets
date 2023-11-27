/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!*********************!*\
  !*** ./src/home.ts ***!
  \*********************/
document.addEventListener('DOMContentLoaded', function () {
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
    // function to sticky header
    var header = document.querySelector('.header');
    var scrollPosition = 0.2 * window.innerHeight;
    window.addEventListener('scroll', function () {
        header.classList.toggle('header-sticky', window.scrollY > 0);
    });
    // function to show and hide the scroll to top button
    var scrollTopButton = document.querySelector('.footer-scroll-top');
    window.addEventListener('scroll', function () {
        if (window.scrollY > scrollPosition) {
            scrollTopButton.classList.remove('scroll-top-anchor-close');
            scrollTopButton.classList.add('scroll-top-anchor-open');
        }
        else {
            scrollTopButton.classList.remove('scroll-top-anchor-open');
            scrollTopButton.classList.add('scroll-top-anchor-close');
        }
    });
    scrollTopButton.addEventListener('click', function (e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth',
        });
    });
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvaG9tZS5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsRUFBRTtJQUM1QyxtRkFBbUY7SUFDbkYsSUFBTSxjQUFjLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDO0lBQ3ZFLElBQU0sVUFBVSxHQUFHLGNBQWMsQ0FBQyxnQkFBZ0IsQ0FBQyxhQUFhLENBQUMsQ0FBQztJQUNsRSxJQUFNLGVBQWUsR0FBRyxDQUFDLENBQUM7SUFDMUIsSUFBTSxnQkFBZ0IsR0FBRyxJQUFJLENBQUM7SUFFOUIsU0FBUyxlQUFlO1FBQ3RCLElBQU0sV0FBVyxHQUFHLE1BQU0sQ0FBQyxVQUFVLENBQUM7UUFDdEMsSUFBTSxlQUFlLEdBQ25CLFdBQVcsR0FBRyxnQkFBZ0IsQ0FBQyxDQUFDLENBQUMsZUFBZSxDQUFDLENBQUMsQ0FBQyxVQUFVLENBQUMsTUFBTSxDQUFDO1FBRXZFLFVBQVUsQ0FBQyxPQUFPLENBQUMsVUFBQyxJQUFJLEVBQUUsS0FBSztZQUM3QixLQUFLLEdBQUcsZUFBZTtnQkFDckIsQ0FBQyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQztnQkFDakMsQ0FBQyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBQ25DLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVELGVBQWUsRUFBRSxDQUFDO0lBQ2xCLE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxRQUFRLEVBQUUsZUFBZSxDQUFDLENBQUM7SUFFbkQsNEJBQTRCO0lBQzVCLElBQU0sTUFBTSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsU0FBUyxDQUFDLENBQUM7SUFDakQsSUFBTSxjQUFjLEdBQUcsR0FBRyxHQUFHLE1BQU0sQ0FBQyxXQUFXLENBQUM7SUFDaEQsTUFBTSxDQUFDLGdCQUFnQixDQUFDLFFBQVEsRUFBRTtRQUNoQyxNQUFNLENBQUMsU0FBUyxDQUFDLE1BQU0sQ0FBQyxlQUFlLEVBQUUsTUFBTSxDQUFDLE9BQU8sR0FBRyxDQUFDLENBQUMsQ0FBQztJQUMvRCxDQUFDLENBQUMsQ0FBQztJQUVILHFEQUFxRDtJQUNyRCxJQUFNLGVBQWUsR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLG9CQUFvQixDQUFDLENBQUM7SUFFckUsTUFBTSxDQUFDLGdCQUFnQixDQUFDLFFBQVEsRUFBRTtRQUNoQyxJQUFJLE1BQU0sQ0FBQyxPQUFPLEdBQUcsY0FBYyxFQUFFO1lBQ25DLGVBQWUsQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLHlCQUF5QixDQUFDLENBQUM7WUFDNUQsZUFBZSxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsd0JBQXdCLENBQUMsQ0FBQztTQUN6RDthQUFNO1lBQ0wsZUFBZSxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsd0JBQXdCLENBQUMsQ0FBQztZQUMzRCxlQUFlLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyx5QkFBeUIsQ0FBQyxDQUFDO1NBQzFEO0lBQ0gsQ0FBQyxDQUFDLENBQUM7SUFFSCxlQUFlLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFLFdBQUM7UUFDekMsQ0FBQyxDQUFDLGNBQWMsRUFBRSxDQUFDO1FBQ25CLE1BQU0sQ0FBQyxRQUFRLENBQUM7WUFDZCxHQUFHLEVBQUUsQ0FBQztZQUNOLFFBQVEsRUFBRSxRQUFRO1NBQ25CLENBQUMsQ0FBQztJQUNMLENBQUMsQ0FBQyxDQUFDO0FBQ0wsQ0FBQyxDQUFDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvaG9tZS50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgKCkgPT4ge1xuICAvLyBmdW5jdGlvbiB0byBsaW1pdCB0aGUgbnVtYmVyIG9mIGV2ZW50cyBzaG93biBvbiB0aGUgaG9tZSBwYWdlIGZvciBtb2JpbGUgZGV2aWNlc1xuICBjb25zdCBldmVudENvbnRhaW5lciA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNob21lLWV2ZW50LWNvbnRhaW5lcicpO1xuICBjb25zdCBldmVudEl0ZW1zID0gZXZlbnRDb250YWluZXIucXVlcnlTZWxlY3RvckFsbCgnLmV2ZW50LWl0ZW0nKTtcbiAgY29uc3QgbGltaXRFdmVudEl0ZW1zID0gNDtcbiAgY29uc3QgdG9nZ2xlU2NyZWVuU2l6ZSA9IDEwMjQ7XG5cbiAgZnVuY3Rpb24gc2hvd0xpbWl0RXZlbnRzKCkge1xuICAgIGNvbnN0IHNjcmVlbldpZHRoID0gd2luZG93LmlubmVyV2lkdGg7XG4gICAgY29uc3QgbWF4VmlzaWJsZUl0ZW1zID1cbiAgICAgIHNjcmVlbldpZHRoIDwgdG9nZ2xlU2NyZWVuU2l6ZSA/IGxpbWl0RXZlbnRJdGVtcyA6IGV2ZW50SXRlbXMubGVuZ3RoO1xuXG4gICAgZXZlbnRJdGVtcy5mb3JFYWNoKChpdGVtLCBpbmRleCkgPT4ge1xuICAgICAgaW5kZXggPCBtYXhWaXNpYmxlSXRlbXNcbiAgICAgICAgPyBpdGVtLmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpXG4gICAgICAgIDogaXRlbS5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgICB9KTtcbiAgfVxuXG4gIHNob3dMaW1pdEV2ZW50cygpO1xuICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcigncmVzaXplJywgc2hvd0xpbWl0RXZlbnRzKTtcblxuICAvLyBmdW5jdGlvbiB0byBzdGlja3kgaGVhZGVyXG4gIGNvbnN0IGhlYWRlciA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5oZWFkZXInKTtcbiAgY29uc3Qgc2Nyb2xsUG9zaXRpb24gPSAwLjIgKiB3aW5kb3cuaW5uZXJIZWlnaHQ7XG4gIHdpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdzY3JvbGwnLCAoKSA9PiB7XG4gICAgaGVhZGVyLmNsYXNzTGlzdC50b2dnbGUoJ2hlYWRlci1zdGlja3knLCB3aW5kb3cuc2Nyb2xsWSA+IDApO1xuICB9KTtcblxuICAvLyBmdW5jdGlvbiB0byBzaG93IGFuZCBoaWRlIHRoZSBzY3JvbGwgdG8gdG9wIGJ1dHRvblxuICBjb25zdCBzY3JvbGxUb3BCdXR0b24gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcuZm9vdGVyLXNjcm9sbC10b3AnKTtcblxuICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignc2Nyb2xsJywgKCkgPT4ge1xuICAgIGlmICh3aW5kb3cuc2Nyb2xsWSA+IHNjcm9sbFBvc2l0aW9uKSB7XG4gICAgICBzY3JvbGxUb3BCdXR0b24uY2xhc3NMaXN0LnJlbW92ZSgnc2Nyb2xsLXRvcC1hbmNob3ItY2xvc2UnKTtcbiAgICAgIHNjcm9sbFRvcEJ1dHRvbi5jbGFzc0xpc3QuYWRkKCdzY3JvbGwtdG9wLWFuY2hvci1vcGVuJyk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHNjcm9sbFRvcEJ1dHRvbi5jbGFzc0xpc3QucmVtb3ZlKCdzY3JvbGwtdG9wLWFuY2hvci1vcGVuJyk7XG4gICAgICBzY3JvbGxUb3BCdXR0b24uY2xhc3NMaXN0LmFkZCgnc2Nyb2xsLXRvcC1hbmNob3ItY2xvc2UnKTtcbiAgICB9XG4gIH0pO1xuXG4gIHNjcm9sbFRvcEJ1dHRvbi5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGUgPT4ge1xuICAgIGUucHJldmVudERlZmF1bHQoKTtcbiAgICB3aW5kb3cuc2Nyb2xsVG8oe1xuICAgICAgdG9wOiAwLFxuICAgICAgYmVoYXZpb3I6ICdzbW9vdGgnLFxuICAgIH0pO1xuICB9KTtcbn0pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9