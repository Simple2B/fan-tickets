/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!**********************!*\
  !*** ./src/event.ts ***!
  \**********************/
document.addEventListener('DOMContentLoaded', function () {
    var buttonFilterDate = document.querySelector('#events-filter-date-button');
    var buttonLocation = document.querySelector('#events-filter-location-button');
    var buttonCategories = document.querySelector('#events-filter-categories-button');
    var buttonDateApply = document.querySelector('#events-filter-date-apply-button');
    var dropdownFilterDate = document.querySelector('#events-filter-date-dropdown');
    var dropdownFilterLocation = document.querySelector('#events-filter-location-dropdown');
    var dropdownFilterCategories = document.querySelector('#events-filter-categories-dropdown');
    var statusFilterLocation = document.querySelector('#events-filter-location-status');
    var inputLocation = document.querySelector('#events-filter-location-input');
    var datalistLocation = document.querySelector('#events-filter-location-list');
    function addHiddenClass(element) {
        element.classList.add('hidden');
    }
    function handleHideEvents(event, element, otherElement) {
        if (!element.contains(event.target) &&
            !otherElement.some(function (el) { return el.contains(event.target); })) {
            addHiddenClass(element);
        }
    }
    function addHideEventsForElement(element, otherElement) {
        if (otherElement === void 0) { otherElement = []; }
        element.classList.toggle('hidden');
        window.addEventListener('mouseup', function (event) {
            handleHideEvents(event, element, otherElement);
        });
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                addHiddenClass(element);
            }
        });
    }
    buttonFilterDate.addEventListener('click', function () {
        var datePickers = document.querySelectorAll('.datepicker');
        var datePickerArray = Array.from(datePickers);
        addHideEventsForElement(dropdownFilterDate, datePickerArray);
    });
    buttonDateApply.addEventListener('click', function () {
        dropdownFilterDate.classList.toggle('hidden');
    });
    buttonLocation.addEventListener('click', function () {
        addHideEventsForElement(dropdownFilterLocation);
    });
    buttonCategories.addEventListener('click', function () {
        addHideEventsForElement(dropdownFilterCategories);
    });
    inputLocation.onfocus = function () {
        datalistLocation.style.display = 'block';
        inputLocation.style.borderRadius = '5px 5px 0 0';
    };
    var _loop_1 = function (index) {
        var option = datalistLocation.options[index];
        option.onclick = function () {
            inputLocation.value = option.value;
            statusFilterLocation.innerHTML = option.value;
            datalistLocation.style.display = 'none';
            inputLocation.style.borderRadius = '5px';
        };
    };
    for (var index in datalistLocation.options) {
        _loop_1(index);
    }
    inputLocation.oninput = function () {
        currentFocus = -1;
        var text = inputLocation.value.toUpperCase();
        for (var index in datalistLocation.options) {
            var option = datalistLocation.options[index];
            option.value.toUpperCase().indexOf(text) > -1
                ? (option.style.display = 'block')
                : (option.style.display = 'none');
        }
    };
    var currentFocus = -1;
    inputLocation.onkeydown = function (e) {
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(datalistLocation.options);
        }
        else if (e.keyCode == 38) {
            currentFocus--;
            addActive(datalistLocation.options);
        }
        else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (datalistLocation.options) {
                    datalistLocation.options[currentFocus].click();
                }
            }
        }
    };
    function addActive(x) {
        if (!x)
            return;
        false;
        removeActive(x);
        if (currentFocus >= x.length)
            currentFocus = 0;
        if (currentFocus < 0)
            currentFocus = x.length - 1;
        x[currentFocus].classList.add('active');
    }
    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove('active');
        }
    }
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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WUFBRSxZQUFZLEdBQUcsQ0FBQyxDQUFDLE1BQU0sR0FBRyxDQUFDLENBQUM7UUFDbEQsQ0FBQyxDQUFDLFlBQVksQ0FBQyxDQUFDLFNBQVMsQ0FBQyxHQUFHLENBQUMsUUFBUSxDQUFDLENBQUM7SUFDMUMsQ0FBQztJQUVELFNBQVMsWUFBWSxDQUFDLENBQXNDO1FBQzFELEtBQUssSUFBSSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsR0FBRyxDQUFDLENBQUMsTUFBTSxFQUFFLENBQUMsRUFBRSxFQUFFO1lBQ2pDLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQyxDQUFDO1NBQ2pDO0lBQ0gsQ0FBQztBQUNILENBQUMsQ0FBQyxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL2V2ZW50LnRzIl0sInNvdXJjZXNDb250ZW50IjpbImRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ0RPTUNvbnRlbnRMb2FkZWQnLCBmdW5jdGlvbiAoKSB7XG4gIGNvbnN0IGJ1dHRvbkZpbHRlckRhdGUgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcjZXZlbnRzLWZpbHRlci1kYXRlLWJ1dHRvbicpO1xuICBjb25zdCBidXR0b25Mb2NhdGlvbjogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1sb2NhdGlvbi1idXR0b24nLFxuICApO1xuICBjb25zdCBidXR0b25DYXRlZ29yaWVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItY2F0ZWdvcmllcy1idXR0b24nLFxuICApO1xuICBjb25zdCBidXR0b25EYXRlQXBwbHkgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1kYXRlLWFwcGx5LWJ1dHRvbicsXG4gICk7XG5cbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJEYXRlOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWRhdGUtZHJvcGRvd24nLFxuICApO1xuICBjb25zdCBkcm9wZG93bkZpbHRlckxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWRyb3Bkb3duJyxcbiAgKTtcbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWNhdGVnb3JpZXMtZHJvcGRvd24nLFxuICApO1xuXG4gIGNvbnN0IHN0YXR1c0ZpbHRlckxvY2F0aW9uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24tc3RhdHVzJyxcbiAgKTtcbiAgY29uc3QgaW5wdXRMb2NhdGlvbjogSFRNTElucHV0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWlucHV0JyxcbiAgKTtcbiAgY29uc3QgZGF0YWxpc3RMb2NhdGlvbjogSFRNTERhdGFMaXN0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWxpc3QnLFxuICApIGFzIEhUTUxEYXRhTGlzdEVsZW1lbnQ7XG5cbiAgZnVuY3Rpb24gYWRkSGlkZGVuQ2xhc3MoZWxlbWVudDogSFRNTEVsZW1lbnQpIHtcbiAgICBlbGVtZW50LmNsYXNzTGlzdC5hZGQoJ2hpZGRlbicpO1xuICB9XG5cbiAgZnVuY3Rpb24gaGFuZGxlSGlkZUV2ZW50cyhcbiAgICBldmVudDogTW91c2VFdmVudCxcbiAgICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgICBvdGhlckVsZW1lbnQ/OiBIVE1MRWxlbWVudFtdLFxuICApIHtcbiAgICBpZiAoXG4gICAgICAhZWxlbWVudC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkgJiZcbiAgICAgICFvdGhlckVsZW1lbnQuc29tZShlbCA9PiBlbC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkpXG4gICAgKSB7XG4gICAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgICB9XG4gIH1cblxuICBmdW5jdGlvbiBhZGRIaWRlRXZlbnRzRm9yRWxlbWVudChcbiAgICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgICBvdGhlckVsZW1lbnQ6IEhUTUxFbGVtZW50W10gPSBbXSxcbiAgKSB7XG4gICAgZWxlbWVudC5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsIChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICAgICAgaGFuZGxlSGlkZUV2ZW50cyhldmVudCwgZWxlbWVudCwgb3RoZXJFbGVtZW50KTtcbiAgICB9KTtcblxuICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICAgIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG5cbiAgYnV0dG9uRmlsdGVyRGF0ZS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHtcbiAgICBjb25zdCBkYXRlUGlja2VycyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5kYXRlcGlja2VyJyk7XG4gICAgY29uc3QgZGF0ZVBpY2tlckFycmF5OiBIVE1MRWxlbWVudFtdID0gQXJyYXkuZnJvbShcbiAgICAgIGRhdGVQaWNrZXJzLFxuICAgICkgYXMgSFRNTEVsZW1lbnRbXTtcblxuICAgIGFkZEhpZGVFdmVudHNGb3JFbGVtZW50KGRyb3Bkb3duRmlsdGVyRGF0ZSwgZGF0ZVBpY2tlckFycmF5KTtcbiAgfSk7XG5cbiAgYnV0dG9uRGF0ZUFwcGx5LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgIGRyb3Bkb3duRmlsdGVyRGF0ZS5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgfSk7XG5cbiAgYnV0dG9uTG9jYXRpb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgYWRkSGlkZUV2ZW50c0ZvckVsZW1lbnQoZHJvcGRvd25GaWx0ZXJMb2NhdGlvbik7XG4gIH0pO1xuXG4gIGJ1dHRvbkNhdGVnb3JpZXMuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7XG4gICAgYWRkSGlkZUV2ZW50c0ZvckVsZW1lbnQoZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzKTtcbiAgfSk7XG5cbiAgaW5wdXRMb2NhdGlvbi5vbmZvY3VzID0gZnVuY3Rpb24gKCkge1xuICAgIGRhdGFsaXN0TG9jYXRpb24uc3R5bGUuZGlzcGxheSA9ICdibG9jayc7XG4gICAgaW5wdXRMb2NhdGlvbi5zdHlsZS5ib3JkZXJSYWRpdXMgPSAnNXB4IDVweCAwIDAnO1xuICB9O1xuICBmb3IgKGxldCBpbmRleCBpbiBkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnMpIHtcbiAgICBjb25zdCBvcHRpb246IEhUTUxPcHRpb25FbGVtZW50ID0gZGF0YWxpc3RMb2NhdGlvbi5vcHRpb25zW2luZGV4XTtcbiAgICBvcHRpb24ub25jbGljayA9IGZ1bmN0aW9uICgpIHtcbiAgICAgIGlucHV0TG9jYXRpb24udmFsdWUgPSBvcHRpb24udmFsdWU7XG4gICAgICBzdGF0dXNGaWx0ZXJMb2NhdGlvbi5pbm5lckhUTUwgPSBvcHRpb24udmFsdWU7XG4gICAgICBkYXRhbGlzdExvY2F0aW9uLnN0eWxlLmRpc3BsYXkgPSAnbm9uZSc7XG4gICAgICBpbnB1dExvY2F0aW9uLnN0eWxlLmJvcmRlclJhZGl1cyA9ICc1cHgnO1xuICAgIH07XG4gIH1cblxuICBpbnB1dExvY2F0aW9uLm9uaW5wdXQgPSBmdW5jdGlvbiAoKSB7XG4gICAgY3VycmVudEZvY3VzID0gLTE7XG4gICAgY29uc3QgdGV4dCA9IGlucHV0TG9jYXRpb24udmFsdWUudG9VcHBlckNhc2UoKTtcbiAgICBmb3IgKGxldCBpbmRleCBpbiBkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnMpIHtcbiAgICAgIGNvbnN0IG9wdGlvbjogSFRNTE9wdGlvbkVsZW1lbnQgPSBkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnNbaW5kZXhdO1xuICAgICAgb3B0aW9uLnZhbHVlLnRvVXBwZXJDYXNlKCkuaW5kZXhPZih0ZXh0KSA+IC0xXG4gICAgICAgID8gKG9wdGlvbi5zdHlsZS5kaXNwbGF5ID0gJ2Jsb2NrJylcbiAgICAgICAgOiAob3B0aW9uLnN0eWxlLmRpc3BsYXkgPSAnbm9uZScpO1xuICAgIH1cbiAgfTtcblxuICBsZXQgY3VycmVudEZvY3VzID0gLTE7XG4gIGlucHV0TG9jYXRpb24ub25rZXlkb3duID0gZnVuY3Rpb24gKGUpIHtcbiAgICBpZiAoZS5rZXlDb2RlID09IDQwKSB7XG4gICAgICBjdXJyZW50Rm9jdXMrKztcbiAgICAgIGFkZEFjdGl2ZShkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnMpO1xuICAgIH0gZWxzZSBpZiAoZS5rZXlDb2RlID09IDM4KSB7XG4gICAgICBjdXJyZW50Rm9jdXMtLTtcbiAgICAgIGFkZEFjdGl2ZShkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnMpO1xuICAgIH0gZWxzZSBpZiAoZS5rZXlDb2RlID09IDEzKSB7XG4gICAgICBlLnByZXZlbnREZWZhdWx0KCk7XG4gICAgICBpZiAoY3VycmVudEZvY3VzID4gLTEpIHtcbiAgICAgICAgaWYgKGRhdGFsaXN0TG9jYXRpb24ub3B0aW9ucykge1xuICAgICAgICAgIGRhdGFsaXN0TG9jYXRpb24ub3B0aW9uc1tjdXJyZW50Rm9jdXNdLmNsaWNrKCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gIH07XG5cbiAgZnVuY3Rpb24gYWRkQWN0aXZlKHg6IEhUTUxDb2xsZWN0aW9uT2Y8SFRNTE9wdGlvbkVsZW1lbnQ+KSB7XG4gICAgaWYgKCF4KSByZXR1cm47XG5cbiAgICBmYWxzZTtcbiAgICByZW1vdmVBY3RpdmUoeCk7XG4gICAgaWYgKGN1cnJlbnRGb2N1cyA+PSB4Lmxlbmd0aCkgY3VycmVudEZvY3VzID0gMDtcbiAgICBpZiAoY3VycmVudEZvY3VzIDwgMCkgY3VycmVudEZvY3VzID0geC5sZW5ndGggLSAxO1xuICAgIHhbY3VycmVudEZvY3VzXS5jbGFzc0xpc3QuYWRkKCdhY3RpdmUnKTtcbiAgfVxuXG4gIGZ1bmN0aW9uIHJlbW92ZUFjdGl2ZSh4OiBIVE1MQ29sbGVjdGlvbk9mPEhUTUxPcHRpb25FbGVtZW50Pikge1xuICAgIGZvciAobGV0IGkgPSAwOyBpIDwgeC5sZW5ndGg7IGkrKykge1xuICAgICAgeFtpXS5jbGFzc0xpc3QucmVtb3ZlKCdhY3RpdmUnKTtcbiAgICB9XG4gIH1cbn0pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9