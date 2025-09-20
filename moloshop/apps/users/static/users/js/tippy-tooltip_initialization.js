
// apps/users/static/users/js/tippy-tooltip_initialization.js

// Подключаем кастомную тему стилей для Подсказок
//apps/core/static/core/scss/partials/_custom-tooltip.scss

document.addEventListener('DOMContentLoaded', function () {
  tippy('.tippy-tooltip', {
    theme: 'custom-tooltip',
    animation: 'scale',
    delay: [100, 100],
    arrow: true,
    placement: 'right',
    maxWidth: 260,
    interactive: false,
  });
});