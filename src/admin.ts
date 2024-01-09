console.log('file admin.ts loaded');
console.log('admin.ts loaded 5 row');

const datesButton: HTMLDivElement = document.querySelector('#event-dates');
const datesDropdown: HTMLSelectElement = document.querySelector(
  '#event-dates-dropdown',
);
if (datesButton && datesDropdown) {
  datesButton.addEventListener('click', () => {
    datesDropdown.classList.toggle('hidden');
  });
}
