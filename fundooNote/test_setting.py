from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'data.note',
        'USER': 'postgres',
        'PASSWORD': 'Pass@123',
        'HOST': 'localhost',
    }
}
AUTH_USER_MODEL = "user.User"
USE_TZ = False