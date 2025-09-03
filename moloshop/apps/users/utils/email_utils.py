
# apps/users/utils/email_utils.py

import random
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

def generate_email_code():
    part1 = random.randint(10, 99)
    part2 = random.randint(100, 999)
    return f"{part1}-{part2}"

def send_email_confirmation_code(user):
    code = generate_email_code()
    profile = user.profile
    profile.email_code = code
    profile.email_code_created = timezone.now()
    profile.save()

    subject = "Код подтверждения регистрации на Moloshop.by"

    # Рендерим html формат письма
    html_content = render_to_string(
        "core/emails/confirmation_email.html",
        {"code": code, "user_email": user.email}
    )

    # Создаем email с альтернативой
    msg = EmailMultiAlternatives(
        subject=subject,
        body=f"Ваш код подтверждения: {code}",  # Текстовая версия
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
















# import random
# from django.core.mail import send_mail
# from django.conf import settings
# from django.utils import timezone
#
# def generate_email_code():
#     # Генерируем двухчастный код: 2 цифры - 3 цифры, разделённый дефисом
#     part1 = random.randint(10, 99)    # две цифры от 10 до 99
#     part2 = random.randint(100, 999)  # три цифры от 100 до 999
#     return f"{part1}-{part2}"
#
# def send_email_confirmation_code(user):
#     code = generate_email_code()
#     profile = user.profile
#     profile.email_code = code
#     profile.email_code_created = timezone.now()
#     profile.save()
#     # print(f"Отправка кода {code} на email {user.email}")
#
#     subject = "Код подтверждения регистрации на Moloshop.by"
#     message = (
#         f"Уважаемый пользователь {user.email},\n\n"
#         f"Ваш код подтверждения регистрации: {code}\n\n"
#         "Введите этот код на странице подтверждения для завершения регистрации.\n\n"
#         f"Если вы не регистрировались, просто проигнорируйте это письмо."
#         f"Это письмо создано автоматически, на него не нужно отвечать."
#         f"С уважением, команда Moloshop.by"
#     )
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [user.email],
#         fail_silently=False,
#     )
