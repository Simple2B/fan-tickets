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

// export function unlockScroll() {
//   const scrollY = document.body.style.top;
//   document.body.style.position = '';
//   document.body.style.top = '';
//   document.body.style.left = '';
//   document.body.style.right = '';
//   window.scrollTo(0, parseInt(scrollY || '0') * -1);

//   console.log('unlock scroll');
// }

// export function lockScroll() {
//   document.body.style.position = 'fixed';
//   document.body.style.top = `-${window.scrollY}px`;
//   document.body.style.left = '0';
//   document.body.style.right = '0';

//   console.log('lock scroll');
// }

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
  const fixedMinDistance: number = 250;
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

  setTimeout(() => {
    if (chatWindow.offsetHeight > maxChatWindowHeight) {
      chatWindow.style.height = `${maxChatWindowHeight}px`;
    }
  }, 500);

  if (chatMain && chatFooter) {
    chatMain.style.height = `calc(100% - ${chatFooter.offsetHeight}px)`;
  }
}

export function lockScrollBody() {
  const screenWith: number = window.innerWidth;
  if (screenWith < 640) {
    document.body.style.position = 'fixed';
    document.body.style.top = `-${window.scrollY}px`;
    document.body.style.left = '0';
    document.body.style.right = '0';
  }
}

export function unlockScrollBody() {
  const screenWith: number = window.innerWidth;
  if (screenWith < 640) {
    const scrollY = document.body.style.top;
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    window.scrollTo(0, parseInt(scrollY || '0') * -1);
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

export function socialMediaShare() {
  const fbShareIcons = document.querySelectorAll(
    '.fb-share',
  ) as NodeListOf<HTMLAnchorElement>;
  fbShareIcons.forEach(fbIcon => {
    fbIcon.addEventListener('click', () => {
      const link = encodeURIComponent(window.location.href);
      fbIcon.href = `https://www.facebook.com/share.php?u=${link}`;
      console.log(fbIcon.href);
    });
  });

  const instaShareIcons = document.querySelectorAll(
    '.i-share',
  ) as NodeListOf<HTMLAnchorElement>;
  instaShareIcons.forEach(instaIcon => {
    instaIcon.addEventListener('click', () => {
      const link = encodeURIComponent(window.location.href);
      instaIcon.href = `https://www.instagram.com`;
      console.log(instaIcon.href);
    });
  });

  const twitterShareIcons = document.querySelectorAll(
    '.x-share',
  ) as NodeListOf<HTMLAnchorElement>;
  twitterShareIcons.forEach(twitterIcon => {
    twitterIcon.addEventListener('click', () => {
      const link = encodeURIComponent(window.location.href);
      const text = encodeURIComponent(
        'Check out cool tickets for sale on FanTicket',
      );
      const hashtags = encodeURIComponent('tickets,forsale');
      twitterIcon.href = `https://twitter.com/share?url=${link}&text=${text}&hashtags=${hashtags}`;
      console.log(twitterIcon.href);
    });
  });
}

export function disableDateFlowbite() {
  setTimeout(() => {
    const datePickers = document.querySelectorAll('.datepicker-picker');

    if (datePickers) {
      datePickers.forEach((datePicker: HTMLDivElement) => {
        setGreyDates(datePicker);
      });
    }

    const calendarButtons = document.querySelectorAll('.next-btn, .prev-btn');

    calendarButtons.forEach((button: HTMLButtonElement) => {
      button.addEventListener('click', (event: Event) => {
        const target = event.target as HTMLElement;
        const datePicker = target.closest(
          '.datepicker-picker',
        ) as HTMLDivElement;

        if (!datePicker) return;

        setGreyDates(datePicker);

        datePicker.addEventListener('DOMSubtreeModified', () => {
          setGreyDates(datePicker);
        });
      });
    });
  }, 1000);
}

function setGreyDates(datePicker: HTMLDivElement) {
  const monthTitle = datePicker.querySelector('.view-switch');
  const month = monthTitle.textContent.split(' ')[0];
  const year = monthTitle.textContent.split(' ')[1];
  const currentDate = new Date(`${month} 1, ${year}`).getMonth();
  const allDates = datePicker.querySelectorAll('.datepicker-cell');

  allDates.forEach((date: HTMLDivElement) => {
    const timeStamp = date.getAttribute('data-date');
    const dateMonth = new Date(parseInt(timeStamp)).getMonth();

    dateMonth !== currentDate
      ? (date.style.color = '#99a1a3')
      : (date.style.color = '#fff');
  });
}
