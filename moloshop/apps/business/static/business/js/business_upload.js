
// apps/business/static/business/js/business_upload.js

// Получение значения cookie по имени
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

// Настройка загрузки файла (одиночного) с предпросмотром (логотип, обложки)
function setupUpload(buttonId, inputId, formId, previewId) {
  const button = document.getElementById(buttonId);
  const input = document.getElementById(inputId);
  const preview = document.getElementById(previewId);
  const form = document.getElementById(formId);
  const uploadUrl = form?.dataset.uploadUrl;

  if (!button || !input || !preview || !form || !uploadUrl) return;

  button.addEventListener("click", () => input.click());

  input.addEventListener("change", () => {
    if (!input.files.length) return;

    const formData = new FormData(form);
    formData.append(input.name, input.files[0]);

    fetch(uploadUrl, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: formData,
      credentials: "same-origin",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success && data.url) {
          // Добавляем timestamp к URL для обхода кеша
          preview.src = data.url + "?t=" + new Date().getTime();
        } else {
          alert(data.error || "Не удалось загрузить файл");
        }
      })
      .catch((err) => {
        console.error(err);
        alert("Ошибка при загрузке файла");
      });
  });
}

// Настройка удаления файла (одиночного) с предпросмотром (логотип, обложки)
function setupDelete(buttonId, formId, previewId, placeholderUrl) {
  const button = document.getElementById(buttonId);
  const form = document.getElementById(formId);
  const preview = document.getElementById(previewId);
  const deleteUrl = form?.dataset.deleteUrl;

  if (!button || !form || !preview || !deleteUrl) return;

  button.addEventListener("click", (e) => {
    e.preventDefault();
    fetch(deleteUrl, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: "same-origin",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          preview.src = placeholderUrl + "?t=" + new Date().getTime();
        } else {
          alert(data.error || "Не удалось удалить файл");
        }
      })
      .catch((err) => {
        console.error(err);
        alert("Ошибка при удалении файла");
      });
  });
}

// Функция-обработчик удаления отдельного изображения галереи
function deleteImageHandler(event) {
  const button = event.currentTarget;
  const mediaId = button.getAttribute('data-media-id');
  const businessSlug = button.closest('[data-business-slug]').dataset.businessSlug;
  const modelSlug = button.closest('[data-model-slug]').dataset.modelSlug;
  const modelType = button.closest('[data-model-type]').dataset.modelType;

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
      button.parentElement.remove();
    } else {
      alert(data.error || 'Ошибка при удалении изображения');
    }
  })
  .catch(() => alert('Ошибка сети при удалении изображения'));
}

// Настройка удаления изображений галереи (множественной)
function setupGalleryDelete() {
  document.querySelectorAll('.btn-delete-image').forEach(button => {
    button.addEventListener('click', deleteImageHandler);
  });
}

// Настройка загрузки изображений галереи (множественной)
function setupGalleryUpload(buttonId, inputId, galleryContainerId, formId) {
  const button = document.getElementById(buttonId);
  const input = document.getElementById(inputId);
  const gallery = document.getElementById(galleryContainerId);
  const form = document.getElementById(formId);
  const uploadUrl = form?.dataset.uploadUrl;

  if (!button || !input || !gallery || !form || !uploadUrl) return;

  button.addEventListener('click', () => input.click());

  input.addEventListener('change', () => {
    if (!input.files.length) return;

    const formData = new FormData(form);
    for (const file of input.files) {
      formData.set('image', file);

      fetch(uploadUrl, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData,
        credentials: 'same-origin',
      })
      .then(res => res.json())
      .then(data => {
        console.log('Server response:', data);
        if (data.success) {
          const div = document.createElement('div');
          div.style.display = 'inline-block';
          div.style.marginRight = '10px';
          div.style.position = 'relative';
          div.innerHTML = `
            <img src="${data.url}" style="max-width: 100px; max-height: 100px; object-fit: cover; border: 1px solid #ccc; padding: 2px;">
            <button type="button" class="btn btn-sm btn-danger btn-delete-image" data-media-id="${data.media_id}">Удалить</button>
          `;
          gallery.appendChild(div);
          div.querySelector('.btn-delete-image').addEventListener('click', deleteImageHandler);
        } else {
          alert(data.error || 'Ошибка загрузки изображения');
        }
      })
      .catch(() => alert('Ошибка сети при загрузке изображения'));
    }
  });
}


// Инициализация после загрузки страницы
document.addEventListener("DOMContentLoaded", () => {
  // Логотип
  setupUpload("select_logo_btn", "id_logo_file", "logo_upload_form", "logo_preview");
  setupDelete("delete_logo_btn", "logo_upload_form", "logo_preview", STATIC_URL + "business/images/placeholder.jpg");

  // Фавикон
  setupUpload("select_favicon_btn", "id_favicon_file", "favicon_upload_form", "favicon_preview");
  setupDelete("delete_favicon_btn", "favicon_upload_form", "favicon_preview", STATIC_URL + "business/images/placeholder.jpg");

  // Обложка товара
  setupUpload("select_product_image_btn", "id_product_image_file", "product_image_upload_form", "product_image_preview");
  setupDelete("delete_product_image_btn", "product_image_upload_form", "product_image_preview", STATIC_URL + "business/images/placeholder.jpg");

  // Обложка услуги
  setupUpload("select_service_image_btn", "id_service_image_file", "service_image_upload_form", "service_image_preview");
  setupDelete("delete_service_image_btn", "service_image_upload_form", "service_image_preview", STATIC_URL + "business/images/placeholder.jpg");

  // Инициализация галерей с множественной загрузкой/удалением
  document.querySelectorAll('.gallery-preview').forEach(gallery => {
    const slug = gallery.dataset.modelSlug;

    setupGalleryDelete(); // Можно оставить один раз, если все кнопки удаления имеют общий класс

    // Формируем id с учетом slug
    const buttonId = `select_gallery_image_btn_${slug}`;
    const inputId = `id_gallery_image_file_${slug}`;
    const galleryContainerId = `gallery_preview_${slug}`;
    const formId = `gallery_upload_form_${slug}`;

    setupGalleryUpload(buttonId, inputId, galleryContainerId, formId);
  });
});
