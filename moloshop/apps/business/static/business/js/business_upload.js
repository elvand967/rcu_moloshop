// apps/business/static/business/js/business_upload.js

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
      headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
      body: formData,
      credentials: "same-origin",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success && data.url) preview.src = data.url;
        else alert(data.error || "Не удалось загрузить файл");
      })
      .catch((err) => {
        console.error(err);
        alert("Ошибка при загрузке файла");
      });
  });
}

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
      headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken") },
      credentials: "same-origin",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) preview.src = placeholderUrl;
        else alert(data.error || "Не удалось удалить файл");
      })
      .catch((err) => {
        console.error(err);
        alert("Ошибка при удалении файла");
      });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupUpload("select_logo_btn", "id_logo_file", "logo_upload_form", "logo_preview");
  setupDelete("delete_logo_btn", "logo_upload_form", "logo_preview", STATIC_URL + "business/images/placeholder.jpg");

  setupUpload("select_favicon_btn", "id_favicon_file", "favicon_upload_form", "favicon_preview");
  setupDelete("delete_favicon_btn", "favicon_upload_form", "favicon_preview", STATIC_URL + "business/images/placeholder.jpg");
});

