console.log('socialMedia.ts');
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

const tiktokShareIcons = document.querySelectorAll(
  '.tiktok-share',
) as NodeListOf<HTMLAnchorElement>;
tiktokShareIcons.forEach(tiktokIcon => {
  tiktokIcon.addEventListener('click', () => {
    const link = encodeURIComponent(window.location.href);
    const text = encodeURIComponent(
      'Check out cool tickets for sale on FanTicket',
    );
    const hashtags = encodeURIComponent('tickets,forsale');
    tiktokIcon.href = `https://tiktok.com/`;
    console.log(tiktokIcon.href);
  });
});
