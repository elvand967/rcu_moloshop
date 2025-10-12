
// apps/business/static/business/js/confirm_delete.js

function confirmDeleteItem(type, slug, title) {
    let formId = 'delete-' + type + '-' + slug;

    Swal.fire({
        title: 'Вы уверены?',
        text: `Вы хотите удалить ${type === 'goods' ? 'товар' : 'услугу'} «${title}»?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Да, удалить',
        cancelButtonText: 'Отмена',
        reverseButtons: true,
        focusCancel: true,
        background: '#f9f9f9',
        color: '#333',
        iconColor: '#e74c3c',
        confirmButtonColor: '#e74c3c',
        cancelButtonColor: '#6c757d',
        customClass: {
            popup: 'rounded-xl shadow-md',
            confirmButton: 'px-4 py-2',
            cancelButton: 'px-4 py-2',
        },
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById(formId).submit();
        }
    });
}