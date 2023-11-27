/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!*********************!*\
  !*** ./src/home.ts ***!
  \*********************/
document.addEventListener('DOMContentLoaded', function () {
    var eventContainer = document.querySelector('#home-event-container');
    var eventItems = eventContainer.querySelectorAll('.event-item');
    // limit the number of events shown on the home page for mobile devices
    var limitEventItems = 4;
    var toggleScreenSize = 1024;
    // function to limit the number of events shown on the home page for mobile devices
    function showLimitEvents() {
        var screenWidth = window.innerWidth;
        var maxVisibleItems = screenWidth < toggleScreenSize ? limitEventItems : eventItems.length;
        eventItems.forEach(function (item, index) {
            index < maxVisibleItems
                ? item.classList.remove('hidden')
                : item.classList.add('hidden');
        });
    }
    // function to set correct width for event image
    function setEventImageWidth() {
        var eventImage = document.querySelector('#home-event-left-image');
        var eventHeaderContainer = document.querySelector('#home-event-header-container');
        var eventHeaderPosition = eventHeaderContainer.getBoundingClientRect().left;
        // 60 is the distance between the event image and the event header as in the design
        var distanceBetweenElements = 60;
        eventImage.style.width = "".concat(eventHeaderPosition - distanceBetweenElements, "px");
    }
    setEventImageWidth();
    showLimitEvents();
    window.addEventListener('resize', showLimitEvents);
    // TODO: delete it if client accepts slider not from design
    // function to set middle scroll position for modules
    var scrollContainers = document.querySelectorAll('.scroll-x-modules');
    scrollContainers.forEach(function (scrollContainer) {
        var totalModulesWidth = 0;
        var modules = scrollContainer.children;
        for (var i = 0; i < modules.length; i++) {
            totalModulesWidth += modules[i]['offsetWidth'];
        }
        scrollContainer.scrollLeft = (totalModulesWidth - window.innerWidth) / 2;
    });
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvaG9tZS5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsRUFBRTtJQUM1QyxJQUFNLGNBQWMsR0FBbUIsUUFBUSxDQUFDLGFBQWEsQ0FDM0QsdUJBQXVCLENBQ3hCLENBQUM7SUFDRixJQUFNLFVBQVUsR0FBRyxjQUFjLENBQUMsZ0JBQWdCLENBQUMsYUFBYSxDQUFDLENBQUM7SUFDbEUsdUVBQXVFO0lBQ3ZFLElBQU0sZUFBZSxHQUFHLENBQUMsQ0FBQztJQUMxQixJQUFNLGdCQUFnQixHQUFHLElBQUksQ0FBQztJQUU5QixtRkFBbUY7SUFDbkYsU0FBUyxlQUFlO1FBQ3RCLElBQU0sV0FBVyxHQUFHLE1BQU0sQ0FBQyxVQUFVLENBQUM7UUFDdEMsSUFBTSxlQUFlLEdBQ25CLFdBQVcsR0FBRyxnQkFBZ0IsQ0FBQyxDQUFDLENBQUMsZUFBZSxDQUFDLENBQUMsQ0FBQyxVQUFVLENBQUMsTUFBTSxDQUFDO1FBRXZFLFVBQVUsQ0FBQyxPQUFPLENBQUMsVUFBQyxJQUFJLEVBQUUsS0FBSztZQUM3QixLQUFLLEdBQUcsZUFBZTtnQkFDckIsQ0FBQyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQztnQkFDakMsQ0FBQyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBQ25DLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVELGdEQUFnRDtJQUNoRCxTQUFTLGtCQUFrQjtRQUN6QixJQUFNLFVBQVUsR0FBcUIsUUFBUSxDQUFDLGFBQWEsQ0FDekQsd0JBQXdCLENBQ3pCLENBQUM7UUFDRixJQUFNLG9CQUFvQixHQUFtQixRQUFRLENBQUMsYUFBYSxDQUNqRSw4QkFBOEIsQ0FDL0IsQ0FBQztRQUNGLElBQU0sbUJBQW1CLEdBQ3ZCLG9CQUFvQixDQUFDLHFCQUFxQixFQUFFLENBQUMsSUFBSSxDQUFDO1FBQ3BELG1GQUFtRjtRQUNuRixJQUFNLHVCQUF1QixHQUFHLEVBQUUsQ0FBQztRQUVuQyxVQUFVLENBQUMsS0FBSyxDQUFDLEtBQUssR0FBRyxVQUN2QixtQkFBbUIsR0FBRyx1QkFBdUIsT0FDM0MsQ0FBQztJQUNQLENBQUM7SUFFRCxrQkFBa0IsRUFBRSxDQUFDO0lBQ3JCLGVBQWUsRUFBRSxDQUFDO0lBQ2xCLE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxRQUFRLEVBQUUsZUFBZSxDQUFDLENBQUM7SUFFbkQsMkRBQTJEO0lBQzNELHFEQUFxRDtJQUNyRCxJQUFNLGdCQUFnQixHQUFHLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxtQkFBbUIsQ0FBQyxDQUFDO0lBRXhFLGdCQUFnQixDQUFDLE9BQU8sQ0FBQyxVQUFDLGVBQStCO1FBQ3ZELElBQUksaUJBQWlCLEdBQUcsQ0FBQyxDQUFDO1FBQzFCLElBQU0sT0FBTyxHQUFtQixlQUFlLENBQUMsUUFBUSxDQUFDO1FBQ3pELEtBQUssSUFBSSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsR0FBRyxPQUFPLENBQUMsTUFBTSxFQUFFLENBQUMsRUFBRSxFQUFFO1lBQ3ZDLGlCQUFpQixJQUFLLE9BQU8sQ0FBQyxDQUFDLENBQW9CLENBQUMsYUFBYSxDQUFDLENBQUM7U0FDcEU7UUFDRCxlQUFlLENBQUMsVUFBVSxHQUFHLENBQUMsaUJBQWlCLEdBQUcsTUFBTSxDQUFDLFVBQVUsQ0FBQyxHQUFHLENBQUMsQ0FBQztJQUMzRSxDQUFDLENBQUMsQ0FBQztBQUNMLENBQUMsQ0FBQyxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL2hvbWUudHMiXSwic291cmNlc0NvbnRlbnQiOlsiZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsICgpID0+IHtcbiAgY29uc3QgZXZlbnRDb250YWluZXI6IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2hvbWUtZXZlbnQtY29udGFpbmVyJyxcbiAgKTtcbiAgY29uc3QgZXZlbnRJdGVtcyA9IGV2ZW50Q29udGFpbmVyLnF1ZXJ5U2VsZWN0b3JBbGwoJy5ldmVudC1pdGVtJyk7XG4gIC8vIGxpbWl0IHRoZSBudW1iZXIgb2YgZXZlbnRzIHNob3duIG9uIHRoZSBob21lIHBhZ2UgZm9yIG1vYmlsZSBkZXZpY2VzXG4gIGNvbnN0IGxpbWl0RXZlbnRJdGVtcyA9IDQ7XG4gIGNvbnN0IHRvZ2dsZVNjcmVlblNpemUgPSAxMDI0O1xuXG4gIC8vIGZ1bmN0aW9uIHRvIGxpbWl0IHRoZSBudW1iZXIgb2YgZXZlbnRzIHNob3duIG9uIHRoZSBob21lIHBhZ2UgZm9yIG1vYmlsZSBkZXZpY2VzXG4gIGZ1bmN0aW9uIHNob3dMaW1pdEV2ZW50cygpIHtcbiAgICBjb25zdCBzY3JlZW5XaWR0aCA9IHdpbmRvdy5pbm5lcldpZHRoO1xuICAgIGNvbnN0IG1heFZpc2libGVJdGVtcyA9XG4gICAgICBzY3JlZW5XaWR0aCA8IHRvZ2dsZVNjcmVlblNpemUgPyBsaW1pdEV2ZW50SXRlbXMgOiBldmVudEl0ZW1zLmxlbmd0aDtcblxuICAgIGV2ZW50SXRlbXMuZm9yRWFjaCgoaXRlbSwgaW5kZXgpID0+IHtcbiAgICAgIGluZGV4IDwgbWF4VmlzaWJsZUl0ZW1zXG4gICAgICAgID8gaXRlbS5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKVxuICAgICAgICA6IGl0ZW0uY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG4gICAgfSk7XG4gIH1cblxuICAvLyBmdW5jdGlvbiB0byBzZXQgY29ycmVjdCB3aWR0aCBmb3IgZXZlbnQgaW1hZ2VcbiAgZnVuY3Rpb24gc2V0RXZlbnRJbWFnZVdpZHRoKCkge1xuICAgIGNvbnN0IGV2ZW50SW1hZ2U6IEhUTUxJbWFnZUVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICAgJyNob21lLWV2ZW50LWxlZnQtaW1hZ2UnLFxuICAgICk7XG4gICAgY29uc3QgZXZlbnRIZWFkZXJDb250YWluZXI6IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAgICcjaG9tZS1ldmVudC1oZWFkZXItY29udGFpbmVyJyxcbiAgICApO1xuICAgIGNvbnN0IGV2ZW50SGVhZGVyUG9zaXRpb24gPVxuICAgICAgZXZlbnRIZWFkZXJDb250YWluZXIuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCkubGVmdDtcbiAgICAvLyA2MCBpcyB0aGUgZGlzdGFuY2UgYmV0d2VlbiB0aGUgZXZlbnQgaW1hZ2UgYW5kIHRoZSBldmVudCBoZWFkZXIgYXMgaW4gdGhlIGRlc2lnblxuICAgIGNvbnN0IGRpc3RhbmNlQmV0d2VlbkVsZW1lbnRzID0gNjA7XG5cbiAgICBldmVudEltYWdlLnN0eWxlLndpZHRoID0gYCR7XG4gICAgICBldmVudEhlYWRlclBvc2l0aW9uIC0gZGlzdGFuY2VCZXR3ZWVuRWxlbWVudHNcbiAgICB9cHhgO1xuICB9XG5cbiAgc2V0RXZlbnRJbWFnZVdpZHRoKCk7XG4gIHNob3dMaW1pdEV2ZW50cygpO1xuICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcigncmVzaXplJywgc2hvd0xpbWl0RXZlbnRzKTtcblxuICAvLyBUT0RPOiBkZWxldGUgaXQgaWYgY2xpZW50IGFjY2VwdHMgc2xpZGVyIG5vdCBmcm9tIGRlc2lnblxuICAvLyBmdW5jdGlvbiB0byBzZXQgbWlkZGxlIHNjcm9sbCBwb3NpdGlvbiBmb3IgbW9kdWxlc1xuICBjb25zdCBzY3JvbGxDb250YWluZXJzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLnNjcm9sbC14LW1vZHVsZXMnKTtcblxuICBzY3JvbGxDb250YWluZXJzLmZvckVhY2goKHNjcm9sbENvbnRhaW5lcjogSFRNTERpdkVsZW1lbnQpID0+IHtcbiAgICBsZXQgdG90YWxNb2R1bGVzV2lkdGggPSAwO1xuICAgIGNvbnN0IG1vZHVsZXM6IEhUTUxDb2xsZWN0aW9uID0gc2Nyb2xsQ29udGFpbmVyLmNoaWxkcmVuO1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgbW9kdWxlcy5sZW5ndGg7IGkrKykge1xuICAgICAgdG90YWxNb2R1bGVzV2lkdGggKz0gKG1vZHVsZXNbaV0gYXMgSFRNTERpdkVsZW1lbnQpWydvZmZzZXRXaWR0aCddO1xuICAgIH1cbiAgICBzY3JvbGxDb250YWluZXIuc2Nyb2xsTGVmdCA9ICh0b3RhbE1vZHVsZXNXaWR0aCAtIHdpbmRvdy5pbm5lcldpZHRoKSAvIDI7XG4gIH0pO1xufSk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=