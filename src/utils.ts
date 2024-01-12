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

export function resizeChat() {
  const header: HTMLElement = document.querySelector('.header');
  const chatWindow: HTMLElement = document.querySelector('#chat-window');
  const headerBottom: number = header.offsetTop + header.offsetHeight;
  const chatWindowTop: number = chatWindow.offsetTop;
  const fixedMinDistance: number = 200;
  const maxChatWindowHeight: number = 475;
  const availableSpace: number = chatWindowTop - headerBottom;

  if (availableSpace < fixedMinDistance) {
    chatWindow.style.height = `calc(100vh - ${fixedMinDistance}px)`;
  }
  if (chatWindow.offsetHeight > maxChatWindowHeight) {
    chatWindow.style.height = `${maxChatWindowHeight}px`;
  }
}
