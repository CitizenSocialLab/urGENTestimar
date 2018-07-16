import os
import sys
import site

site.addsitedir('/home/jduch/.virtualenvs/firatarrega/lib/python2.7/site-packages/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

paths = [
  '/var/www/urgent_estimar/',
  '/var/www/urgent_estimar/game',
]

for path in paths:
  if path not in sys.path:
    sys.path.append(path)
   
print >> sys.stderr, sys.path
