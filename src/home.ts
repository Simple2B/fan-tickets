document.addEventListener('DOMContentLoaded', () => {
  const eventContainer: HTMLDivElement = document.querySelector(
    '#home-event-container',
  );
  const eventItems = eventContainer.querySelectorAll('.event-item');
  // limit the number of events shown on the home page for mobile devices
  const limitEventItems = 4;
  const toggleScreenSize = 1024;

  // function to limit the number of events shown on the home page for mobile devices
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

  // function to set correct width for event image
  function setEventImageWidth() {
    const eventImage: HTMLImageElement = document.querySelector(
      '#home-event-left-image',
    );
    const eventHeaderContainer: HTMLDivElement = document.querySelector(
      '#home-event-header-container',
    );
    const eventHeaderPosition =
      eventHeaderContainer.getBoundingClientRect().left;
    // 60 is the distance between the event image and the event header as in the design
    const distanceBetweenElements = 60;

    eventImage.style.width = `${
      eventHeaderPosition - distanceBetweenElements
    }px`;
  }

  setEventImageWidth();
  showLimitEvents();
  window.addEventListener('resize', showLimitEvents);

  // TODO: delete it if client accepts slider not from design
  // function to set middle scroll position for modules
  const scrollContainers = document.querySelectorAll('.scroll-x-modules');

  scrollContainers.forEach((scrollContainer: HTMLDivElement) => {
    let totalModulesWidth = 0;
    const modules: HTMLCollection = scrollContainer.children;
    for (let i = 0; i < modules.length; i++) {
      totalModulesWidth += (modules[i] as HTMLDivElement)['offsetWidth'];
    }
    scrollContainer.scrollLeft = (totalModulesWidth - window.innerWidth) / 2;
  });
});
