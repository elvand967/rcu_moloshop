# moloshop/apps/main/log.py
from django.shortcuts import render
from django.urls import reverse

def home_view(request):
    context = {
        'offices': [
            {
                'name': 'Офис Центральный',
                'short_description': 'Главный офис компании с полным набором услуг.',
                'image': type('Img', (), {'url': '/media/temp/1_thumbnail.jpg'})(),
                'url': '/offices/central/'
            },
            {
                'name': 'Офис Восточный',
                'short_description': 'Региональный офис для клиентов восточного региона.',
                'image': type('Img', (), {'url': '/media/temp/22_thumbnail.jpg'})(),
                'url': '/offices/east/'
            },
            {
                'name': 'Офис Заподный',
                'short_description': 'Главный офис компании с полным набором услуг.',
                'image': type('Img', (), {'url': '/media/temp/1_thumbnail.jpg'})(),
                'url': '/offices/central/'
            },
            {
                'name': 'Офис Южный',
                'short_description': 'Региональный офис для клиентов восточного региона.',
                'image': type('Img', (), {'url': '/media/temp/22_thumbnail.jpg'})(),
                'url': '/offices/east/'
            },
        ],
        'products': [
            {
                'name': 'Услуга: Веб-дизайн',
                'price': '250',
                'image': type('Img', (), {'url': '/media/temp/1.png'})(),
                'get_absolute_url': '/marketplace/web-design/'
            },
            {
                'name': 'Товар: Смартфон',
                'price': '1200',
                'image': type('Img', (), {'url': '/media/temp/3.png'})(),
                'get_absolute_url': '/marketplace/smartphone/'
            }
        ],
        'ads': [
            {
                'title': 'Скидка на ремонт компьютеров',
                'short_description': 'Только до конца месяца скидка 20% на все виды ремонта.',
                'image': type('Img', (), {'url': '/media/temp/4.png'})(),
                'get_absolute_url': '/board/ad1/'
            },
            {
                'title': 'Ищу партнёра для стартапа',
                'short_description': 'Ищу инвестора для IT-проекта с потенциалом.',
                'image': type('Img', (), {'url': '/media/temp/5.png'})(),
                'get_absolute_url': '/board/ad2/'
            }
        ],
        'blog_posts': [
            {
                'title': '5 советов для успешного бизнеса',
                'short_description': 'Краткое руководство по увеличению продаж и клиентской базы.',
                'get_absolute_url': '/blog/tips-for-business/'
            },
            {
                'title': 'Как выбрать офисное помещение',
                'short_description': 'Основные критерии при выборе места для вашего офиса.',
                'get_absolute_url': '/blog/office-selection/'
            }
        ],
        'portfolio_items': [
            {
                'title': 'Дизайн лендинга для студии',
                'image': type('Img', (), {'url': '/media/temp/6.png'})()
            },
            {
                'title': 'Мобильное приложение для магазина',
                'image': type('Img', (), {'url': '/media/temp/7.png'})()
            }
        ]
    }

    return render(request, 'main/home.html', context)
















# from django.shortcuts import render
#
# def home_view(request):
#     context = {
#         'offices': [],          # список офисов
#         'products': [],         # товары
#         'ads': [],              # объявления
#         'blog_posts': [],       # статьи
#         'portfolio_items': [],  # портфолио
#     }
#     return render(request, 'main/home.html', context)
