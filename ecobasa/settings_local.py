# -*- coding: utf-8 -*-

#from __future__ import unicode_literals
# we cannot use unicode_literals here, or smtplib will crash, expecting a str when reading the secret key

from .default_settings import *

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ecobasa',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

ADMINS = (
)
MANAGERS = ADMINS

DEBUG = True  # <<<<< SET TO `False` ON staging AND production
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
THUMBNAIL_DEBUG = DEBUG

DEBUG_TOOLBAR_ENABLED = False

if DEBUG:
    del LOGGING

### !!! WARNING !!! CHANGE THIS IN THE PRODUCTION ENVIRONMENT
SECRET_KEY = '#g*)$4gwah--aq(i53z825ug0@ft^3&h34nkg@&yisc8f3t%u+qc_9k2%o*_nfd*'

# from ecobasa.wachstumswende.de
COSINNUS_ETHERPAD_BASE_URL = 'https://pad.sinnwerkstatt.com/api'
COSINNUS_ETHERPAD_API_KEY = ''  # copy from staging if needed

# recaptcha
RECAPTCHA_PUBLIC_KEY = '6LfPBgUTAAAAALmElA3Co18PYSfvvGG5Rl94Qiyg'  # needs to be set in local settings.py
RECAPTCHA_PRIVATE_KEY = ''  # copy from staging if needed

# enable this haystack setting if you have actually set up elastic search on your system
"""
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'cosinnus.backends.RobustElasticSearchEngine',  # replaces 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'ecobasa',
    },
}
"""
# note: this will use the most basic, in-memory haystack backend that gives no useful search results
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# save mail as local text files
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '__mail__' # change this to a proper location or mkdir


""" ---------------- MISC SETTINGS ------------------- """

""" Logging warning suppression (because no plans to upgrade beyond Django 1.8 LTS) """
import logging, copy
from django.utils.log import DEFAULT_LOGGING

LOGGING = copy.deepcopy(DEFAULT_LOGGING)
LOGGING['filters']['suppress_deprecated'] = {
    '()': 'ecobasa.settings.SuppressDeprecated'  
}
LOGGING['handlers']['console']['filters'].append('suppress_deprecated')

class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = [
            'RemovedInDjango19Warning'
        ]
        # Return false to suppress message.
        return not any([warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])


if DEBUG_TOOLBAR_ENABLED:

    INSTALLED_APPS = INSTALLED_APPS + [
        'django_extensions',
        'debug_toolbar',
        'werkzeug_debugger_runserver',
    ]
    
    INTERNAL_IPS = ['127.0.0.1']
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE_CLASSES
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        #'haystack.panels.HaystackDebugPanel',
    ]


""" --------------- COSINNUS SETTINGS ---------------- """

COSINNUS_SITE_PROTOCOL = 'http'

# only for DRJA
COSINNUS_IMPORT_PROJECTS_PERMITTED = False

# this links the django instance running on this settings module to the portal:
SITE_ID = 1

# extra-aggressive Exception raising
DEBUG_LOCAL = True
