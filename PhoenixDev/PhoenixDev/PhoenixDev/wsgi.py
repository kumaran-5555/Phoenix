"""
WSGI config for phoenix project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys
#sys.path.append('/home/kumaran/docroot/phoenix/phoenix')

root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PhoenixDev.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
