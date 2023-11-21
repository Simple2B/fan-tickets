/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!**********************!*\
  !*** ./src/event.ts ***!
  \**********************/
document.addEventListener('DOMContentLoaded', function () {
    var buttonFilterDate = document.querySelector('#events-filter-date-button');
    var buttonLocation = document.querySelector('#events-filter-location-button');
    var buttonCategories = document.querySelector('#events-filter-categories-button');
    var dropdownFilterDate = document.querySelector('#events-filter-date-dropdown');
    var dropdownFilterLocation = document.querySelector('#events-filter-location-dropdown');
    var dropdownFilterCategories = document.querySelector('#events-filter-categories-dropdown');
    var buttonDateApply = document.querySelector('#events-filter-date-apply-button');
    var input = document.querySelector('#events-filter-location-input');
    buttonFilterDate.addEventListener('click', function () {
        dropdownFilterDate.classList.toggle('hidden');
    });
    var browsers = document.querySelector('#events-filter-location-list');
    buttonLocation.addEventListener('click', function () {
        dropdownFilterLocation.classList.toggle('hidden');
    });
    buttonCategories.addEventListener('click', function () {
        dropdownFilterCategories.classList.toggle('hidden');
    });
    buttonDateApply.addEventListener('click', function () {
        dropdownFilterDate.classList.toggle('hidden');
    });
    input.onfocus = function () {
        browsers.style.display = 'block';
        input.style.borderRadius = '5px 5px 0 0';
    };
    var _loop_1 = function (option) {
        option.onclick = function () {
            input.value = option.value;
            browsers.style.display = 'none';
            input.style.borderRadius = '5px';
        };
    };
    for (var _i = 0, _a = browsers.options; _i < _a.length; _i++) {
        var option = _a[_i];
        _loop_1(option);
    }
    input.oninput = function () {
        currentFocus = -1;
        var text = input.value.toUpperCase();
        for (var _i = 0, _a = browsers.options; _i < _a.length; _i++) {
            var option = _a[_i];
            if (option.value.toUpperCase().indexOf(text) > -1) {
                option.style.display = 'block';
            }
            else {
                option.style.display = 'none';
            }
        }
    };
    var currentFocus = -1;
    input.onkeydown = function (e) {
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(browsers.options);
        }
        else if (e.keyCode == 38) {
            currentFocus--;
            addActive(browsers.options);
        }
        else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (browsers.options)
                    browsers.options[currentFocus].click();
            }
        }
    };
    function addActive(x) {
        if (!x)
            return false;
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
    // Set the initial width
    setDatalistWidth();
    // Update the width whenever the window is resized
    window.addEventListener('resize', setDatalistWidth);
    function setDatalistWidth() {
        var inputWidth = buttonLocation.offsetWidth;
        console.log(dropdownFilterLocation.offsetWidth);
        browsers.style.width = "".concat(inputWidth, "px");
    }
});

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,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LENBQUMsUUFBUSxDQUFDLENBQUM7SUFDMUMsQ0FBQztJQUNELFNBQVMsWUFBWSxDQUFDLENBQUM7UUFDckIsS0FBSyxJQUFJLENBQUMsR0FBRyxDQUFDLEVBQUUsQ0FBQyxHQUFHLENBQUMsQ0FBQyxNQUFNLEVBQUUsQ0FBQyxFQUFFLEVBQUU7WUFDakMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUM7U0FDakM7SUFDSCxDQUFDO0lBRUQsd0JBQXdCO0lBQ3hCLGdCQUFnQixFQUFFLENBQUM7SUFFbkIsa0RBQWtEO0lBQ2xELE1BQU0sQ0FBQyxnQkFBZ0IsQ0FBQyxRQUFRLEVBQUUsZ0JBQWdCLENBQUMsQ0FBQztJQUVwRCxTQUFTLGdCQUFnQjtRQUN2QixJQUFNLFVBQVUsR0FBRyxjQUFjLENBQUMsV0FBVyxDQUFDO1FBQzlDLE9BQU8sQ0FBQyxHQUFHLENBQUMsc0JBQXNCLENBQUMsV0FBVyxDQUFDLENBQUM7UUFFaEQsUUFBUSxDQUFDLEtBQUssQ0FBQyxLQUFLLEdBQUcsVUFBRyxVQUFVLE9BQUksQ0FBQztJQUMzQyxDQUFDO0FBQ0gsQ0FBQyxDQUFDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zdGF0aWMvLi9zcmMvZXZlbnQudHMiXSwic291cmNlc0NvbnRlbnQiOlsiZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsIGZ1bmN0aW9uICgpIHtcbiAgY29uc3QgYnV0dG9uRmlsdGVyRGF0ZSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJyNldmVudHMtZmlsdGVyLWRhdGUtYnV0dG9uJyk7XG4gIGNvbnN0IGJ1dHRvbkxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGJ1dHRvbkNhdGVnb3JpZXMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICcjZXZlbnRzLWZpbHRlci1jYXRlZ29yaWVzLWJ1dHRvbicsXG4gICk7XG4gIGNvbnN0IGRyb3Bkb3duRmlsdGVyRGF0ZSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWRhdGUtZHJvcGRvd24nLFxuICApO1xuICBjb25zdCBkcm9wZG93bkZpbHRlckxvY2F0aW9uOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWRyb3Bkb3duJyxcbiAgKTtcbiAgY29uc3QgZHJvcGRvd25GaWx0ZXJDYXRlZ29yaWVzID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItY2F0ZWdvcmllcy1kcm9wZG93bicsXG4gICk7XG5cbiAgY29uc3QgYnV0dG9uRGF0ZUFwcGx5ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItZGF0ZS1hcHBseS1idXR0b24nLFxuICApO1xuICBjb25zdCBpbnB1dDogSFRNTElucHV0RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXG4gICAgJyNldmVudHMtZmlsdGVyLWxvY2F0aW9uLWlucHV0JyxcbiAgKTtcbiAgYnV0dG9uRmlsdGVyRGF0ZS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGZ1bmN0aW9uICgpIHtcbiAgICBkcm9wZG93bkZpbHRlckRhdGUuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gIH0pO1xuICBjb25zdCBicm93c2VyczogSFRNTERhdGFFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAnI2V2ZW50cy1maWx0ZXItbG9jYXRpb24tbGlzdCcsXG4gICk7XG4gIGJ1dHRvbkxvY2F0aW9uLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZnVuY3Rpb24gKCkge1xuICAgIGRyb3Bkb3duRmlsdGVyTG9jYXRpb24uY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gIH0pO1xuICBidXR0b25DYXRlZ29yaWVzLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZnVuY3Rpb24gKCkge1xuICAgIGRyb3Bkb3duRmlsdGVyQ2F0ZWdvcmllcy5jbGFzc0xpc3QudG9nZ2xlKCdoaWRkZW4nKTtcbiAgfSk7XG4gIGJ1dHRvbkRhdGVBcHBseS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGZ1bmN0aW9uICgpIHtcbiAgICBkcm9wZG93bkZpbHRlckRhdGUuY2xhc3NMaXN0LnRvZ2dsZSgnaGlkZGVuJyk7XG4gIH0pO1xuXG4gIGlucHV0Lm9uZm9jdXMgPSBmdW5jdGlvbiAoKSB7XG4gICAgYnJvd3NlcnMuc3R5bGUuZGlzcGxheSA9ICdibG9jayc7XG4gICAgaW5wdXQuc3R5bGUuYm9yZGVyUmFkaXVzID0gJzVweCA1cHggMCAwJztcbiAgfTtcbiAgZm9yIChsZXQgb3B0aW9uIG9mIGJyb3dzZXJzLm9wdGlvbnMpIHtcbiAgICBvcHRpb24ub25jbGljayA9IGZ1bmN0aW9uICgpIHtcbiAgICAgIGlucHV0LnZhbHVlID0gb3B0aW9uLnZhbHVlO1xuICAgICAgYnJvd3NlcnMuc3R5bGUuZGlzcGxheSA9ICdub25lJztcbiAgICAgIGlucHV0LnN0eWxlLmJvcmRlclJhZGl1cyA9ICc1cHgnO1xuICAgIH07XG4gIH1cblxuICBpbnB1dC5vbmlucHV0ID0gZnVuY3Rpb24gKCkge1xuICAgIGN1cnJlbnRGb2N1cyA9IC0xO1xuICAgIHZhciB0ZXh0ID0gaW5wdXQudmFsdWUudG9VcHBlckNhc2UoKTtcbiAgICBmb3IgKGxldCBvcHRpb24gb2YgYnJvd3NlcnMub3B0aW9ucykge1xuICAgICAgaWYgKG9wdGlvbi52YWx1ZS50b1VwcGVyQ2FzZSgpLmluZGV4T2YodGV4dCkgPiAtMSkge1xuICAgICAgICBvcHRpb24uc3R5bGUuZGlzcGxheSA9ICdibG9jayc7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBvcHRpb24uc3R5bGUuZGlzcGxheSA9ICdub25lJztcbiAgICAgIH1cbiAgICB9XG4gIH07XG4gIHZhciBjdXJyZW50Rm9jdXMgPSAtMTtcbiAgaW5wdXQub25rZXlkb3duID0gZnVuY3Rpb24gKGUpIHtcbiAgICBpZiAoZS5rZXlDb2RlID09IDQwKSB7XG4gICAgICBjdXJyZW50Rm9jdXMrKztcbiAgICAgIGFkZEFjdGl2ZShicm93c2Vycy5vcHRpb25zKTtcbiAgICB9IGVsc2UgaWYgKGUua2V5Q29kZSA9PSAzOCkge1xuICAgICAgY3VycmVudEZvY3VzLS07XG4gICAgICBhZGRBY3RpdmUoYnJvd3NlcnMub3B0aW9ucyk7XG4gICAgfSBlbHNlIGlmIChlLmtleUNvZGUgPT0gMTMpIHtcbiAgICAgIGUucHJldmVudERlZmF1bHQoKTtcbiAgICAgIGlmIChjdXJyZW50Rm9jdXMgPiAtMSkge1xuICAgICAgICAvKmFuZCBzaW11bGF0ZSBhIGNsaWNrIG9uIHRoZSBcImFjdGl2ZVwiIGl0ZW06Ki9cbiAgICAgICAgaWYgKGJyb3dzZXJzLm9wdGlvbnMpIGJyb3dzZXJzLm9wdGlvbnNbY3VycmVudEZvY3VzXS5jbGljaygpO1xuICAgICAgfVxuICAgIH1cbiAgfTtcblxuICBmdW5jdGlvbiBhZGRBY3RpdmUoeCkge1xuICAgIGlmICgheCkgcmV0dXJuIGZhbHNlO1xuICAgIHJlbW92ZUFjdGl2ZSh4KTtcbiAgICBpZiAoY3VycmVudEZvY3VzID49IHgubGVuZ3RoKSBjdXJyZW50Rm9jdXMgPSAwO1xuICAgIGlmIChjdXJyZW50Rm9jdXMgPCAwKSBjdXJyZW50Rm9jdXMgPSB4Lmxlbmd0aCAtIDE7XG4gICAgeFtjdXJyZW50Rm9jdXNdLmNsYXNzTGlzdC5hZGQoJ2FjdGl2ZScpO1xuICB9XG4gIGZ1bmN0aW9uIHJlbW92ZUFjdGl2ZSh4KSB7XG4gICAgZm9yICh2YXIgaSA9IDA7IGkgPCB4Lmxlbmd0aDsgaSsrKSB7XG4gICAgICB4W2ldLmNsYXNzTGlzdC5yZW1vdmUoJ2FjdGl2ZScpO1xuICAgIH1cbiAgfVxuXG4gIC8vIFNldCB0aGUgaW5pdGlhbCB3aWR0aFxuICBzZXREYXRhbGlzdFdpZHRoKCk7XG5cbiAgLy8gVXBkYXRlIHRoZSB3aWR0aCB3aGVuZXZlciB0aGUgd2luZG93IGlzIHJlc2l6ZWRcbiAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ3Jlc2l6ZScsIHNldERhdGFsaXN0V2lkdGgpO1xuXG4gIGZ1bmN0aW9uIHNldERhdGFsaXN0V2lkdGgoKSB7XG4gICAgY29uc3QgaW5wdXRXaWR0aCA9IGJ1dHRvbkxvY2F0aW9uLm9mZnNldFdpZHRoO1xuICAgIGNvbnNvbGUubG9nKGRyb3Bkb3duRmlsdGVyTG9jYXRpb24ub2Zmc2V0V2lkdGgpO1xuXG4gICAgYnJvd3NlcnMuc3R5bGUud2lkdGggPSBgJHtpbnB1dFdpZHRofXB4YDtcbiAgfVxufSk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=