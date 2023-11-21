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
        console.log(otherElement);
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
            if (option.value.toUpperCase().indexOf(text) > -1) {
                option.style.display = 'block';
            }
            else {
                option.style.display = 'none';
            }
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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LENBQUM7UUFDL0MsSUFBSSxZQUFZLEdBQUcsQ0FBQztZQUFFLFlBQVksR0FBRyxDQUFDLENBQUMsTUFBTSxHQUFHLENBQUMsQ0FBQztRQUNsRCxDQUFDLENBQUMsWUFBWSxDQUFDLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQztJQUMxQyxDQUFDO0lBRUQsU0FBUyxZQUFZLENBQUMsQ0FBc0M7UUFDMUQsS0FBSyxJQUFJLENBQUMsR0FBRyxDQUFDLEVBQUUsQ0FBQyxHQUFHLENBQUMsQ0FBQyxNQUFNLEVBQUUsQ0FBQyxFQUFFLEVBQUU7WUFDakMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUM7U0FDakM7SUFDSCxDQUFDO0FBQ0gsQ0FBQyxDQUFDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvZXZlbnQudHMiXSwic291cmNlc0NvbnRlbnQiOlsiZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsIGZ1bmN0aW9uICgpIHtcbiAgY29uc3QgYnV0dG9uRmlsdGVyRGF0ZSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNldmVudHMtZmlsdGVyLWRhdGUtYnV0dG9uJyk7XG4gIGNvbnN0IGJ1dHRvbkxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGJ1dHRvbkNhdGVnb3JpZXMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1jYXRlZ29yaWVzLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGJ1dHRvbkRhdGVBcHBseSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWRhdGUtYXBwbHktYnV0dG9uJyxcbiAgKTtcblxuICBjb25zdCBkcm9wZG93bkZpbHRlckRhdGU6IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItZGF0ZS1kcm9wZG93bicsXG4gICk7XG4gIGNvbnN0IGRyb3Bkb3duRmlsdGVyTG9jYXRpb246IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24tZHJvcGRvd24nLFxuICApO1xuICBjb25zdCBkcm9wZG93bkZpbHRlckNhdGVnb3JpZXM6IEhUTUxEaXZFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItY2F0ZWdvcmllcy1kcm9wZG93bicsXG4gICk7XG5cbiAgY29uc3Qgc3RhdHVzRmlsdGVyTG9jYXRpb24gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1sb2NhdGlvbi1zdGF0dXMnLFxuICApO1xuICBjb25zdCBpbnB1dExvY2F0aW9uOiBIVE1MSW5wdXRFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24taW5wdXQnLFxuICApO1xuICBjb25zdCBkYXRhbGlzdExvY2F0aW9uOiBIVE1MRGF0YUxpc3RFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24tbGlzdCcsXG4gICkgYXMgSFRNTERhdGFMaXN0RWxlbWVudDtcblxuICBmdW5jdGlvbiBhZGRIaWRkZW5DbGFzcyhlbGVtZW50OiBIVE1MRWxlbWVudCkge1xuICAgIGVsZW1lbnQuY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7XG4gIH1cblxuICBmdW5jdGlvbiBoYW5kbGVIaWRlRXZlbnRzKFxuICAgIGV2ZW50OiBNb3VzZUV2ZW50LFxuICAgIGVsZW1lbnQ6IEhUTUxFbGVtZW50LFxuICAgIG90aGVyRWxlbWVudD86IEhUTUxFbGVtZW50W10sXG4gICkge1xuICAgIGNvbnNvbGUubG9nKG90aGVyRWxlbWVudCk7XG5cbiAgICBpZiAoXG4gICAgICAhZWxlbWVudC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkgJiZcbiAgICAgICFvdGhlckVsZW1lbnQuc29tZShlbCA9PiBlbC5jb250YWlucyhldmVudC50YXJnZXQgYXMgTm9kZSkpXG4gICAgKSB7XG4gICAgICBhZGRIaWRkZW5DbGFzcyhlbGVtZW50KTtcbiAgICB9XG4gIH1cblxuICBmdW5jdGlvbiBhZGRIaWRlRXZlbnRzRm9yRWxlbWVudChcbiAgICBlbGVtZW50OiBIVE1MRWxlbWVudCxcbiAgICBvdGhlckVsZW1lbnQ6IEhUTUxFbGVtZW50W10gPSBbXSxcbiAgKSB7XG4gICAgZWxlbWVudC5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgICB3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsIChldmVudDogTW91c2VFdmVudCkgPT4ge1xuICAgICAgaGFuZGxlSGlkZUV2ZW50cyhldmVudCwgZWxlbWVudCwgb3RoZXJFbGVtZW50KTtcbiAgICB9KTtcblxuICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBmdW5jdGlvbiAoZXZlbnQpIHtcbiAgICAgIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICAgIGFkZEhpZGRlbkNsYXNzKGVsZW1lbnQpO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG5cbiAgYnV0dG9uRmlsdGVyRGF0ZS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGZ1bmN0aW9uICgpIHtcbiAgICBjb25zdCBkYXRlUGlja2VycyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5kYXRlcGlja2VyJyk7XG4gICAgY29uc3QgZGF0ZVBpY2tlckFycmF5OiBIVE1MRWxlbWVudFtdID0gQXJyYXkuZnJvbShcbiAgICAgIGRhdGVQaWNrZXJzLFxuICAgICkgYXMgSFRNTEVsZW1lbnRbXTtcblxuICAgIGFkZEhpZGVFdmVudHNGb3JFbGVtZW50KGRyb3Bkb3duRmlsdGVyRGF0ZSwgZGF0ZVBpY2tlckFycmF5KTtcbiAgfSk7XG5cbiAgYnV0dG9uRGF0ZUFwcGx5LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZnVuY3Rpb24gKCkge1xuICAgIGRyb3Bkb3duRmlsdGVyRGF0ZS5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgfSk7XG5cbiAgYnV0dG9uTG9jYXRpb24uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCBmdW5jdGlvbiAoKSB7XG4gICAgYWRkSGlkZUV2ZW50c0ZvckVsZW1lbnQoZHJvcGRvd25GaWx0ZXJMb2NhdGlvbik7XG4gIH0pO1xuXG4gIGJ1dHRvbkNhdGVnb3JpZXMuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCBmdW5jdGlvbiAoKSB7XG4gICAgYWRkSGlkZUV2ZW50c0ZvckVsZW1lbnQoZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzKTtcbiAgfSk7XG5cbiAgaW5wdXRMb2NhdGlvbi5vbmZvY3VzID0gZnVuY3Rpb24gKCkge1xuICAgIGRhdGFsaXN0TG9jYXRpb24uc3R5bGUuZGlzcGxheSA9ICdibG9jayc7XG4gICAgaW5wdXRMb2NhdGlvbi5zdHlsZS5ib3JkZXJSYWRpdXMgPSAnNXB4IDVweCAwIDAnO1xuICB9O1xuICBmb3IgKGxldCBpbmRleCBpbiBkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnMpIHtcbiAgICBjb25zdCBvcHRpb246IEhUTUxPcHRpb25FbGVtZW50ID0gZGF0YWxpc3RMb2NhdGlvbi5vcHRpb25zW2luZGV4XTtcbiAgICBvcHRpb24ub25jbGljayA9IGZ1bmN0aW9uICgpIHtcbiAgICAgIGlucHV0TG9jYXRpb24udmFsdWUgPSBvcHRpb24udmFsdWU7XG4gICAgICBzdGF0dXNGaWx0ZXJMb2NhdGlvbi5pbm5lckhUTUwgPSBvcHRpb24udmFsdWU7XG4gICAgICBkYXRhbGlzdExvY2F0aW9uLnN0eWxlLmRpc3BsYXkgPSAnbm9uZSc7XG4gICAgICBpbnB1dExvY2F0aW9uLnN0eWxlLmJvcmRlclJhZGl1cyA9ICc1cHgnO1xuICAgIH07XG4gIH1cblxuICBpbnB1dExvY2F0aW9uLm9uaW5wdXQgPSBmdW5jdGlvbiAoKSB7XG4gICAgY3VycmVudEZvY3VzID0gLTE7XG4gICAgY29uc3QgdGV4dCA9IGlucHV0TG9jYXRpb24udmFsdWUudG9VcHBlckNhc2UoKTtcbiAgICBmb3IgKGxldCBpbmRleCBpbiBkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnMpIHtcbiAgICAgIGNvbnN0IG9wdGlvbjogSFRNTE9wdGlvbkVsZW1lbnQgPSBkYXRhbGlzdExvY2F0aW9uLm9wdGlvbnNbaW5kZXhdO1xuICAgICAgaWYgKG9wdGlvbi52YWx1ZS50b1VwcGVyQ2FzZSgpLmluZGV4T2YodGV4dCkgPiAtMSkge1xuICAgICAgICBvcHRpb24uc3R5bGUuZGlzcGxheSA9ICdibG9jayc7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBvcHRpb24uc3R5bGUuZGlzcGxheSA9ICdub25lJztcbiAgICAgIH1cbiAgICB9XG4gIH07XG4gIGxldCBjdXJyZW50Rm9jdXMgPSAtMTtcbiAgaW5wdXRMb2NhdGlvbi5vbmtleWRvd24gPSBmdW5jdGlvbiAoZSkge1xuICAgIGlmIChlLmtleUNvZGUgPT0gNDApIHtcbiAgICAgIGN1cnJlbnRGb2N1cysrO1xuICAgICAgYWRkQWN0aXZlKGRhdGFsaXN0TG9jYXRpb24ub3B0aW9ucyk7XG4gICAgfSBlbHNlIGlmIChlLmtleUNvZGUgPT0gMzgpIHtcbiAgICAgIGN1cnJlbnRGb2N1cy0tO1xuICAgICAgYWRkQWN0aXZlKGRhdGFsaXN0TG9jYXRpb24ub3B0aW9ucyk7XG4gICAgfSBlbHNlIGlmIChlLmtleUNvZGUgPT0gMTMpIHtcbiAgICAgIGUucHJldmVudERlZmF1bHQoKTtcbiAgICAgIGlmIChjdXJyZW50Rm9jdXMgPiAtMSkge1xuICAgICAgICBpZiAoZGF0YWxpc3RMb2NhdGlvbi5vcHRpb25zKSB7XG4gICAgICAgICAgZGF0YWxpc3RMb2NhdGlvbi5vcHRpb25zW2N1cnJlbnRGb2N1c10uY2xpY2soKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgfTtcblxuICBmdW5jdGlvbiBhZGRBY3RpdmUoeDogSFRNTENvbGxlY3Rpb25PZjxIVE1MT3B0aW9uRWxlbWVudD4pIHtcbiAgICBpZiAoIXgpIHJldHVybjtcblxuICAgIGZhbHNlO1xuICAgIHJlbW92ZUFjdGl2ZSh4KTtcbiAgICBpZiAoY3VycmVudEZvY3VzID49IHgubGVuZ3RoKSBjdXJyZW50Rm9jdXMgPSAwO1xuICAgIGlmIChjdXJyZW50Rm9jdXMgPCAwKSBjdXJyZW50Rm9jdXMgPSB4Lmxlbmd0aCAtIDE7XG4gICAgeFtjdXJyZW50Rm9jdXNdLmNsYXNzTGlzdC5hZGQoJ2FjdGl2ZScpO1xuICB9XG5cbiAgZnVuY3Rpb24gcmVtb3ZlQWN0aXZlKHg6IEhUTUxDb2xsZWN0aW9uT2Y8SFRNTE9wdGlvbkVsZW1lbnQ+KSB7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCB4Lmxlbmd0aDsgaSsrKSB7XG4gICAgICB4W2ldLmNsYXNzTGlzdC5yZW1vdmUoJ2FjdGl2ZScpO1xuICAgIH1cbiAgfVxufSk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=