
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

// Настройка загрузки файла
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

// Настройка удаления файла
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
});
