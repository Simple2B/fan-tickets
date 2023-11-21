document.addEventListener('DOMContentLoaded', function () {
  const buttonFilterDate = document.querySelector('#events-filter-date-button');
  const buttonLocation: HTMLDivElement = document.querySelector(
    '#events-filter-location-button',
  );
  const buttonCategories = document.querySelector(
    '#events-filter-categories-button',
  );
  const dropdownFilterDate = document.querySelector(
    '#events-filter-date-dropdown',
  );
  const dropdownFilterLocation: HTMLDivElement = document.querySelector(
    '#events-filter-location-dropdown',
  );
  const dropdownFilterCategories = document.querySelector(
    '#events-filter-categories-dropdown',
  );

  const buttonDateApply = document.querySelector(
    '#events-filter-date-apply-button',
  );
  const input: HTMLInputElement = document.querySelector(
    '#events-filter-location-input',
  );
  buttonFilterDate.addEventListener('click', function () {
    dropdownFilterDate.classList.toggle('hidden');
  });
  const browsers: HTMLDataElement = document.querySelector(
    '#events-filter-location-list',
  );
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
  for (let option of browsers.options) {
    option.onclick = function () {
      input.value = option.value;
      browsers.style.display = 'none';
      input.style.borderRadius = '5px';
    };
  }

  input.oninput = function () {
    currentFocus = -1;
    var text = input.value.toUpperCase();
    for (let option of browsers.options) {
      if (option.value.toUpperCase().indexOf(text) > -1) {
        option.style.display = 'block';
      } else {
        option.style.display = 'none';
      }
    }
  };
  var currentFocus = -1;
  input.onkeydown = function (e) {
    if (e.keyCode == 40) {
      currentFocus++;
      addActive(browsers.options);
    } else if (e.keyCode == 38) {
      currentFocus--;
      addActive(browsers.options);
    } else if (e.keyCode == 13) {
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (browsers.options) browsers.options[currentFocus].click();
      }
    }
  };

  function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
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
    const inputWidth = buttonLocation.offsetWidth;
    console.log(dropdownFilterLocation.offsetWidth);

    browsers.style.width = `${inputWidth}px`;
  }
});
