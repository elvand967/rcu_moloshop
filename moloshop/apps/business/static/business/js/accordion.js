
// apps/business/static/business/js/accordion.js

document.addEventListener("DOMContentLoaded", function() {
  const headers = document.querySelectorAll(".accordion-header");

  headers.forEach(header => {
    header.addEventListener("click", (event) => {
      // Проверяем, не кликнули ли по кнопке удаления (или другому интерактивному элементу),
      // чтобы не переключать аккордеон при клике туда
      if (event.target.closest(".btn-delete") || event.target.closest(".btn-delete-image") || event.target.closest("button")) {
        return;
      }

      const isActive = header.classList.contains("active");
      const body = header.nextElementSibling;

      if (isActive) {
        // Закрываем текущий открытый блок
        header.classList.remove("active");
        header.querySelector(".toggle-icon").classList.remove("active");
        body.style.maxHeight = null;
        body.style.paddingTop = "0";
        body.style.paddingBottom = "0";
      } else {
        // Закрываем все остальные
        headers.forEach(h => {
          h.classList.remove("active");
          h.querySelector(".toggle-icon").classList.remove("active");
          const b = h.nextElementSibling;
          b.style.maxHeight = null;
          b.style.paddingTop = "0";
          b.style.paddingBottom = "0";
        });
        // Открываем текущий
        header.classList.add("active");
        header.querySelector(".toggle-icon").classList.add("active");
        body.style.maxHeight = (body.scrollHeight + 20) + "px";
        body.style.paddingTop = "1rem";
        body.style.paddingBottom = "1rem";
      }
    });
  });

  {% if active_service_id %}
  const activeItem = document.querySelector(`.accordion-item[data-service-id="{{ active_service_id }}"]`);
  if(activeItem){
    const activeHeader = activeItem.querySelector(".accordion-header");
    const activeBody = activeHeader.nextElementSibling;
    activeHeader.classList.add("active");
    activeHeader.querySelector(".toggle-icon").classList.add("active");
    activeBody.style.maxHeight = (activeBody.scrollHeight + 20) + "px";
    activeBody.style.paddingTop = "1rem";
    activeBody.style.paddingBottom = "1rem";
  }
  {% endif %}
});
