
# apps/business/models/order.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.business.models.business import Business
from apps.business.models.products import Goods, Service
from apps.business.models.staff import Staff
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.business.utils.master_time import is_staff_available_for_service
from apps.core.models import UUIDModel


User = get_user_model()

class Order(UUIDModel):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Ожидает обработки')
        PROCESSING = 'processing', _('В обработке')
        COMPLETED = 'completed', _('Завершён')
        CANCELLED = 'cancelled', _('Отменён')

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='orders', verbose_name=_("Бизнес"))
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name=_("Покупатель"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_("Статус заказа"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Общая сумма"))

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.customer} в {self.business}"
class OrderItem(UUIDModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_("Заказ"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  # Товар или услуга
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Количество"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена за единицу"))

    # Дополнительные поля для услуг:
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Мастер / специалист"))
    appointment_datetime = models.DateTimeField(null=True, blank=True, verbose_name=_("Время записи"))

    def clean(self):
        super().clean()
        if self.staff and self.appointment_datetime and self.service and self.service.duration_minutes:
            is_staff_available_for_service(
                staff=self.staff,
                appointment_datetime=self.appointment_datetime,
                service_duration_minutes=self.service.duration_minutes
            )

    class Meta:
        verbose_name = _("Позиция заказа")
        verbose_name_plural = _("Позиции заказа")

    def __str__(self):
        return f"{self.content_object} x {self.quantity} ({self.staff or 'без мастера'})"

    def get_total_price(self):
        return self.price * self.quantity

