import os

# apps/business/models/products.py

from django.db import models
from django.core.exceptions import ValidationError
from apps.business.utils.image_utils import process_product_image
from django.urls import reverse
from apps.core.models.abstract import SlugNamespaceModel, NamedSlugModel
from .staff import Staff
from .business import Business
from mptt.models import MPTTModel, TreeForeignKey

from apps.core.utils.image_processor import process_image, ImageSpec


CURRENCY_CHOICES = [
    ('BYN', 'Белорусский рубль'),
    ('USD', 'Доллар США'),
    ('EUR', 'Евро'),
    ('RUB', 'Российский рубль'),
]


class Category(NamedSlugModel, MPTTModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='categories')
    slug = models.SlugField(max_length=255, verbose_name='Slug категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', blank=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = ('business', 'slug')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class SKUModel(SlugNamespaceModel):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name=None  # будем задавать в наследниках
    )
    sku = models.CharField(
        max_length=64,
        blank=True,
        null=False,
        default="",
    )

    class Meta:
        abstract = True

    def clean(self):
        """
        Контроль уникальности SKU в рамках бизнеса:
        - Игнорируем пустые значения
        - Проверяем как текущую модель, так и "соседнюю" (Goods / Service)
        - На SQLite выполняется полная проверка
        - В PostgreSQL будет работать частичный индекс + эта проверка как fallback
        """
        super().clean()

        if not self.sku:  # пустой SKU разрешаем
            return

        from apps.business.models import Goods, Service

        # Проверка в текущей модели
        qs = self.__class__.objects.filter(
            business=self.business,
            sku=self.sku
        ).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({"sku": f"Артикул {self.sku} уже занят."})

        # Проверка в соседней модели
        other_model = Goods if isinstance(self, Service) else Service
        qs_other = other_model.objects.filter(
            business=self.business,
            sku=self.sku
        )
        if qs_other.exists():
            raise ValidationError({"sku": f"Артикул {self.sku} уже используется в другом объекте бизнеса."})


'''Товары'''
class Goods(SKUModel):
    """
    class SlugNamespaceModel(UUIDModel): # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        title = models.CharField(max_length=255)
        namespace = models.CharField(max_length=50, blank=True, null=True, help_text="Пространство имён для slug"
        slug = models.SlugField(max_length=255, blank=True)
    )"""
    UNIT_CHOICES = [
        ('pcs', 'Штука'),
        ('kg', 'Килограмм'),
        ('ltr', 'Литр'),
        ('m', 'Метр'),
        ('pack', 'Упаковка'),
    ]
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="goods",  # правильное имя
    )
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='goods')
    description = models.TextField(blank=True, verbose_name="Описание товара")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='pcs', verbose_name="Единица товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу товара")
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, blank=True, null=True, verbose_name="Валюта")
    is_active = models.BooleanField(default=True, help_text="Активен ли товар для продажи")
    image = models.ImageField(upload_to="business/", blank=True, null=True)
    image_webp = models.ImageField(upload_to="business/", blank=True, null=True)  # новое поле для WebP
    rating = models.FloatField(default=0, help_text="Средний рейтинг товара")
    delivery_info = models.CharField(default="Самовывоз", max_length=255, blank=True, null=True,  help_text="Информация по доставке")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta(SKUModel.Meta):
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["business", "title"]
        constraints = [
            models.UniqueConstraint(
                fields=["business", "sku"],
                condition=~models.Q(sku=""),  # игнорируем пустые
                name="unique_goods_sku_per_business_not_empty",
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.sku or 'без SKU'})"

    def save(self, *args, **kwargs):
        if not self.namespace and self.business_id:
            self.namespace = str(self.business_id)

        if self.image and self.business:
            year = self.business.created_at.strftime("%Y")
            month = self.business.created_at.strftime("%m")
            base_dir = f"{year}/{month}"

            processed = process_image(
                self.image.file,
                ImageSpec(
                    width=430,
                    height=242,
                    crop=True,
                    formats=["JPEG", "WEBP"],
                    base_dir=base_dir,
                    slug_seed=f"{self.business.slug}-{self.slug}",
                )
            )
            if processed:
                if "jpeg" in processed:
                    jpeg_file = processed["jpeg"]
                    jpeg_file.name = os.path.join(base_dir, "jpeg", os.path.basename(jpeg_file.name))
                    self.image.save(jpeg_file.name, jpeg_file, save=False)
                if "webp" in processed:
                    webp_file = processed["webp"]
                    webp_file.name = os.path.join(base_dir, "webp", os.path.basename(webp_file.name))
                    self.image_webp.save(webp_file.name, webp_file, save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "business:goods_detail",
            kwargs={"business_slug": self.business.slug, "goods_slug": self.slug}
        )


'''Услуги'''
class Service(SKUModel):
    UNIT_CHOICES = [
        ('acad_hour', 'Академический час'),  # Репетиторство, обучение
        ('session', 'Сеанс'),  # Массаж, физиотерапия
        ('haircut', 'Стрижка'),  # Салон красоты
        ('consultation', 'Консультация'),  # Юридические, психологические услуги
        ('visit', 'Визит'),  # Медицинские услуги, домработница
        ('package', 'Пакет'),  # Пакет услуг
        ('service', 'Услуга'),  # Общая услуга без количественного измерения
        ('hour', 'Час'),  # Работа специалиста, аренда
        ('day', 'День'),  # Долгосрочные услуги, курсы
        ('task', 'Задача'),  # Разовые проекты, задачи
    ]
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="services",
    )
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    description = models.TextField(blank=True, verbose_name='Описание услуги')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='service', verbose_name='Единица измерения')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, blank=True, null=True, help_text="Валюта")
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Мастер / специалист')
    place_of_service = models.CharField(max_length=255, blank=True, verbose_name='Место оказания услуги', help_text='Например, на дому, в салоне и т.п.')
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, verbose_name='Длительность услуги (минуты)')
    image = models.ImageField(upload_to="business/", blank=True, null=True)
    image_webp = models.ImageField(upload_to="business/", blank=True, null=True)  # новое поле для WebP
    is_active = models.BooleanField(default=True, verbose_name='Активна ли услуга')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')

    def save(self, *args, **kwargs):
        if not self.namespace and self.business_id:
            self.namespace = str(self.business_id)

        if self.image and self.business:
            year = self.business.created_at.strftime("%Y")
            month = self.business.created_at.strftime("%m")
            base_dir = f"{year}/{month}"

            processed = process_image(
                self.image.file,
                ImageSpec(
                    width=430,
                    height=242,
                    crop=True,
                    formats=["JPEG", "WEBP"],
                    base_dir=base_dir,
                    slug_seed=f"{self.business.slug}-{self.slug}",
                )
            )
            if processed:
                if "jpeg" in processed:
                    jpeg_file = processed["jpeg"]
                    jpeg_file.name = os.path.join(base_dir, "jpeg", os.path.basename(jpeg_file.name))
                    self.image.save(jpeg_file.name, jpeg_file, save=False)
                if "webp" in processed:
                    webp_file = processed["webp"]
                    webp_file.name = os.path.join(base_dir, "webp", os.path.basename(webp_file.name))
                    self.image_webp.save(webp_file.name, webp_file, save=False)

        super().save(*args, **kwargs)

    class Meta(SKUModel.Meta):
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["business", "title"]
        constraints = [
            models.UniqueConstraint(
                fields=["business", "sku"],
                condition=~models.Q(sku=""),  # игнорируем пустые
                name="unique_service_sku_per_business_not_empty",
            )
        ]

    def __str__(self):
        return self.title