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
    // var source = new EventSource(
    //   "{{ url_for('sse.stream', channel='room_unique_id') }}",
    // );
    // source.addEventListener(
    //   'greeting',
    //   function (event) {
    //     var data = JSON.parse(event.data);
    //     console.log(data);
    //   },
    //   false,
    // );
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvaG9tZS5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsRUFBRTtJQUM1QyxJQUFNLGNBQWMsR0FBbUIsUUFBUSxDQUFDLGFBQWEsQ0FDM0QsdUJBQXVCLENBQ3hCLENBQUM7SUFDRixJQUFNLFVBQVUsR0FBRyxjQUFjLENBQUMsZ0JBQWdCLENBQUMsYUFBYSxDQUFDLENBQUM7SUFDbEUsdUVBQXVFO0lBQ3ZFLElBQU0sZUFBZSxHQUFHLENBQUMsQ0FBQztJQUMxQixJQUFNLGdCQUFnQixHQUFHLElBQUksQ0FBQztJQUU5QixtRkFBbUY7SUFDbkYsU0FBUyxlQUFlO1FBQ3RCLElBQU0sV0FBVyxHQUFHLE1BQU0sQ0FBQyxVQUFVLENBQUM7UUFDdEMsSUFBTSxlQUFlLEdBQ25CLFdBQVcsR0FBRyxnQkFBZ0IsQ0FBQyxDQUFDLENBQUMsZUFBZSxDQUFDLENBQUMsQ0FBQyxVQUFVLENBQUMsTUFBTSxDQUFDO1FBRXZFLFVBQVUsQ0FBQyxPQUFPLENBQUMsVUFBQyxJQUFJLEVBQUUsS0FBSztZQUM3QixLQUFLLEdBQUcsZUFBZTtnQkFDckIsQ0FBQyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQztnQkFDakMsQ0FBQyxDQUFDLElBQUksQ0FBQyxTQUFTLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBQ25DLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVELGdEQUFnRDtJQUNoRCxTQUFTLGtCQUFrQjtRQUN6QixJQUFNLFVBQVUsR0FBcUIsUUFBUSxDQUFDLGFBQWEsQ0FDekQsd0JBQXdCLENBQ3pCLENBQUM7UUFDRixJQUFNLG9CQUFvQixHQUFtQixRQUFRLENBQUMsYUFBYSxDQUNqRSw4QkFBOEIsQ0FDL0IsQ0FBQztRQUNGLElBQU0sbUJBQW1CLEdBQ3ZCLG9CQUFvQixDQUFDLHFCQUFxQixFQUFFLENBQUMsSUFBSSxDQUFDO1FBQ3BELG1GQUFtRjtRQUNuRixJQUFNLHVCQUF1QixHQUFHLEVBQUUsQ0FBQztRQUVuQyxVQUFVLENBQUMsS0FBSyxDQUFDLEtBQUssR0FBRyxVQUN2QixtQkFBbUIsR0FBRyx1QkFBdUIsT0FDM0MsQ0FBQztJQUNQLENBQUM7SUFFRCxrQkFBa0IsRUFBRSxDQUFDO0lBQ3JCLGVBQWUsRUFBRSxDQUFDO0lBQ2xCLE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxRQUFRLEVBQUUsZUFBZSxDQUFDLENBQUM7SUFFbkQsMkRBQTJEO0lBQzNELHFEQUFxRDtJQUNyRCxJQUFNLGdCQUFnQixHQUFHLFFBQVEsQ0FBQyxnQkFBZ0IsQ0FBQyxtQkFBbUIsQ0FBQyxDQUFDO0lBRXhFLGdCQUFnQixDQUFDLE9BQU8sQ0FBQyxVQUFDLGVBQStCO1FBQ3ZELElBQUksaUJBQWlCLEdBQUcsQ0FBQyxDQUFDO1FBQzFCLElBQU0sT0FBTyxHQUFtQixlQUFlLENBQUMsUUFBUSxDQUFDO1FBQ3pELEtBQUssSUFBSSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsR0FBRyxPQUFPLENBQUMsTUFBTSxFQUFFLENBQUMsRUFBRSxFQUFFO1lBQ3ZDLGlCQUFpQixJQUFLLE9BQU8sQ0FBQyxDQUFDLENBQW9CLENBQUMsYUFBYSxDQUFDLENBQUM7U0FDcEU7UUFDRCxlQUFlLENBQUMsVUFBVSxHQUFHLENBQUMsaUJBQWlCLEdBQUcsTUFBTSxDQUFDLFVBQVUsQ0FBQyxHQUFHLENBQUMsQ0FBQztJQUMzRSxDQUFDLENBQUMsQ0FBQztJQUVILGdDQUFnQztJQUNoQyw2REFBNkQ7SUFDN0QsS0FBSztJQUNMLDJCQUEyQjtJQUMzQixnQkFBZ0I7SUFDaEIsdUJBQXVCO0lBQ3ZCLHlDQUF5QztJQUN6Qyx5QkFBeUI7SUFDekIsT0FBTztJQUNQLFdBQVc7SUFDWCxLQUFLO0FBQ1AsQ0FBQyxDQUFDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvaG9tZS50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgKCkgPT4ge1xuICBjb25zdCBldmVudENvbnRhaW5lcjogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjaG9tZS1ldmVudC1jb250YWluZXInLFxuICApO1xuICBjb25zdCBldmVudEl0ZW1zID0gZXZlbnRDb250YWluZXIucXVlcnlTZWxlY3RvckFsbCgnLmV2ZW50LWl0ZW0nKTtcbiAgLy8gbGltaXQgdGhlIG51bWJlciBvZiBldmVudHMgc2hvd24gb24gdGhlIGhvbWUgcGFnZSBmb3IgbW9iaWxlIGRldmljZXNcbiAgY29uc3QgbGltaXRFdmVudEl0ZW1zID0gNDtcbiAgY29uc3QgdG9nZ2xlU2NyZWVuU2l6ZSA9IDEwMjQ7XG5cbiAgLy8gZnVuY3Rpb24gdG8gbGltaXQgdGhlIG51bWJlciBvZiBldmVudHMgc2hvd24gb24gdGhlIGhvbWUgcGFnZSBmb3IgbW9iaWxlIGRldmljZXNcbiAgZnVuY3Rpb24gc2hvd0xpbWl0RXZlbnRzKCkge1xuICAgIGNvbnN0IHNjcmVlbldpZHRoID0gd2luZG93LmlubmVyV2lkdGg7XG4gICAgY29uc3QgbWF4VmlzaWJsZUl0ZW1zID1cbiAgICAgIHNjcmVlbldpZHRoIDwgdG9nZ2xlU2NyZWVuU2l6ZSA/IGxpbWl0RXZlbnRJdGVtcyA6IGV2ZW50SXRlbXMubGVuZ3RoO1xuXG4gICAgZXZlbnRJdGVtcy5mb3JFYWNoKChpdGVtLCBpbmRleCkgPT4ge1xuICAgICAgaW5kZXggPCBtYXhWaXNpYmxlSXRlbXNcbiAgICAgICAgPyBpdGVtLmNsYXNzTGlzdC5yZW1vdmUoJ2hpZGRlbicpXG4gICAgICAgIDogaXRlbS5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8vIGZ1bmN0aW9uIHRvIHNldCBjb3JyZWN0IHdpZHRoIGZvciBldmVudCBpbWFnZVxuICBmdW5jdGlvbiBzZXRFdmVudEltYWdlV2lkdGgoKSB7XG4gICAgY29uc3QgZXZlbnRJbWFnZTogSFRNTEltYWdlRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgICAnI2hvbWUtZXZlbnQtbGVmdC1pbWFnZScsXG4gICAgKTtcbiAgICBjb25zdCBldmVudEhlYWRlckNvbnRhaW5lcjogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICAgJyNob21lLWV2ZW50LWhlYWRlci1jb250YWluZXInLFxuICAgICk7XG4gICAgY29uc3QgZXZlbnRIZWFkZXJQb3NpdGlvbiA9XG4gICAgICBldmVudEhlYWRlckNvbnRhaW5lci5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKS5sZWZ0O1xuICAgIC8vIDYwIGlzIHRoZSBkaXN0YW5jZSBiZXR3ZWVuIHRoZSBldmVudCBpbWFnZSBhbmQgdGhlIGV2ZW50IGhlYWRlciBhcyBpbiB0aGUgZGVzaWduXG4gICAgY29uc3QgZGlzdGFuY2VCZXR3ZWVuRWxlbWVudHMgPSA2MDtcblxuICAgIGV2ZW50SW1hZ2Uuc3R5bGUud2lkdGggPSBgJHtcbiAgICAgIGV2ZW50SGVhZGVyUG9zaXRpb24gLSBkaXN0YW5jZUJldHdlZW5FbGVtZW50c1xuICAgIH1weGA7XG4gIH1cblxuICBzZXRFdmVudEltYWdlV2lkdGgoKTtcbiAgc2hvd0xpbWl0RXZlbnRzKCk7XG4gIHdpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdyZXNpemUnLCBzaG93TGltaXRFdmVudHMpO1xuXG4gIC8vIFRPRE86IGRlbGV0ZSBpdCBpZiBjbGllbnQgYWNjZXB0cyBzbGlkZXIgbm90IGZyb20gZGVzaWduXG4gIC8vIGZ1bmN0aW9uIHRvIHNldCBtaWRkbGUgc2Nyb2xsIHBvc2l0aW9uIGZvciBtb2R1bGVzXG4gIGNvbnN0IHNjcm9sbENvbnRhaW5lcnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcuc2Nyb2xsLXgtbW9kdWxlcycpO1xuXG4gIHNjcm9sbENvbnRhaW5lcnMuZm9yRWFjaCgoc2Nyb2xsQ29udGFpbmVyOiBIVE1MRGl2RWxlbWVudCkgPT4ge1xuICAgIGxldCB0b3RhbE1vZHVsZXNXaWR0aCA9IDA7XG4gICAgY29uc3QgbW9kdWxlczogSFRNTENvbGxlY3Rpb24gPSBzY3JvbGxDb250YWluZXIuY2hpbGRyZW47XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBtb2R1bGVzLmxlbmd0aDsgaSsrKSB7XG4gICAgICB0b3RhbE1vZHVsZXNXaWR0aCArPSAobW9kdWxlc1tpXSBhcyBIVE1MRGl2RWxlbWVudClbJ29mZnNldFdpZHRoJ107XG4gICAgfVxuICAgIHNjcm9sbENvbnRhaW5lci5zY3JvbGxMZWZ0ID0gKHRvdGFsTW9kdWxlc1dpZHRoIC0gd2luZG93LmlubmVyV2lkdGgpIC8gMjtcbiAgfSk7XG5cbiAgLy8gdmFyIHNvdXJjZSA9IG5ldyBFdmVudFNvdXJjZShcbiAgLy8gICBcInt7IHVybF9mb3IoJ3NzZS5zdHJlYW0nLCBjaGFubmVsPSdyb29tX3VuaXF1ZV9pZCcpIH19XCIsXG4gIC8vICk7XG4gIC8vIHNvdXJjZS5hZGRFdmVudExpc3RlbmVyKFxuICAvLyAgICdncmVldGluZycsXG4gIC8vICAgZnVuY3Rpb24gKGV2ZW50KSB7XG4gIC8vICAgICB2YXIgZGF0YSA9IEpTT04ucGFyc2UoZXZlbnQuZGF0YSk7XG4gIC8vICAgICBjb25zb2xlLmxvZyhkYXRhKTtcbiAgLy8gICB9LFxuICAvLyAgIGZhbHNlLFxuICAvLyApO1xufSk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=
