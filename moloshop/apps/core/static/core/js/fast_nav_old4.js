// moloshop/apps/core/static/core/js/fast_nav.js

function isElementVisible(el) {
    if (!el) return false;
    const rect = el.getBoundingClientRect();
    // Считаем элемент видимым, если хотя бы часть его видна во viewport
    return rect.top < window.innerHeight && rect.bottom > 0;
}

function updateFastScrollNav() {
    const header = document.querySelector('header');
    const footer = document.querySelector('footer');
    const nav = document.querySelector('.fast-scroll-nav');
    const upBtn = nav ? nav.querySelector('.fast-scroll-btn.up') : null;
    const downBtn = nav ? nav.querySelector('.fast-scroll-btn.down') : null;

    if (!nav || !upBtn || !downBtn) return;

    // Блок всегда прижат к низу экрана
    nav.classList.add('position-fixed');
    nav.style.left = '0';
    nav.style.right = '0';
    nav.style.bottom = '0';
    nav.style.zIndex = '100';

    // Проверяем видимость header и footer
    const headerVisible = isElementVisible(header);
    const footerVisible = isElementVisible(footer);

    // 1. Видна верхняя граница <header> и нижняя граница </footer> — блок скрыт
    if (headerVisible && footerVisible) {
        nav.classList.add('d-none');
    } else {
        nav.classList.remove('d-none');
        // 2. Видна нижняя граница </header>, не видна нижняя граница </footer> — только вверх
        if (headerVisible && !footerVisible) {
            upBtn.classList.add('d-none');
            downBtn.classList.remove('d-none');
        }
        // 3. Не видна ни </header>, ни </footer> — обе кнопки
        else if (!headerVisible && !footerVisible) {
            upBtn.classList.remove('d-none');
            downBtn.classList.remove('d-none');
        }
        // 4. Видна верхняя граница <footer>, не видна </header> — только вверх
        else if (footerVisible && !headerVisible) {
            upBtn.classList.remove('d-none');
            downBtn.classList.add('d-none');
        }
    }
}

window.addEventListener('scroll', updateFastScrollNav, {passive: true});
window.addEventListener('resize', updateFastScrollNav);
document.addEventListener('DOMContentLoaded', updateFastScrollNav);

// Действия кнопок
document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('.fast-scroll-nav');
    if (!nav) return;
    const upBtn = nav.querySelector('.fast-scroll-btn.up');
    const downBtn = nav.querySelector('.fast-scroll-btn.down');

    if (upBtn) {
        upBtn.onclick = function() {
            document.querySelector('header').scrollIntoView({behavior: 'smooth'});
        };
    }
    if (downBtn) {
        downBtn.onclick = function() {
            document.querySelector('footer').scrollIntoView({behavior: 'smooth'});
        };
    }
});
