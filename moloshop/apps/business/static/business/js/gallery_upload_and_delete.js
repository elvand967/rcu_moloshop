
// apps/business/static/business/js/gallery_upload_and_delete.js

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
  const mediaId = button.getAttribute("data-media-id");

  const galleryPreview = button.closest(".gallery-preview");
  const businessSlug = galleryPreview.dataset.businessSlug;
  const modelSlug = galleryPreview.dataset.modelSlug;
  const modelType = galleryPreview.dataset.modelType;

  Swal.fire({
    title: "Удалить изображение?",
    text: "Это действие нельзя будет отменить",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Да, удалить",
    cancelButtonText: "Отмена",
    confirmButtonColor: "#e74c3c",
    cancelButtonColor: "#6c757d",
    reverseButtons: true,
    focusCancel: true,  // Активная кнопка "Отмена"
  }).then((result) => {
    if (result.isConfirmed) {
      fetch(
        `/business/${businessSlug}/${modelType}/${modelSlug}/gallery/delete/${mediaId}/`,
        {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "X-Requested-With": "XMLHttpRequest",
          },
          credentials: "same-origin",
        }
      )
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            const itemElem = document.getElementById(`gallery-item-${mediaId}`);
            if (itemElem) itemElem.remove();
            Swal.fire("Удалено!", "Изображение удалено.", "success");
          } else {
            Swal.fire("Ошибка", data.error || "Не удалось удалить изображение", "error");
          }
        })
        .catch(() =>
          Swal.fire("Ошибка", "Ошибка сети при удалении изображения", "error")
        );
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // Назначаем обработчик удаления для существующих кнопок
  document.querySelectorAll(".btn-delete-image").forEach((button) => {
    button.addEventListener("click", deleteImageHandler);
  });

  // Обработка загрузки изображений галереи (несколько форм на странице)
  document.querySelectorAll("form[id^='gallery_upload_form_']").forEach((form) => {
    const fileInput = form.querySelector('input[type="file"]');
    const uploadUrl = form.dataset.uploadUrl;
    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const galleryPreview = form.previousElementSibling; // div.gallery-preview
    const selectBtn = form.querySelector("button");

    // Отслеживаем клик на кнопку "Загрузить изображение"
    selectBtn.addEventListener("click", () => {
      fileInput.click();
    });

    fileInput.addEventListener("change", async () => {
      const file = fileInput.files[0];
      if (!file) return;

      const fd = new FormData();
      fd.append("image", file);
      fd.append("csrfmiddlewaretoken", csrfToken);

      try {
        const response = await fetch(uploadUrl, {
          method: "POST",
          body: fd,
        });
        const data = await response.json();

        if (data.success) {
          // Создаем новый элемент галереи с изображением и кнопкой удаления
          const newItem = document.createElement("div");
          newItem.classList.add("gallery-item");
          newItem.id = `gallery-item-${data.media_id}`;
          newItem.innerHTML = `
            <img src="${data.url}" alt="" class="gallery-img">
            <button type="button" class="btn btn-sm btn-danger btn-delete-image" data-media-id="${data.media_id}">Удалить</button>
          `;

          galleryPreview.appendChild(newItem);

          // Назначаем обработчик удаления на новую кнопку
          newItem.querySelector(".btn-delete-image").addEventListener("click", deleteImageHandler);
        } else {
          Swal.fire("Ошибка загрузки", data.error || "Неизвестная ошибка", "error");
        }
      } catch (error) {
        Swal.fire("Ошибка сети", "Ошибка при загрузке изображения", "error");
      } finally {
        fileInput.value = "";
      }
    });
  });
});