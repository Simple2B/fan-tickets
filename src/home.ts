document.addEventListener('DOMContentLoaded', () => {
  // function to limit the number of events shown on the home page for mobile devices
  const eventContainer = document.querySelector('#home-event-container');
  const eventItems = eventContainer.querySelectorAll('.event-item');
  const limitEventItems = 4;
  const toggleScreenSize = 1024;

  function showLimitEvents() {
    const screenWidth = window.innerWidth;
    const maxVisibleItems =
      screenWidth < toggleScreenSize ? limitEventItems : eventItems.length;

    eventItems.forEach((item, index) => {
      index < maxVisibleItems
        ? item.classList.remove('hidden')
        : item.classList.add('hidden');
    });
  }

  showLimitEvents();
  window.addEventListener('resize', showLimitEvents);

  // function to sticky header
  const header = document.querySelector('.header');
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
});
