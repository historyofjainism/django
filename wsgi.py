"""
WSGI config for live project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
os.environ.setdefault('APP_ENVIRONMENT', 'production')
os.environ.setdefault('CLOUDINARY_URL','cloudinary://111376825554284:CWgsyTXwZj_yGZWHwUbSRB82lTU@history-of-jainism')

application = get_wsgi_application()
