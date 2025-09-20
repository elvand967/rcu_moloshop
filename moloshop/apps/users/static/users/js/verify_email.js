
//apps/users/static/users/js/verify_email.js
// Управление в шаблоне verify_email.html

document.addEventListener('DOMContentLoaded', function () {
  const link = document.getElementById('resend-code-link');
  link.addEventListener('click', function (e) {
    e.preventDefault();
    if (link.classList.contains('loading')) return; // предотвратить множественные клики
    link.classList.add('loading');
    const originalText = link.textContent;
    link.textContent = 'Отправляем...';
    fetch(link.href, {method: 'POST', headers: {'X-CSRFToken': getCookie('csrftoken')}})
      .then(response => {
        if (response.ok) {
          link.textContent = 'Код отправлен!';
          link.classList.add('sent');
          setTimeout(() => {
            link.textContent = originalText;
            link.classList.remove('loading', 'sent');
          }, 5000);
        } else {
          link.textContent = 'Ошибка отправки, попробуйте снова';
          link.classList.remove('loading');
        }
      })
      .catch(() => {
        link.textContent = 'Ошибка отправки, проверьте интернет';
        link.classList.remove('loading');
      });

    // Функция для чтения csrf токена из куки
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
});