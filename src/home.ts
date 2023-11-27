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
