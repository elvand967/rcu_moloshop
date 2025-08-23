
// Показываем/скрываем подменю по стрелке только на мобильных

document.addEventListener('DOMContentLoaded', function () {
  function isMobile() {
    return window.matchMedia('(max-width: 835px)').matches;
  }

  document.querySelectorAll('.menu-item.has-dropdown').forEach(function(menuItem) {
    const toggleBtn = menuItem.querySelector('.dropdown-toggle');
    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', function (e) {
      if (!isMobile()) return; // Только для мобильных!
      e.preventDefault();
      const isOpen = menuItem.classList.contains('submenu-open');
      if (isOpen) {
        menuItem.classList.remove('submenu-open');
        toggleBtn.setAttribute('aria-expanded', 'false');
      } else {
        // Закрыть другие открытые подменю
        document.querySelectorAll('.menu-item.has-dropdown.submenu-open').forEach(function (other) {
          if (other !== menuItem) {
            other.classList.remove('submenu-open');
            const otherToggle = other.querySelector('.dropdown-toggle');
            if (otherToggle) otherToggle.setAttribute('aria-expanded', 'false');
          }
        });
        menuItem.classList.add('submenu-open');
        toggleBtn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // Закрывать все подменю по клику вне навбара
  document.addEventListener('click', function (e) {
    if (!isMobile()) return;
    const nav = document.querySelector('.navbar');
    if (nav && !nav.contains(e.target)) {
      document.querySelectorAll('.menu-item.has-dropdown.submenu-open').forEach(function (item) {
        item.classList.remove('submenu-open');
        const toggle = item.querySelector('.dropdown-toggle');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      });
    }
  });
});
