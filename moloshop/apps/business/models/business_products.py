
# apps/business/models/business_products.py

import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.core.models.abstract import SlugNamespaceModel, UUIDModel
from apps.business.models.business import Business
from apps.business.models.staff import Staff


# ==========================
#  Валюты
# ==========================
class CurrencyChoice(models.TextChoices):
    """Справочник валют"""
    BYN = "BYN", "Белорусский рубль"
    RUB = "RUB", "Российский рубль"
    USD = "USD", "Доллар США"
    EUR = "EUR", "Евро"
    PLN = "PLN", "Польский злотый"


# ==========================
#  Единицы измерения
# ==========================
class GoodsUnit(models.TextChoices):
    PIECE = "pcs", "Штука"
    KILOGRAM = "kg", "Килограмм"
    GRAM = "g", "Грамм"
    LITER = "l", "Литр"
    METER = "m", "Метр"
    SQUARE_METER = "m2", "Квадратный метр"
    CUBIC_METER = "m3", "Кубический метр"
    PACKAGE = "pkg", "Упаковка"


class ServiceUnit(models.TextChoices):
    ACAD_HOUR = "acad_hour", "Академический час"
    SESSION = "session", "Сеанс"
    HAIRCUT = "haircut", "Стрижка"
    CONSULTATION = "consultation", "Консультация"
    VISIT = "visit", "Визит"
    PACKAGE = "package", "Пакет"
    SERVICE = "service", "Услуга"
    HOUR = "hour", "Час"
    DAY = "day", "День"
    TASK = "task", "Задача"


# ==========================
#  Категории
# ==========================
class Category(SlugNamespaceModel, MPTTModel):
    """Категории товаров и услуг для конкретного бизнеса"""
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Бизнес",
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория",
    )
    description = models.TextField("Описание", blank=True)

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["namespace", "slug"],
                name="uniq_category_namespace_slug",
            )
        ]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.namespace and self.business_id:
            self.namespace = self.business.slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.business})"


# ==========================
#  Медиа (галерея)
# ==========================
class Media(UUIDModel):
    """Универсальная модель для хранения медиа (фото/файлы)"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    file = models.FileField("Файл", upload_to="uploads/%Y/%m/%d/")
    alt_text = models.CharField("Описание", max_length=255, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_main = models.BooleanField("Основное изображение", default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        ordering = ["order"]
        verbose_name = "Медиа"
        verbose_name_plural = "Медиа"

    def __str__(self):
        return f"Media {self.id} ({self.content_type} - {self.object_id})"


# ==========================
#  Абстрактная базовая модель для Товаров и Услуг.
# ==========================
class BaseProduct(SlugNamespaceModel):
    """Общие поля для товаров и услуг"""
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        verbose_name="Бизнес",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)ss",
        verbose_name="Категория",
    )
    # 🔹 связь с галереей (Media)
    media = GenericRelation(
        "business.Media",
        related_query_name="%(class)s_media"  # products_media / services_media
    )

    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена за единицу")
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoice.choices,
        default=CurrencyChoice.BYN,
        blank=True,
        verbose_name="Валюта",
    )
    rating = models.FloatField(default=0, help_text="Средний рейтинг")
    total_likes = models.PositiveIntegerField(default=0, help_text="Всего лайков")
    total_dislikes = models.PositiveIntegerField(default=0, help_text="Всего дизлайков")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    sku = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="Артикул",
    )

    class Meta:
        abstract = True
        ordering = ["title"]

    def clean(self):
        """Контроль уникальности SKU в рамках бизнеса"""
        super().clean()
        if not self.sku:  # пустой SKU разрешаем
            return

        # Проверка пересечений по бизнесу и SKU (обе модели)
        product_ct = ContentType.objects.get_for_model(Product)
        service_ct = ContentType.objects.get_for_model(Service)

        conflict = (
            Product.objects.filter(business=self.business, sku=self.sku)
            .exclude(pk=self.pk)
            .exists()
            or Service.objects.filter(business=self.business, sku=self.sku)
            .exclude(pk=self.pk)
            .exists()
        )
        if conflict:
            raise ValidationError({"sku": f"Артикул {self.sku} уже используется в рамках бизнеса."})

    def save(self, *args, **kwargs):
        if not self.namespace and self.business_id:
            self.namespace = self.business.slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ==========================
#  Товары  Goods
# ==========================
class Product(BaseProduct):
    """Товар конкретного бизнеса"""
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток")
    delivery_info = models.CharField(
        default="Самовывоз",
        max_length=255,
        blank=True,
        null=True,
        help_text="Информация по доставке",
    )
    unit = models.CharField(
        max_length=10,
        choices=GoodsUnit.choices,
        default=GoodsUnit.PIECE,
        verbose_name="Единица"
    )
    image = models.ImageField("Обложка", upload_to="products/covers/", blank=True, null=True)
    gallery = GenericRelation(Media, related_query_name="product")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["namespace", "slug"], name="uniq_product_namespace_slug")
        ]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.title} ({self.business})"


# ==========================
#  Услуги
# ==========================
class Service(BaseProduct):
    """Услуга конкретного бизнеса"""
    duration = models.DurationField("Длительность", null=True, blank=True)
    place_of_service = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Место оказания услуги",
        help_text="Например, на дому, в салоне и т.п.",
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Мастер / специалист",
    )
    unit = models.CharField(
        max_length=20,
        choices=ServiceUnit.choices,
        default=ServiceUnit.SERVICE,
        verbose_name="Единица"
    )
    image = models.ImageField("Обложка", upload_to="services/covers/", blank=True, null=True)
    gallery = GenericRelation(Media, related_query_name="service")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["namespace", "slug"], name="uniq_service_namespace_slug")
        ]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.title} ({self.business})"


# ==========================
#  Signals: очистка медиа при удалении
# ==========================
@receiver(post_delete, sender=Media)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Удаляем файл с диска при удалении Media"""
    if instance.file:
        instance.file.delete(save=False)
