import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.business.models import Business, ContactInfo, Messenger, Staff, Category, Goods, Service
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Генерация тестовых бизнесов с товарами, услугами, категориями, контактами и сотрудниками'

    def handle(self, *args, **options):
        now = timezone.now()

        # ======= Осмысленные данные =======
        business_templates = [
            {
                "title": "Кондитерская «Сладкая жизнь»",
                "owner_email": "owner1@example.com",
                "type": "ООО",
            },
            {
                "title": "ИП «Мастер на час»",
                "owner_email": "owner2@example.com",
                "type": "ИП",
            },
            {
                "title": "Самозанятый «Фитнес-тренер Алексей»",
                "owner_email": "owner3@example.com",
                "type": "Самозанятый",
            },
            {
                "title": "ИП «Ремонт квартир»",
                "owner_email": "owner4@example.com",
                "type": "ИП",
            },
            {
                "title": "ООО «Цветочный мир»",
                "owner_email": "owner5@example.com",
                "type": "ООО",
            },
        ]

        # Товары и услуги
        product_names = ["Торт шоколадный", "Пирожное эклер", "Капкейк ягодный", "Флористическая композиция",
                         "Набор инструментов"]
        service_names = ["Доставка на дом", "Массаж спины", "Консультация юриста", "Уборка квартиры",
                         "Персональный тренинг"]
        categories_data = ["Основные товары", "Премиум товары", "Сезонные предложения", "Популярные услуги",
                           "Экспресс-сервисы"]
        units_goods = ['pcs', 'kg', 'ltr', 'm', 'pack']
        units_services = ['acad_hour', 'session', 'haircut', 'consultation', 'visit', 'package', 'service', 'hour',
                          'day', 'task']
        currencies = ['BYN', 'USD', 'EUR', 'RUB']

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
                order=b_idx,
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
            # Генерация 2 мессенджеров
            for mt in random.sample(messenger_types, 2):
                Messenger.objects.create(
                    contact_info=contact,
                    messenger_type=mt,
                    identifier=f"{mt}_{b_idx}@example.com" if mt == 'email' else f"+37529123{b_idx}{b_idx}"
                )

            # ======= Staff =======
            for _ in range(2 + random.randint(0, 1)):
                Staff.objects.create(
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
                Goods.objects.create(
                    business=business,
                    category=random.choice(categories),
                    title=random.choice(product_names),
                    description="Тестовое описание товара",
                    unit=random.choice(units_goods),
                    price=round(random.uniform(10, 200), 2),
                    currency=random.choice(currencies),
                    sku=f"SKU-{b_idx}-{random.randint(1000, 9999)}",
                    is_active=True,
                    created_at=now,
                    updated_at=now
                )

            # ======= Услуги =======
            for _ in range(3):
                Service.objects.create(
                    business=business,
                    category=random.choice(categories),
                    title=random.choice(service_names),
                    description="Тестовое описание услуги",
                    unit=random.choice(units_services),
                    price=round(random.uniform(20, 500), 2),
                    currency=random.choice(currencies),
                    is_active=True,
                    created_at=now,
                    updated_at=now
                )

        self.stdout.write(self.style.SUCCESS("Генерация тестовых бизнесов завершена!"))
