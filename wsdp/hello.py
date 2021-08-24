import os
import sys
from django.conf import settings
from django.core.wsgi import get_wsgi_application

DEBUG = os.environ.get('DEBUG','on') == "on"
SECRET_KEY = os.environ.get('SECRET_KEY',os.urandom(32))
ALLOWED_HOSTS= os.environ.get('ALLOWED_HOSTS','localhost').split(",")
settings.configure(
    DEBUG=DEBUG ,
    SECRET_KEY =SECRET_KEY, 
    ALLOWED_HOST=ALLOWED_HOSTS,
    ROOT_URLCONF= __name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'djando.middleware.csrf.CsrfViewMiddleware',
        'djando.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

from django.conf.urls import url
from django.http import HttpResponse
application = get_wsgi_application()

def index(request):
    return HttpResponse('this is the smalles Django Application')

urlpatterns =(
    url(r'^$',index),
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
