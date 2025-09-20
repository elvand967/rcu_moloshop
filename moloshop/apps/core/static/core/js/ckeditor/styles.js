// подключаем Стилизацию изображений для WYSIWYG-редактора CKEditor

CKEDITOR.stylesSet.add('custom_styles', [
  {
    name: 'Адаптивное изображение',
    element: 'img',
    attributes: { 'class': 'img-fluid' }
  },
  {
    name: 'Выравнивание слева',
    element: 'img',
    attributes: { 'class': 'img-left' }
  },
  {
    name: 'Выравнивание справа',
    element: 'img',
    attributes: { 'class': 'img-right' }
  },
  {
    name: 'По центру',
    element: 'img',
    attributes: { 'class': 'img-center' }
  },
  {
    name: 'Hover-увеличение',
    element: 'img',
    attributes: { 'class': 'img-hover-zoom' }
  },
  {
    name: 'Lightbox',
    element: 'img',
    attributes: { 'class': 'lightbox' }
  }
]);
