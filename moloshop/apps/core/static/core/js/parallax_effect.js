
document.addEventListener('DOMContentLoaded', function() {
  const header = document.querySelector('.hero-parallax');
  if (!header) return;

  // Настроим "коэффициент замедления" (чем больше, тем медленнее фон)
  const slowdown = 1.5;

  function parallaxScroll() {
    // Сколько пользователь проскроллил страницу
    const scrolled = window.pageYOffset || document.documentElement.scrollTop;
    // Смещение фона считается делением прокрутки на slowdown
    header.style.backgroundPosition = `center ${-(scrolled / slowdown)}px`;
  }

  window.addEventListener('scroll', parallaxScroll, { passive: true });
});

