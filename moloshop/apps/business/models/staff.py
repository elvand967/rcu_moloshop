
# apps/business/models/staff.py

'''
 Staff (мастер / специалист)
'''
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.business.models import Business
from apps.core.models import UUIDModel


class Staff(UUIDModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='staff_members')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    position = models.CharField(max_length=255, blank=True, verbose_name='Должность / специализация')
    bio = models.TextField(blank=True, verbose_name='Описание / биография')
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True, verbose_name='Фото')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Средний рейтинг мастера от 0 до 5"
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Мастер / специалист'
        verbose_name_plural = 'Мастера / специалисты'
        unique_together = ('business', 'email')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
