import {handleHideElements} from './utils';

console.log('file admin.ts loaded');
console.log('admin.ts loaded 5 row');

const datesButton: HTMLDivElement = document.querySelector('#event-dates');
const datesDropdown: HTMLSelectElement = document.querySelector(
  '#event-dates-dropdown',
);

datesButton.addEventListener('click', () => {
  const datePickers = document.querySelectorAll('.datepicker');
  const datePickerArray: HTMLElement[] = Array.from(
    datePickers,
  ) as HTMLElement[];

  handleHideElements(datesDropdown, datePickerArray);
});

const searchInput: HTMLInputElement = document.querySelector(
  '#table-search-events',
);
const searchInputButton = document.querySelector('#table-search-events-button');
if (searchInputButton && searchInput) {
  searchInputButton.addEventListener('click', () => {
    searchInput.value = '';
    searchInput.click();
  });
}
