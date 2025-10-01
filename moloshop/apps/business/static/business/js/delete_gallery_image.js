function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (const cookie of cookies) {
      const c = cookie.trim();
      if (c.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(c.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function deleteImageHandler(event) {
  const button = event.currentTarget;
  const mediaId = button.getAttribute('data-media-id');

  // Получаем атрибуты из родительского блока gallery-preview
  const galleryPreview = button.closest('.gallery-preview');
  const businessSlug = galleryPreview.dataset.businessSlug;
  const modelSlug = galleryPreview.dataset.modelSlug;
  const modelType = galleryPreview.dataset.modelType;

  if (!confirm('Удалить изображение?')) return;

  fetch(`/business/${businessSlug}/${modelType}/${modelSlug}/gallery/delete/${mediaId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'X-Requested-With': 'XMLHttpRequest'
    },
    credentials: 'same-origin'
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      // Удаляем элемент с изображением из DOM
      const itemElem = document.getElementById(`gallery-item-${mediaId}`);
      if (itemElem) itemElem.remove();
    } else {
      alert(data.error || 'Ошибка при удалении изображения');
    }
  })
  .catch(() => alert('Ошибка сети при удалении изображения'));
}

// Инициализация: назначаем обработчики на все кнопки удаления
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.btn-delete-image').forEach(button => {
    button.addEventListener('click', deleteImageHandler);
  });
});
