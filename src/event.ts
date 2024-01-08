import {handleHideElements} from './utils';

document.addEventListener('DOMContentLoaded', function () {
  const buttonFilterDate = document.querySelector('#events-filter-date-button');
  const buttonLocation: HTMLDivElement = document.querySelector(
    '#events-filter-location-button',
  );
  const buttonCategories = document.querySelector(
    '#events-filter-categories-button',
  );
  const buttonDateApply = document.querySelector(
    '#events-filter-date-apply-button',
  );

  const dropdownFilterDate: HTMLDivElement = document.querySelector(
    '#events-filter-date-dropdown',
  );
  const dropdownFilterLocation: HTMLDivElement = document.querySelector(
    '#events-filter-location-dropdown',
  );
  const dropdownFilterCategories: HTMLDivElement = document.querySelector(
    '#events-filter-categories-dropdown',
  );

  const statusFilterLocation = document.querySelector(
    '#events-filter-location-status',
  );
  const inputLocation: HTMLInputElement = document.querySelector(
    '#events-filter-location-input',
  );
  const datalistLocation: HTMLDataListElement = document.querySelector(
    '#events-filter-location-list',
  ) as HTMLDataListElement;

  buttonFilterDate.addEventListener('click', () => {
    const datePickers = document.querySelectorAll('.datepicker');
    const datePickerArray: HTMLElement[] = Array.from(
      datePickers,
    ) as HTMLElement[];

    handleHideElements(dropdownFilterDate, datePickerArray);
  });

  buttonDateApply.addEventListener('click', () => {
    dropdownFilterDate.classList.toggle('hidden');
  });

  buttonLocation.addEventListener('click', () => {
    handleHideElements(dropdownFilterLocation);
    inputLocation.focus();
  });

  buttonCategories.addEventListener('click', () => {
    handleHideElements(dropdownFilterCategories);
  });

  inputLocation.onfocus = function () {
    datalistLocation.style.display = 'block';
    inputLocation.style.borderRadius = '5px 5px 0 0';
  };
  for (let index in datalistLocation.options) {
    const option: HTMLOptionElement = datalistLocation.options[index];
    option.onclick = function () {
      inputLocation.value = option.value;
      statusFilterLocation.innerHTML = option.value;
      datalistLocation.style.display = 'none';
      inputLocation.style.borderRadius = '5px';
    };
  }

  inputLocation.oninput = function () {
    currentFocus = -1;
    const text = inputLocation.value.toUpperCase();
    for (let index in datalistLocation.options) {
      const option: HTMLOptionElement = datalistLocation.options[index];
      option.value.toUpperCase().indexOf(text) > -1
        ? (option.style.display = 'block')
        : (option.style.display = 'none');
    }
  };

  let currentFocus = -1;
  inputLocation.onkeydown = function (e) {
    if (e.keyCode == 40) {
      currentFocus++;
      addActive(datalistLocation.options);
    } else if (e.keyCode == 38) {
      currentFocus--;
      addActive(datalistLocation.options);
    } else if (e.keyCode == 13) {
      e.preventDefault();
      if (currentFocus > -1) {
        if (datalistLocation.options) {
          datalistLocation.options[currentFocus].click();
        }
      }
    }
  };

  function addActive(x: HTMLCollectionOf<HTMLOptionElement>) {
    if (!x) return;

    false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
    x[currentFocus].classList.add('active');
  }

  function removeActive(x: HTMLCollectionOf<HTMLOptionElement>) {
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove('active');
    }
  }
});
