import {easepick} from '@easepick/bundle';

function scrollDown(element: HTMLDivElement) {
  setTimeout(() => {
    element.scrollTo({
      top: element.scrollHeight,
      behavior: 'smooth',
    });
  }, 200);
}

function toggleChatWindow() {
  const chatWindow: HTMLDivElement = document.querySelector('#chat-window');
  chatWindow.classList.toggle('chat-window-close');
  chatWindow.classList.toggle('chat-window-open');
}

document.addEventListener('DOMContentLoaded', () => {
  const chatIcon = document.querySelector('#chat-icon');
  const chatBody: HTMLDivElement = document.querySelector('#chat-body');
  const openIcon = chatIcon.querySelector('.chat-icon-open');
  const closeIcon = chatIcon.querySelector('.chat-icon-close');

  chatIcon.addEventListener('click', () => {
    // openIcon.classList.toggle('chat-icon-inactive');
    // closeIcon.classList.toggle('chat-icon-active');
    toggleChatWindow();
    scrollDown(chatBody);

    const observer = new MutationObserver(mutations => {
      const locationButton = document.querySelector(
        '#chat-sell-location-button',
      );
      if (locationButton) {
        locationButton.addEventListener('click', () => {});
      }

      mutations.forEach(mutation => {
        if (mutation.type === 'childList') {
          scrollDown(chatBody);
        }
      });
    });

    observer.observe(chatBody, {childList: true});
  });
});

const locationButton = document.querySelector('.chat-filter-location-button');
const dropdownFilterDate: HTMLDivElement = document.querySelector(
  '#chat-filter-location-dropdown',
);
const inputLocation: HTMLInputElement = document.querySelector(
  '#chat-filter-location-input',
);
const datalistLocation: HTMLDataListElement = document.querySelector(
  '#chat-filter-location-list',
) as HTMLDataListElement;
const statusFilterLocation = document.querySelector(
  '#chat-filter-location-status',
);

const datepickerFilter = document.getElementById('datepicker-filter');
if (datepickerFilter) {
  const chatBody: HTMLDivElement = document.querySelector('#chat-body');
  const picker = new easepick.create({
    element: document.getElementById('datepicker-filter'),
    css: ['https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.1/dist/index.css'],
    format: 'MM/DD/YYYY',
  });
  datepickerFilter.addEventListener('click', () => {
    scrollDown(chatBody);
  });
}

if (locationButton) {
  locationButton.addEventListener('click', () => {
    const chatBody: HTMLDivElement = document.querySelector('#chat-body');
    dropdownFilterDate.classList.toggle('chat-location-dropdown-active');
    inputLocation.focus();
    scrollDown(chatBody);
  });
}

if (inputLocation) {
  inputLocation.onfocus = function () {
    datalistLocation.style.display = 'block';
    inputLocation.style.borderRadius = '5px 5px 0 0';
  };
  for (let index in datalistLocation.options) {
    const option: HTMLOptionElement = datalistLocation.options[index];
    if (typeof option !== 'number') {
      option.onclick = function () {
        inputLocation.value = option.value;
        statusFilterLocation.innerHTML = option.value;
        dropdownFilterDate.classList.remove('chat-location-dropdown-active');
        datalistLocation.style.display = 'none';
        inputLocation.style.borderRadius = '5px';
      };
    }
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

  const addActive = (x: HTMLCollectionOf<HTMLOptionElement>) => {
    if (!x) return;

    false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
    x[currentFocus].classList.add('active');
  };

  const removeActive = (x: HTMLCollectionOf<HTMLOptionElement>) => {
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove('active');
    }
  };
}

const chatCloseButtons = document.querySelectorAll('.chat-close-button');
if (chatCloseButtons) {
  chatCloseButtons.forEach(button => {
    button.addEventListener('click', () => {
      toggleChatWindow();
    });
  });
}

const categoryDropdowns = document.querySelectorAll('.dropdown');

if (categoryDropdowns) {
  const chatBody: HTMLDivElement = document.querySelector('#chat-body');
  categoryDropdowns.forEach(dropdown => {
    const dropdownButton = dropdown.querySelector('.dropdown-button');
    const dropdownMenu = dropdown.querySelector('.dropdown-list');
    const dropdownArrow = dropdown.querySelector('.dropdown-arrow');
    const categoryButtons = dropdown.querySelectorAll('.chat-category-button');
    const eventCategoryInput: HTMLInputElement = document.querySelector(
      '#event-category-input',
    );
    const dropdownTitle = dropdown.querySelector('.chat-category-title');
    if (dropdownButton) {
      dropdownButton.addEventListener('click', e => {
        scrollDown(chatBody);
        const currentDropdown = (e.target as Element).closest('.dropdown');

        dropdownMenu.classList.toggle('dropdown-list-active');
        dropdownArrow.classList.toggle('rotate-180');
        categoryButtons.forEach(button => {
          button.addEventListener('click', () => {
            const currentCategory = button.getAttribute('data-category');
            eventCategoryInput.value = currentCategory;
            dropdownTitle.innerHTML = currentCategory;
            dropdownMenu.classList.remove('dropdown-list-active');
            dropdownArrow.classList.remove('rotate-180');
          });
        });

        categoryDropdowns.forEach(dropdown => {
          if (dropdown !== currentDropdown) {
            dropdown
              .querySelector('.dropdown-list')
              .classList.remove('dropdown-list-active');
          }
        });

        window.addEventListener('mouseup', event => {
          if (!dropdown.contains(event.target as Node)) {
            dropdownMenu.classList.remove('dropdown-list-active');
            dropdownArrow.classList.remove('rotate-180');
          }
        });
      });
    }
  });
}

const identityDocumentUploadInput = document.querySelector(
  '#chat-auth-identity-input',
) as HTMLInputElement;

if (identityDocumentUploadInput) {
  identityDocumentUploadInput.addEventListener('change', function (e: Event) {
    const target = e.target as HTMLInputElement;
    const files = target.files;
    if (files && files.length > 0) {
      const file = files[0];
      handleImageUpload(file);
    }
  });
}

function handleImageUpload(file: File) {
  const roomUniqueIdInput: HTMLInputElement = document.querySelector(
    '#chat-room-unique-id',
  );
  const formData = new FormData();
  formData.append('file', file);
  formData.append('room_unique_id', roomUniqueIdInput.value);

  const reader = new FileReader();
  reader.onload = function (e) {
    fetch('/chat/identification', {
      method: 'POST',
      body: formData,
    })
      .then(response => console.log('response', response))
      .catch(error => {
        console.error('Error:', error);
      });
  };
  reader.readAsDataURL(file);
}
