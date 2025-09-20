
// apps/users/static/users/js/loading_avatar.js

// При нажатии на кнопку "Изменить" открывается диалог выбора файла.
// Если файл выбран — происходит отправка формы.
// Если пользователь нажимает "Отмена" — событие change не срабатывает (или файлы не выбираются), и форма не отправляется.

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

document.getElementById('select_avatar_btn').addEventListener('click', function() {
  document.getElementById('id_avatar_file').click();
});

document.getElementById('id_avatar_file').addEventListener('change', function() {
  if(this.files.length > 0) {
    const formData = new FormData();
    formData.append('avatar_file', this.files[0]);
    fetch('/users/profile/upload-avatar/', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      body: formData,
    }).then(response => {
      if(response.ok) {
        location.reload();
      } else {
        alert("Ошибка загрузки аватара");
      }
    });
  }
});