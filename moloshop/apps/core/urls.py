
# moloshop/apps/core/urls.py

from django.urls import path
from .views import *

app_name = "core" # пространство имён

urlpatterns = [
    # path('', includes, name='includes'),
    path('favorites/', favorites, name='favorites'),
    path('about/', about, name='about'),
    path('feedback/', feedback, name='feedback'),
    path('portfolio/', portfolio, name='portfolio'),
    path('fag/', fag, name='fag'),
    path('board/', board, name='board'),
    path('showcase/', showcase, name='showcase'),

    path('docs/<slug:slug>/', docs_detail, name='docs_detail'),

    #
    # path('named-urls-json/', named_urls_api, name='named_urls_json'),
]
