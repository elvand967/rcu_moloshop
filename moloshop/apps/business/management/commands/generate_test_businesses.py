
# apps/business/management/commands/generate_test_businesses.py

import random
import io
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from PIL import Image
from apps.business.models import (
    Business, ContactInfo, Messenger, Staff,
    Category, Product, Service, Media, GoodsUnit, ServiceUnit, CurrencyChoice
)
from django.contrib.auth import get_user_model

User = get_user_model()

'''
команда
(.venv) D:\PythonProject\rcu_moloshop\moloshop>python manage.py generate_test_businesses
'''


class Command(BaseCommand):
    help = 'Генерация тестовых бизнесов с товарами, услугами, категориями, контактами, сотрудниками и тестовыми изображениями'

    def generate_unique_sku(self, business, base_sku):
        """Генерирует уникальный SKU в рамках бизнеса для Product и Service"""
        sku = base_sku
        counter = 1
        while Product.objects.filter(business=business, sku=sku).exists() \
                or Service.objects.filter(business=business, sku=sku).exists():
            sku = f"{base_sku}-{counter}"
            counter += 1
        return sku

    def create_test_image(self, width=200, height=200, color=None):
        """Создаёт тестовое изображение и возвращает ContentFile"""
        color = color or (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        image = Image.new('RGB', (width, height), color=color)
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        return ContentFile(buffer.read(), name=f'test_{random.randint(1000,9999)}.jpg')

    def add_gallery_images(self, instance, count=3):
        """Добавляет несколько тестовых изображений в галерею"""
        for i in range(count):
            img_file = self.create_test_image()
            Media.objects.create(
                content_object=instance,
                file=img_file,
                alt_text=f"Тестовое изображение {i+1}",
                order=i,
                is_main=(i == 0)
            )

    def handle(self, *args, **options):
        now = timezone.now()

        # ======= Шаблоны бизнесов =======
        business_templates = [
            {"title": "Кондитерская «Сладкая жизнь»", "owner_email": "owner1@example.com", "type": "ООО"},
            {"title": "ИП «Мастер на час»", "owner_email": "owner2@example.com", "type": "ИП"},
            {"title": "Самозанятый «Фитнес-тренер Алексей»", "owner_email": "owner3@example.com", "type": "Самозанятый"},
            {"title": "ИП «Ремонт квартир»", "owner_email": "owner4@example.com", "type": "ИП"},
            {"title": "ООО «Цветочный мир»", "owner_email": "owner5@example.com", "type": "ООО"},
        ]

        product_names = ["Торт шоколадный", "Пирожное эклер", "Капкейк ягодный", "Флористическая композиция",
                         "Набор инструментов"]
        service_names = ["Доставка на дом", "Массаж спины", "Консультация юриста", "Уборка квартиры",
                         "Персональный тренинг"]
        categories_data = ["Основные товары", "Премиум товары", "Сезонные предложения", "Популярные услуги",
                           "Экспресс-сервисы"]
        messenger_types = ['phone', 'email', 'whatsapp', 'telegram', 'viber', 'instagram']
        first_names = ["Алексей", "Мария", "Иван", "Ольга", "Сергей", "Екатерина", "Дмитрий"]
        last_names = ["Иванов", "Петрова", "Сидоров", "Кузнецова", "Смирнов", "Федорова"]

        # ======= Создание бизнесов =======
        for b_idx, b_data in enumerate(business_templates, start=1):
            owner_email = b_data["owner_email"]
            owner, _ = User.objects.get_or_create(
                email=owner_email,
                defaults={"is_active": True, "first_name": "Тест", "last_name": f"Пользователь {b_idx}"}
            )

            business = Business.objects.create(
                title=b_data["title"],
                owner=owner,
                description=f"{b_data['type']} в тестовой базе данных",
                is_visible=True,
                created_at=now,
                updated_at=now
            )
            self.stdout.write(self.style.SUCCESS(f"Создан бизнес: {business.title}"))

            # ======= ContactInfo + Messengers =======
            contact = ContactInfo.objects.create(
                business=business,
                location="Минск",
                address=f"ул. Тестовая, {b_idx}",
                order=1,
            )
            for mt in random.sample(messenger_types, 2):
                Messenger.objects.create(
                    contact_info=contact,
                    messenger_type=mt,
                    identifier=f"{mt}_{b_idx}@example.com" if mt == 'email' else f"+37529123{b_idx}{b_idx}"
                )

            # ======= Staff =======
            staff_list = []
            for _ in range(2 + random.randint(0, 1)):
                staff_member = Staff.objects.create(
                    business=business,
                    first_name=random.choice(first_names),
                    last_name=random.choice(last_names),
                    position=random.choice(["Мастер", "Менеджер", "Консультант"]),
                    bio="Опытный специалист",
                    phone=f"+37529{random.randint(1000000, 9999999)}",
                    email=f"staff{b_idx}_{random.randint(1, 99)}@example.com",
                    rating=round(random.uniform(3.0, 5.0), 1),
                    is_active=True
                )
                staff_list.append(staff_member)

            # ======= Категории =======
            categories = []
            for c_name in random.sample(categories_data, 3):
                cat = Category.objects.create(
                    business=business,
                    title=c_name
                )
                categories.append(cat)

            # ======= Товары =======
            for _ in range(3):
                base_sku = f"SKU-P-{b_idx}-{random.randint(1000, 9999)}"
                sku = self.generate_unique_sku(business, base_sku)
                product = Product.objects.create(
                    business=business,
                    category=random.choice(categories),
                    title=random.choice(product_names),
                    description="Тестовое описание товара",
                    unit=random.choice([u.value for u in GoodsUnit]),
                    price=round(random.uniform(10, 200), 2),
                    currency=random.choice([c.value for c in CurrencyChoice]),
                    sku=sku,
                    is_active=True,
                    created_at=now,
                    updated_at=now,
                    stock=random.randint(5, 50),
                    delivery_info="Самовывоз",
                    image=self.create_test_image()
                )
                self.add_gallery_images(product, count=3)

            # ======= Услуги =======
            for _ in range(3):
                base_sku = f"SKU-S-{b_idx}-{random.randint(1000, 9999)}"
                sku = self.generate_unique_sku(business, base_sku)
                service = Service.objects.create(
                    business=business,
                    category=random.choice(categories),
                    title=random.choice(service_names),
                    description="Тестовое описание услуги",
                    unit=random.choice([u.value for u in ServiceUnit]),
                    price=round(random.uniform(20, 500), 2),
                    currency=random.choice([c.value for c in CurrencyChoice]),
                    sku=sku,
                    is_active=True,
                    created_at=now,
                    updated_at=now,
                    duration=timezone.timedelta(minutes=random.randint(30, 120)),
                    place_of_service=random.choice(["На дому", "В салоне", "Онлайн"]),
                    staff=random.choice(staff_list) if staff_list else None,
                    image=self.create_test_image()
                )
                self.add_gallery_images(service, count=3)

        self.stdout.write(self.style.SUCCESS("Генерация тестовых бизнесов с изображениями завершена!"))
