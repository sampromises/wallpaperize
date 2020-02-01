"""
WSGI config for sskywalker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import logging
import os

from django.core.wsgi import get_wsgi_application

log = logging.getLogger("app")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sskywalker.settings')

log.info("wsgi.py called...")
application = get_wsgi_application()
log.info(f"wsgi.py succeeded, application = {application}")
