// moloshop/apps/core/static/core/js/fast_nav.js

// Проверка, виден ли элемент хотя бы частично во viewport
function isElementVisible(el) {
    if (!el) return false;
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom > 0;
}

// Обновление состояния блока fast scroll nav
function updateFastScrollNav() {
    const header = document.querySelector('header');
    const footer = document.querySelector('footer');
    const navFixed = document.querySelector('.fast-scroll-nav-fixed');
    if (!navFixed) return;

    const nav = navFixed.querySelector('.fast-scroll-nav');
    const upBtn = nav.querySelector('.fast-scroll-btn.up');
    const downBtn = nav.querySelector('.fast-scroll-btn.down');

    const headerVisible = isElementVisible(header);
    const footerVisible = isElementVisible(footer);

    // 1. Скрываем полностью, если видны и header, и footer
    if (headerVisible && footerVisible) {
        navFixed.classList.add('d-none');
    } else {
        navFixed.classList.remove('d-none');

        // 2. Виден только header (верхняя граница) → показываем только вниз
        if (headerVisible && !footerVisible) {
            upBtn.classList.add('d-none');
            downBtn.classList.remove('d-none');
        }
        // 3. Не видны ни header, ни footer → показываем обе кнопки
        else if (!headerVisible && !footerVisible) {
            upBtn.classList.remove('d-none');
            downBtn.classList.remove('d-none');
        }
        // 4. Виден footer, не виден header → показываем только вверх
        else if (footerVisible && !headerVisible) {
            upBtn.classList.remove('d-none');
            downBtn.classList.add('d-none');
        }
    }
}

// Скролл по кнопкам
function setupFastScrollButtons() {
    const navFixed = document.querySelector('.fast-scroll-nav-fixed');
    if (!navFixed) return;

    const nav = navFixed.querySelector('.fast-scroll-nav');
    const upBtn = nav.querySelector('.fast-scroll-btn.up');
    const downBtn = nav.querySelector('.fast-scroll-btn.down');

    if (upBtn) {
        upBtn.onclick = () => {
            const header = document.querySelector('header');
            if (header) header.scrollIntoView({behavior: 'smooth'});
        };
    }

    if (downBtn) {
        downBtn.onclick = () => {
            const footer = document.querySelector('footer');
            if (footer) footer.scrollIntoView({behavior: 'smooth'});
        };
    }
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    updateFastScrollNav();
    setupFastScrollButtons();

    window.addEventListener('scroll', updateFastScrollNav, {passive: true});
    window.addEventListener('resize', updateFastScrollNav);
});

