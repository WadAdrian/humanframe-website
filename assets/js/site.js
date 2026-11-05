(() => {
  const navigationToggle = document.querySelector('.nav-toggle');
  const navigation = document.querySelector('.site-nav');
  const header = document.querySelector('.site-header');

  if (navigationToggle && navigation && header) {
    const groups = [...navigation.querySelectorAll('.nav-group')];
    const closeGroups = (except = null) => {
      groups.forEach((group) => {
        if (group !== except) group.open = false;
      });
    };
    const closeNavigation = (restoreFocus = false) => {
      const wasOpen = navigation.classList.contains('is-open');
      navigation.classList.remove('is-open');
      navigationToggle.setAttribute('aria-expanded', 'false');
      navigationToggle.textContent = 'Menu';
      closeGroups();
      if (wasOpen && restoreFocus) navigationToggle.focus();
    };

    navigationToggle.addEventListener('click', () => {
      const open = navigation.classList.toggle('is-open');
      navigationToggle.setAttribute('aria-expanded', String(open));
      navigationToggle.textContent = open ? 'Close' : 'Menu';
    });
    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a')) closeNavigation();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key !== 'Escape') return;
      const openGroup = groups.find((group) => group.open);
      if (openGroup) {
        closeGroups();
        openGroup.querySelector('summary')?.focus();
      } else {
        closeNavigation(true);
      }
    });
    document.addEventListener('click', (event) => {
      if (!header.contains(event.target)) closeNavigation();
    });
    groups.forEach((group) => {
      group.addEventListener('toggle', () => {
        if (group.open) closeGroups(group);
      });
    });
    const desktopNavigation = window.matchMedia('(min-width: 901px)');
    const resetNavigation = () => closeNavigation();
    if (desktopNavigation.addEventListener) {
      desktopNavigation.addEventListener('change', resetNavigation);
    } else {
      desktopNavigation.addListener(resetNavigation);
    }
    window.addEventListener('resize', resetNavigation, { passive: true });
    document.documentElement.classList.add('navigation-ready');
  }

  const inquiryForm = document.querySelector('[data-inquiry-form]');
  const inquiryPreview = document.querySelector('[data-inquiry-preview]');
  const inquiryBody = document.querySelector('[data-inquiry-body]');
  const inquiryEmail = document.querySelector('[data-inquiry-email]');

  if (inquiryForm && inquiryPreview && inquiryBody && inquiryEmail) {
    const clearDraft = () => {
      inquiryPreview.hidden = true;
      inquiryBody.textContent = '';
      inquiryEmail.href = 'mailto:humanframerobotics@gmail.com';
    };

    inquiryForm.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!inquiryForm.reportValidity()) return;
      const data = new FormData(inquiryForm);
      const value = (name) => String(data.get(name) || '').trim();
      const subject = `HumanFrame ${value('interest')} — ${value('institution')}`;
      const body = [
        'Hello HumanFrame,', '',
        `Name: ${value('name')}`,
        `Email: ${value('email')}`,
        `Institution / organization: ${value('institution')}`,
        `Topic: ${value('interest')}`, '',
        'Research interests and proposed collaboration:',
        value('message'), '',
      ].join('\n');
      inquiryBody.textContent = body;
      inquiryEmail.href = `mailto:humanframerobotics@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      inquiryPreview.hidden = false;
      document.querySelector('#draft-title')?.focus();
    });
    inquiryForm.addEventListener('input', clearDraft);
    inquiryForm.addEventListener('change', clearDraft);
    inquiryForm.addEventListener('reset', clearDraft);
    if (new URLSearchParams(window.location.search).get('interest') === 'research') {
      inquiryForm.elements.namedItem('interest').value = 'Research collaboration';
    }
    inquiryForm.hidden = false;
  }
})();
