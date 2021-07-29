import random
import string
import os

from api.settings.production import *  # noqa
from api.settings.production import DATABASES

# A boolean that turns on/off debug mode.
# https://docs.djangoproject.com/en/2.2/ref/settings/#debug
DEBUG = True

# If set to True, Django's normal exception handling of view functions
# will be suppressed, and exceptions will propagate upwards
# https://docs.djangoproject.com/en/2.2/ref/settings/#debug-propagate-exceptions
DEBUG_PROPAGATE_EXCEPTIONS = True

# router information
ROUTER_HOST = 'drycc-router.example.com'
ROUTER_PORT = 80

# randomize test database name so we can run multiple unit tests simultaneously
DATABASES['default']['NAME'] = "unittest-{}".format(''.join(
    random.choice(string.ascii_letters + string.digits) for _ in range(8)))
DATABASES['default']['USER'] = 'postgres'

# use DB name to isolate the data for each test run
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': DATABASES['default']['NAME'],
        'KEY_PREFIX': DATABASES['default']['NAME'],
    }
}


DRYCC_DEFAULT_CONFIG_TAGS = os.environ.get('DRYCC_DEFAULT_CONFIG_TAGS', '')

DRYCC_APP_STORAGE_CLASS = os.environ.get('DRYCC_APP_STORAGE_CLASS', '')


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()
