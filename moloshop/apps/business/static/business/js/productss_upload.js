
// apps/business/static/business/js/productss_upload.js

/*
Этот JS работает с множеством форм (по одной на каждую услугу).
По выбору файла отправляет AJAX для загрузки, обновляет превью с защитой от кеша.
При удалении обложки показывает SweetAlert2 подтверждение,
после удаления меняет превью на плейсхолдер.
Обрабатывает CSRF, ошибки сети и ответы.
*/

document.addEventListener("DOMContentLoaded", () => {
  const uploadForms = document.querySelectorAll(".service-image-upload-form");

  uploadForms.forEach((form) => {
    const fileInput = form.querySelector(".service-image-file");
    const selectBtn = form.querySelector(".select-service-image-btn");
    const deleteBtn = form.querySelector(".delete-service-image-btn");
    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;

    // Кнопка "Загрузить обложку" → открываем диалог выбора файла
    selectBtn?.addEventListener("click", () => fileInput.click());

    // Обработка выбора файла и загрузка через fetch
    fileInput?.addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const uploadUrl = form.dataset.uploadUrl;
      const formData = new FormData();
      formData.append("image", file);
      formData.append("csrfmiddlewaretoken", csrfToken);

      try {
        const response = await fetch(uploadUrl, {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (data.success) {
          const container = form.closest(".accordion-body") || form.parentElement;
          const preview = container.querySelector(".service-image-preview");
          if (preview) {
            preview.src = data.url + "?v=" + new Date().getTime(); // защита от кеша
          }
        } else {
          Swal.fire({
            icon: "error",
            title: "Ошибка загрузки",
            text: data.error || "Не удалось загрузить изображение",
          });
        }
      } catch (err) {
        console.error("Ошибка при загрузке:", err);
        Swal.fire({
          icon: "error",
          title: "Ошибка сети",
          text: "Не удалось загрузить изображение",
        });
      } finally {
        fileInput.value = ""; // очищаем input
      }
    });

    // Кнопка "Удалить обложку" с SweetAlert2 подтверждением
    deleteBtn?.addEventListener("click", async () => {
      const deleteUrl = form.dataset.deleteUrl;
      const result = await Swal.fire({
        title: 'Удалить обложку услуги?',
        text: "Это действие нельзя будет отменить",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e74c3c',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Да, удалить',
        cancelButtonText: 'Отмена',
        reverseButtons: true,
        focusCancel: true,  // ставит фокус на кнопку отмены при открытии
      });

      if (result.isConfirmed) {
        try {
          const response = await fetch(deleteUrl, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },
          });

          const data = await response.json();

          if (data.success) {
            const container = form.closest(".accordion-body") || form.parentElement;
            const preview = container.querySelector(".service-image-preview");
            if (preview) {
              preview.src = "/static/business/images/placeholder.jpg";
            }
            Swal.fire('Удалено!', 'Обложка успешно удалена.', 'success');
          } else {
            Swal.fire('Ошибка', data.error || 'Не удалось удалить изображение', 'error');
          }
        } catch (err) {
          console.error("Ошибка при удалении:", err);
          Swal.fire('Ошибка', 'Ошибка при удалении изображения', 'error');
        }
      }
    });

  });
});

