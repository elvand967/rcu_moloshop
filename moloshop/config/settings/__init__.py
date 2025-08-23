# ../config/settings/__init__.py

import os

env = os.getenv('DJANGO_ENV', 'dev').lower()

if env == 'prod' or env == 'production':
    from .prod import *
# elif env == 'test':
#     from .test import *  # если у тебя будет файл test.py
else:
    from .dev import *