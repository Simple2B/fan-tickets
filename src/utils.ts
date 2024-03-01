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
  const chatMain: HTMLElement = document.querySelector('#chat-body');
  const chatFooter: HTMLElement = document.querySelector('#chat-footer');
  const chatWindow: HTMLElement = document.querySelector('#chat-window');
  const screenWith: number = window.innerWidth;
  const headerBottom: number = header.offsetTop + header.offsetHeight;
  const chatWindowTop: number = chatWindow.offsetTop;
  const fixedMinDistance: number = 220;
  const maxChatWindowHeight: number = 650;
  const availableSpace: number = chatWindowTop - headerBottom;

  if (screenWith < 640) {
    chatMain.style.height = `calc(100% - ${chatFooter.offsetHeight}px)`;
    return;
  }

  if (!header || !chatWindow) return;

  if (availableSpace < fixedMinDistance) {
    chatWindow.style.height = `calc(100vh - ${fixedMinDistance}px)`;
  }
  if (chatWindow.offsetHeight > maxChatWindowHeight) {
    chatWindow.style.height = `${maxChatWindowHeight}px`;
  }

  if (chatMain && chatFooter) {
    chatMain.style.height = `calc(100% - ${chatFooter.offsetHeight}px)`;
  }
}

export function scrollDown(element: HTMLDivElement) {
  element.scrollTo({
    top: element.scrollHeight,
  });
}

const scrollAnimationDuration = 200;
export function scrollDownSmooth(element: HTMLDivElement) {
  setTimeout(() => {
    element.scrollTo({
      top: element.scrollHeight,
      behavior: 'smooth',
    });
  }, scrollAnimationDuration);
}
