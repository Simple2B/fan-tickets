function addHiddenClass(element: HTMLElement) {
  element.classList.add('hidden');
}

function hideElements(
  event: MouseEvent,
  element: HTMLElement,
  otherElement?: HTMLElement[],
) {
  if (
    !element.contains(event.target as Node) &&
    !otherElement.some(el => el.contains(event.target as Node))
  ) {
    addHiddenClass(element);
  }
}

export function handleHideElements(
  element: HTMLElement,
  otherElement: HTMLElement[] = [],
) {
  element.classList.toggle('hidden');
  window.addEventListener('mouseup', (event: MouseEvent) => {
    hideElements(event, element, otherElement);
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      addHiddenClass(element);
    }
  });
}
