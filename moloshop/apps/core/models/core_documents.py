
# ../apps/core/models/core_documents.py

from django.db import models
from .abstract import SlugNamespaceModel
from ckeditor_uploader.fields import RichTextUploadingField


class ContractsInstructions(SlugNamespaceModel):
    # title = models.CharField(max_length=255)
    # namespace = models.CharField(
    #     max_length=50,
    #     blank=True,
    #     null=True,
    #     help_text="Пространство имён для slug (опционально)"
    # )
    # slug = models.SlugField(max_length=255, blank=True)
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        verbose_name='SEO заголовок'
    )
    seo_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name='SEO описание'
    )
    content = RichTextUploadingField()  # -//- с загрузкой картинок/файлов, свойства по умолчанию
    # content = RichTextField()   # форматируемый текст
    # content = RichTextUploadingField(config_name='moloshop')   # -//- с загрузкой картинок/файлов в MEDIA_ROOT/CKEDITOR_UPLOAD_PATH

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Политику, правила, инструкции"
        verbose_name_plural = "Политики, правила, инструкции"


    def __str__(self):
        return self.title