"""
WSGI config for DomDino project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application
sys.path.append('/home/emabord/Developer/ArduinoDomotica/DomDino')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DomDino.settings")

application = get_wsgi_application()

"""
import os,sys
sys.path.append('/home/emabord/Developer/ArduinoDomotica/DomDino/DomDino')
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomDino.settings'
import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()
def application(environ, start_response):
	environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
	if environ['wsgi.url_scheme'] == 'https':
		environ['HTTPS'] = 'on'

"""
