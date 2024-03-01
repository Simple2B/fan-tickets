import {Modal} from 'flowbite';
import type {ModalOptions, ModalInterface} from 'flowbite';

// /*
//  * $editUserModal: required
//  * options: optional
//  */

// // For your js code

interface IUser {
  id: number;
  username: string;
  email: string;
  activated: boolean;
}

const $modalElement: HTMLElement = document.querySelector('#editUserModal');
const $addUserModalElement: HTMLElement =
  document.querySelector('#add-user-modal');

const modalOptions: ModalOptions = {
  placement: 'bottom-right',
  backdrop: 'dynamic',
  backdropClasses:
    'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40',
  closable: true,
  onHide: () => {
    console.log('modal is hidden');
  },
  onShow: () => {
    console.log('user id: ');
  },
  onToggle: () => {
    console.log('modal has been toggled');
  },
};

const modal: ModalInterface = new Modal($modalElement, modalOptions);
const addModal: ModalInterface = new Modal($addUserModalElement, modalOptions);

const $buttonElements = document.querySelectorAll('.user-edit-button');
$buttonElements.forEach(e =>
  e.addEventListener('click', () => {
    editUser(JSON.parse(e.getAttribute('data-target')));
  }),
);

// closing add edit modal
const $buttonClose = document.querySelector('#modalCloseButton');
if ($buttonClose) {
  $buttonClose.addEventListener('click', () => {
    modal.hide();
  });
}

// closing add user modal
const addModalCloseBtn = document.querySelector('#modalAddCloseButton');
if (addModalCloseBtn) {
  addModalCloseBtn.addEventListener('click', () => {
    addModal.hide();
  });
}

// search flow
const searchInput: HTMLInputElement = document.querySelector(
  '#table-search-users',
);
const searchInputButton = document.querySelector('#table-search-user-button');
if (searchInputButton && searchInput) {
  searchInputButton.addEventListener('click', () => {
    searchInput.value = '';
    searchInput.click();
  });
}
const deleteButtons = document.querySelectorAll('.delete-user-btn');

deleteButtons.forEach(e => {
  e.addEventListener('click', async () => {
    if (confirm('Are sure?')) {
      let id = e.getAttribute('data-user-id');
      const response = await fetch(`/user/delete/${id}`, {
        method: 'DELETE',
      });
      if (response.status == 200) {
        location.reload();
      }
    }
  });
});

function editUser(user: IUser) {
  let input: HTMLInputElement = document.querySelector('#user-edit-username');
  input.value = user.username;
  input = document.querySelector('#user-edit-id');
  input.value = user.id.toString();
  input = document.querySelector('#user-edit-email');
  input.value = user.email;
  input = document.querySelector('#user-edit-password');
  input.value = '*******';
  input = document.querySelector('#user-edit-password_confirmation');
  input.value = '*******';
  input = document.querySelector('#user-edit-activated');
  input.checked = user.activated;
  input = document.querySelector('#user-edit-next_url');
  input.value = window.location.href;
  modal.show();
}

const imageUploadInput = document.querySelector(
  '#sidebar-image-input',
) as HTMLInputElement;
const eventImageUploadInput = document.querySelector(
  '#event-image-input',
) as HTMLInputElement;

if (imageUploadInput) {
  imageUploadInput.addEventListener('change', function (e: Event) {
    const target = e.target as HTMLInputElement;
    const files = target.files;
    if (files && files.length > 0) {
      const file = files[0];
      const instance = 'user';
      handleImageUpload(file, instance);
    }
  });
}

if (eventImageUploadInput) {
  eventImageUploadInput.addEventListener('change', function (e: Event) {
    const target = e.target as HTMLInputElement;
    const files = target.files;

    if (files && files.length > 0) {
      console.log('files inside if', files);

      const file = files[0];
      const instance = 'event';
      const uniqueIdInput: HTMLInputElement =
        document.querySelector('#event-unique-id');
      console.log('uniqueIdInput', uniqueIdInput.value);

      handleImageUpload(file, instance, uniqueIdInput.value);
    }
  });
}

function handleImageUpload(file: File, instance: string, uniqueId?: string) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('instance', instance);
  if (uniqueId) {
    formData.append('uniqueId', uniqueId);
  }

  const reader = new FileReader();
  reader.onload = function (e) {
    // fetch('/user/logo-upload', {
    //   method: 'POST',
    //   body: formData,
    // })
    //   .then(response => console.log('response', response))
    //   .then(() => window.location.reload())
    //   .catch(error => {
    //     console.error('Error:', error);
    //   });
  };
  reader.readAsDataURL(file);
}

// function to make dropdowns in user profile
function openCloseDropdown(
  button: HTMLButtonElement,
  container: HTMLDivElement,
) {
  container.classList.toggle('dropdown-close');
  container.classList.toggle('dropdown-open');
  container.classList.contains('dropdown-close')
    ? (button.innerHTML = 'Mostrar')
    : (button.innerHTML = 'Ocultar');
}

const subscribeButton: HTMLButtonElement = document.querySelector(
  '#user-profile-subscribe-btn',
);
const paymentButton: HTMLButtonElement = document.querySelector(
  '#user-profile-payment-btn',
);
const emailButton: HTMLButtonElement = document.querySelector(
  '#user-profile-email-btn',
);
const subscribeContainer: HTMLDivElement = document.querySelector(
  '#user-profile-subscribe-container',
);
const paymentContainer: HTMLDivElement = document.querySelector(
  '#user-profile-payment-container',
);
const emailContainer: HTMLDivElement = document.querySelector(
  '#user-profile-email-container',
);

if (subscribeButton) {
  subscribeButton.addEventListener('click', () => {
    openCloseDropdown(subscribeButton, subscribeContainer);
  });
}

if (paymentButton) {
  paymentButton.addEventListener('click', () => {
    openCloseDropdown(paymentButton, paymentContainer);
  });
}

if (emailButton) {
  emailButton.addEventListener('click', () => {
    openCloseDropdown(emailButton, emailContainer);
  });
}
