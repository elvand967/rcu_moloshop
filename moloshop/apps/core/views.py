
# ../apps/core/log.py

from django.shortcuts import render


def about(request):
    data = {
        'title': 'О нас',
        'info': 'Мы — команда профессионалов, увлеченных своим делом и стремящихся создавать качественные и инновационные решения. '
                'Наша миссия — помогать клиентам достигать поставленных целей, '
                'предлагая надежные и эффективные продукты и услуги.',
        'repeat_range': range(20),  # список для 20 повторений
    }
    return render(request, 'core/temp/about.html', context=data)

def board(request):
    data = {
        'title': 'Доска объявлений',
        'info': 'Страница доски объявлений',
    }
    return render(request, 'core/temp/board.html', context=data)

def fag(request):
    data = {
        'title': 'FAG',
        'info': 'Часто задаваемые вопросы',
    }
    return render(request, 'core/temp/fag.html', context=data)

def feedback(request):
    data = {
        'title': 'Обратная связь',  # тестируем отработку 'title' по умолчанию в шаблоне
        'info': 'Здесь должна быть форма обратной связи',
    }
    return render(request, 'core/temp/feedback.html', context=data)

def home(request):
    data = {
        'title': 'Домашняя страница',
        'info': 'Первые шаги настройки',
    }
    return render(request, 'core/temp/home.html', context=data)

def portfolio(request):
    data = {
        'title': 'Портфолио',
        'info': 'Портфолио: новые презентации и разработки',
    }
    return render(request, 'core/temp/portfolio.html', context=data)

def showcase(request):
    data = {
        'title': 'Витрина',
        'info': 'Витрина товаров и услуг исполнителей',
    }
    return render(request, 'core/temp/showcase.html', context=data)

def favorites(request):
    data = {
        'title': 'Избранное',
        'info': 'Избранные товары и услуги исполнителей',
    }
    return render(request, 'core/temp/favorites.html', context=data)



# apps/core/log.py
from django.shortcuts import render, get_object_or_404
from .models.core_documents import ContractsInstructions


def docs_detail(request, slug):
    """
    Показывает один документ ContractsInstructions по slug.
    """
    document = get_object_or_404(ContractsInstructions, slug=slug)

    context = {
        'document': document
    }
    return render(request, 'core/docs.html', context)




