import {handleHideElements} from './utils';

function filterDropdownLocation(
  dropdownList: NodeListOf<HTMLDivElement>,
  dropdownInput: HTMLInputElement,
) {
  const filter = dropdownInput.value.toUpperCase();

  for (let i = 0; i < dropdownList.length; i++) {
    const txtValue = dropdownList[i].textContent || dropdownList[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      dropdownList[i].style.display = '';
    } else {
      dropdownList[i].style.display = 'none';
    }
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const buttonFilterDate = document.querySelector('#events-filter-date-button');
  const buttonLocation: HTMLDivElement = document.querySelector(
    '#events-filter-location-button',
  );
  const buttonLocationNames = document.querySelectorAll(
    '.dropdown-location-name-button',
  ) as NodeListOf<HTMLDivElement>;

  const buttonCategories = document.querySelector(
    '#events-filter-categories-button',
  );
  const buttonDateApply = document.querySelector(
    '#events-filter-date-apply-button',
  );

  const dropdownFilterDate: HTMLDivElement = document.querySelector(
    '#events-filter-date-dropdown',
  );
  const dropdownFilterLocation: HTMLDivElement =
    document.querySelector('#dropdown-location');
  const dropdownFilterCategories: HTMLDivElement = document.querySelector(
    '#events-filter-categories-dropdown',
  );

  const statusFilterLocation = document.querySelector(
    '#events-filter-location-status',
  );

  if (buttonFilterDate) {
    buttonFilterDate.addEventListener('click', () => {
      const datePickers = document.querySelectorAll('.datepicker');
      const datePickerArray: HTMLElement[] = Array.from(
        datePickers,
      ) as HTMLElement[];

      handleHideElements(dropdownFilterDate, datePickerArray);
    });
  }

  if (buttonDateApply) {
    buttonDateApply.addEventListener('click', () => {
      dropdownFilterDate.classList.toggle('hidden');
    });
  }

  if (buttonCategories) {
    buttonCategories.addEventListener('click', () => {
      handleHideElements(dropdownFilterCategories);
    });
  }

  if (statusFilterLocation) {
    const dropDownLocationInput: HTMLInputElement = document.querySelector(
      '#dropdown-location-input',
    );

    if (buttonLocation) {
      buttonLocation.addEventListener('click', () => {
        dropDownLocationInput.focus();
        handleHideElements(dropdownFilterLocation);
      });
    }

    buttonLocationNames.forEach((button: HTMLDivElement) => {
      button.addEventListener('click', () => {
        statusFilterLocation.innerHTML = button.innerHTML;
        handleHideElements(dropdownFilterLocation);
      });
    });
    dropDownLocationInput.addEventListener('keyup', () => {
      filterDropdownLocation(buttonLocationNames, dropDownLocationInput);
    });
  }
});
