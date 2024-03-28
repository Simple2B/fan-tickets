import 'flowbite';
import {disableDateFlowbite, resizeChat, socialMediaShare} from './utils';

const themeToggleDarkIcons = document.querySelectorAll(
  '#theme-toggle-dark-icon',
);
const themeToggleLightIcons = document.querySelectorAll(
  '#theme-toggle-light-icon',
);

// Change the icons inside the button based on previous settings
// if (
//   localStorage.getItem('color-theme') === 'dark' ||
//   (!('color-theme' in localStorage) &&
//     window.matchMedia('(prefers-color-scheme: dark)').matches)
// ) {
//   themeToggleLightIcons.forEach(function (el) {
//     el.classList.remove('hidden');
//   });
//   document.documentElement.classList.add('dark');
// } else {
//   themeToggleDarkIcons.forEach(function (el) {
//     el.classList.remove('hidden');
//   });
//   document.documentElement.classList.remove('dark');
// }

document.documentElement.classList.add('dark');

// const themeToggleButtons = document.querySelectorAll('#theme-toggle');

// themeToggleButtons.forEach(function (themeToggleBtn) {
//   themeToggleBtn.addEventListener('click', function () {
//     // toggle icons inside button
//     themeToggleDarkIcons.forEach(function (themeToggleDarkIcon) {
//       themeToggleDarkIcon.classList.toggle('hidden');
//     });

//     themeToggleLightIcons.forEach(function (themeToggleLightIcon) {
//       themeToggleLightIcon.classList.toggle('hidden');
//     });

//     // if set via local storage previously
//     if (localStorage.getItem('color-theme')) {
//       if (localStorage.getItem('color-theme') === 'light') {
//         document.documentElement.classList.add('dark');
//         localStorage.setItem('color-theme', 'dark');
//       } else {
//         document.documentElement.classList.remove('dark');
//         localStorage.setItem('color-theme', 'light');
//       }

//       // if NOT set via local storage previously
//     } else {
//       if (document.documentElement.classList.contains('dark')) {
//         document.documentElement.classList.remove('dark');
//         localStorage.setItem('color-theme', 'light');
//       } else {
//         document.documentElement.classList.add('dark');
//         localStorage.setItem('color-theme', 'dark');
//       }
//     }
//   });
// });

// function to sticky header
const header = document.querySelector('.header');
// 20% of the viewport heights
const scrollPosition = 0.2 * window.innerHeight;

if (header) {
  window.addEventListener('scroll', () => {
    header.classList.toggle('header-sticky', window.scrollY > 0);
  });
}

if (window.scrollY > 0) {
  header.classList.add('header-sticky');
}

// function to show and hide the scroll to top button
const scrollTopButton = document.querySelector('.footer-scroll-top');

if (scrollTopButton) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > scrollPosition) {
      scrollTopButton.classList.remove('scroll-top-anchor-close');
      scrollTopButton.classList.add('scroll-top-anchor-open');
    } else {
      scrollTopButton.classList.remove('scroll-top-anchor-open');
      scrollTopButton.classList.add('scroll-top-anchor-close');
    }
  });
}

if (scrollTopButton) {
  scrollTopButton.addEventListener('click', e => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  });
}

// header user dropdown
const headerUserDropdown = document.querySelector('#header-user-dropdown');
const headerUserDropdownButton = document.querySelector(
  '#header-user-dropdown-button',
);
const headerUserDropdownArrow = document.querySelector(
  '#header-user-dropdown-arrow',
);

if (headerUserDropdownButton) {
  headerUserDropdownButton.addEventListener('click', () => {
    headerUserDropdownArrow.classList.toggle('rotate-180');
    headerUserDropdown.classList.toggle('header-user-dropdown-active');

    window.addEventListener('mouseup', event => {
      if (!headerUserDropdown.contains(event.target as Node)) {
        headerUserDropdown.classList.remove('header-user-dropdown-active');
        headerUserDropdownArrow.classList.remove('rotate-180');
      }
    });
  });
}

// mobile menu
const menuButtonOpen = document.querySelector('#menu-button-open');
const menuButtonClose = document.querySelector('#menu-button-close');
const menu = document.querySelector('#menu');

if (menuButtonOpen) {
  menuButtonOpen.addEventListener('click', () => {
    menu.classList.toggle('menu-mobile-active');
  });
}

if (menuButtonClose) {
  menuButtonClose.addEventListener('click', () => {
    menu.classList.toggle('menu-mobile-active');
  });
}

// mobile menu dropdowns
const menuMobileDropdowns = document.querySelectorAll('.dropdown');

if (menuMobileDropdowns) {
  menuMobileDropdowns.forEach(dropdown => {
    const dropdownButton = dropdown.querySelector('.dropdown-button');
    const dropdownMenu = dropdown.querySelector('.dropdown-list');
    const dropdownArrow = dropdown.querySelector('.dropdown-arrow');

    dropdownButton.addEventListener('click', e => {
      const currentDropdown = (e.target as Element).closest('.dropdown');

      dropdownMenu.classList.toggle('dropdown-list-active');
      dropdownArrow.classList.toggle('rotate-180');

      menuMobileDropdowns.forEach(dropdown => {
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
  });
}

// register verification modal
const verificationInputs = document.querySelectorAll(
  '.auth-register-verification-input',
) as NodeListOf<HTMLInputElement>;
const verificationButton = document.querySelector(
  '#auth-register-verification-button',
);

verificationInputs.forEach((input: HTMLInputElement, index1) => {
  input.addEventListener('keyup', event => {
    const currentInput = input;
    const nextInput = input.nextElementSibling as HTMLInputElement;
    const previousInput = input.previousElementSibling as HTMLInputElement;

    if (currentInput.value.length > 1) {
      currentInput.value = '';
      return;
    }

    if (nextInput && nextInput.hasAttribute('disabled') && currentInput.value) {
      nextInput.removeAttribute('disabled');
      nextInput.focus();
    }

    if (event.key === 'Backspace') {
      verificationInputs.forEach((input, index2) => {
        if (index1 <= index2 && previousInput) {
          input.setAttribute('disabled', 'disabled');
          currentInput.value = '';
          previousInput.focus();
        }
      });
    }

    if (!verificationInputs[5].disabled && verificationInputs[5].value !== '') {
      verificationButton.removeAttribute('disabled');
      verificationButton.classList.remove(
        'auth-register-verification-button-disabled',
      );
      return;
    }
    verificationButton.setAttribute('disabled', 'disabled');
    verificationButton.classList.add(
      'auth-register-verification-button-disabled',
    );
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const chatIcon = document.querySelector('#chat-icon');
  if (chatIcon) {
    chatIcon.addEventListener('click', () => {
      setTimeout(() => {
        resizeChat();
      }, 200);
    });
  }
  disableDateFlowbite();
});

window.addEventListener('resize', resizeChat);

// const fbShareIcons = document.querySelectorAll(
//   '.fb-share',
// ) as NodeListOf<HTMLAnchorElement>;
// fbShareIcons.forEach(fbIcon => {
//   fbIcon.addEventListener('click', () => {
//     const link = encodeURIComponent(window.location.href);
//     fbIcon.href = `https://www.facebook.com/share.php?u=${link}`;
//     console.log(fbIcon.href);
//   });
// });

// const instaShareIcons = document.querySelectorAll(
//   '.i-share',
// ) as NodeListOf<HTMLAnchorElement>;
// instaShareIcons.forEach(instaIcon => {
//   instaIcon.addEventListener('click', () => {
//     const link = encodeURIComponent(window.location.href);
//     instaIcon.href = `https://www.instagram.com`;
//     console.log(instaIcon.href);
//   });
// });

// const twitterShareIcons = document.querySelectorAll(
//   '.x-share',
// ) as NodeListOf<HTMLAnchorElement>;
// twitterShareIcons.forEach(twitterIcon => {
//   twitterIcon.addEventListener('click', () => {
//     const link = encodeURIComponent(window.location.href);
//     const text = encodeURIComponent(
//       'Check out cool tickets for sale on FanTicket',
//     );
//     const hashtags = encodeURIComponent('tickets,forsale');
//     twitterIcon.href = `https://twitter.com/share?url=${link}&text=${text}&hashtags=${hashtags}`;
//     console.log(twitterIcon.href);
//   });
// });

socialMediaShare();
