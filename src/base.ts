import 'flowbite';
import {toggleDropdown} from './utils';

const themeToggleDarkIcons = document.querySelectorAll(
  '#theme-toggle-dark-icon',
);
const themeToggleLightIcons = document.querySelectorAll(
  '#theme-toggle-light-icon',
);

// Change the icons inside the button based on previous settings
if (
  localStorage.getItem('color-theme') === 'dark' ||
  (!('color-theme' in localStorage) &&
    window.matchMedia('(prefers-color-scheme: dark)').matches)
) {
  themeToggleLightIcons.forEach(function (el) {
    el.classList.remove('hidden');
  });
  document.documentElement.classList.add('dark');
} else {
  themeToggleDarkIcons.forEach(function (el) {
    el.classList.remove('hidden');
  });
  document.documentElement.classList.remove('dark');
}

const themeToggleButtons = document.querySelectorAll('#theme-toggle');

themeToggleButtons.forEach(function (themeToggleBtn) {
  themeToggleBtn.addEventListener('click', function () {
    // toggle icons inside button
    themeToggleDarkIcons.forEach(function (themeToggleDarkIcon) {
      themeToggleDarkIcon.classList.toggle('hidden');
    });

    themeToggleLightIcons.forEach(function (themeToggleLightIcon) {
      themeToggleLightIcon.classList.toggle('hidden');
    });

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
      if (localStorage.getItem('color-theme') === 'light') {
        document.documentElement.classList.add('dark');
        localStorage.setItem('color-theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('color-theme', 'light');
      }

      // if NOT set via local storage previously
    } else {
      if (document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('color-theme', 'light');
      } else {
        document.documentElement.classList.add('dark');
        localStorage.setItem('color-theme', 'dark');
      }
    }
  });
});

// function to sticky header
const header = document.querySelector('.header');
// 20% of the viewport heights
const scrollPosition = 0.2 * window.innerHeight;
window.addEventListener('scroll', () => {
  header.classList.toggle('header-sticky', window.scrollY > 0);
});

// function to show and hide the scroll to top button
const scrollTopButton = document.querySelector('.footer-scroll-top');

window.addEventListener('scroll', () => {
  if (window.scrollY > scrollPosition) {
    scrollTopButton.classList.remove('scroll-top-anchor-close');
    scrollTopButton.classList.add('scroll-top-anchor-open');
  } else {
    scrollTopButton.classList.remove('scroll-top-anchor-open');
    scrollTopButton.classList.add('scroll-top-anchor-close');
  }
});

scrollTopButton.addEventListener('click', e => {
  e.preventDefault();
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  });
});

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

// header user dropdown
const headerUserDropdown = document.querySelector('#header-user-dropdown');
const headerUserDropdownButton = document.querySelector(
  '#header-user-dropdown-button',
);
const headerUserDropdownArrow = document.querySelector(
  '#header-user-dropdown-arrow',
);

headerUserDropdownButton.addEventListener('click', () => {
  toggleDropdown(headerUserDropdown as HTMLDivElement);
  headerUserDropdownArrow.classList.toggle('rotate-180');
  headerUserDropdown.classList.toggle('header-user-dropdown-open');
  headerUserDropdown.classList.toggle('header-user-dropdown-close');
});
