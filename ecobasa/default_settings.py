# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from os.path import dirname, join, realpath
from django.utils.translation import ugettext_lazy as _

from django.conf.global_settings import *

BASE_PATH = realpath(join(dirname(__file__), '..'))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = join(BASE_PATH, 'media')

# this might be overridden in an out settings file to match the cosinnus Portal's static dir
STATIC_ROOT = join(BASE_PATH, 'static-collected')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(BASE_PATH, 'static'),
)

LOCALE_PATHS = (
    join(BASE_PATH, 'locale'),
)


ROOT_URLCONF = 'ecobasa.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ecobasa.wsgi.application'


""" Import django settings from cosinnus-core.
    Override or add to specific settings here! 
"""

INTERNAL_INSTALLED_APPS = [
   'ecobasa',
]

from cosinnus.default_settings import *
INSTALLED_APPS = compile_installed_apps(internal_apps=INTERNAL_INSTALLED_APPS)


# templates setting is missing base directory. must come after cosinnus.default_settings import!
TEMPLATES[0]['DIRS'] = [join(BASE_PATH, 'templates'),]

LANGUAGES = [
    ('en', _('English')),
    ('de', _('Deutsch')),
    ('es', _('Spanish')),
]

# yes, it's dumb, but we need the ids of all integrated Portals in this list, and this needs to
# be set in the default_settings.py so that ALL portals know that
# this setting is overwritten in a seperate file which is imported by ALL portal settings files
try:
    from .settings_all_portals import COSINNUS_INTEGRATED_PORTAL_IDS
except ImportError:
    COSINNUS_INTEGRATED_PORTAL_IDS = []


# If you run into trouble, update your HAYSTACK_CONNECTIONS on your local settings as
# explained on
# http://django-haystack.readthedocs.org/en/latest/tutorial.html#modify-your-settings-py 
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'cosinnus.backends.RobustElasticSearchEngine',  # replaces 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'ecobasa',
    },
}

WAGTAIL_SITE_NAME = 'ecobasa'

ENDLESS_PAGINATION_PER_PAGE = 8
ENDLESS_PAGINATION_PREVIOUS_LABEL = '<b>&#9001;</b> back'
ENDLESS_PAGINATION_NEXT_LABEL = 'continue <b>&#9002;</b>'

# Make this unique, and don't share it with anybody.
SECRET_KEY = None

# recaptcha
RECAPTCHA_PUBLIC_KEY = None  # needs to be set in local settings.py
RECAPTCHA_PRIVATE_KEY = None  # needs to be set in local settings.py
RECAPTCHA_USE_SSL = True

""" *** The most important settings, definitely customise these for your portal *** """

# this links the django instance running on this settings module to the portal:
SITE_ID = 1
# this MUST be the URL subdomain part. eg. if you're setting up a portal at http://myportal.example.com, set this to 'myportal'
COSINNUS_PORTAL_NAME = 'ecobasa'

# i18n string that is used as the base page title for this portal
COSINNUS_BASE_PAGE_TITLE_TRANS = 'Projektwelt - Мир проектов'
# trigger the translation indexer. leave this, won't trigger otherwise for some reason
_('Projektwelt - Мир проектов')

COSINNUS_RECRUIT_EMAIL_BODY_TEXT = _(''
    '%(sender_name)s hat Dich eingeladen, Dich bei "%(portal_name)s" zu registrieren und dem Projekt "%(team_name)s" beizutreten. '
    'ecobasa vernetzt nachhaltige Gemeinschaften in einem globalen Schenk-Netzwerk. Wir verbinden '
    'Gemeinschaften untereinander, Menschen mit Gemeinschaften und Wünsche mit Angeboten. Damit das Netzwerk funktioniert brauchen wir '
    'dich mit deinen Fähigkeiten, Produkten, deinem Wissen und deinen Erfahrungen. Je mehr Menschen mitmachen, '
    'desto mehr Wünsche gehen in Erfüllung! Du kannst dir im Gegenzug auch alles wünschen und das '
    'wird hoffentlich von jemand anderem im Netzwerk erfüllt. Wir sind schon sehr viele, aber mit dir einer mehr '
    'und einen Schritt weniger von einem funktionierendem globalen Schenknetzwerk entfernt.'
    '<br/><br/>'
    'Mehr Informationen zu ecobasa findest Du auf den folgenden Webseiten:<br/>\n\n'
    '<ul>'
    '<li><a href="https://ecobasa.org/en/about-the-platform/" target="_blank">https://ecobasa.org/en/about-the-platform/</a></li>'
    '<li><a href="https://ecobasa.org/en/about-the-network/" target="_blank">https://ecobasa.org/en/about-the-network/</a></li>'
    '</ul><br/>\n\n'
    'Viel Spaß!'
    '<br/><br/>'
    'Dein ecobasa-Team')


SESSION_COOKIE_DOMAIN = 'ecobasa.org'
SESSION_COOKIE_NAME = 'wechange_ecobasa'

""" *** Add any custom portal-specific settings that affect cosinnus apps here: *** """

# determines which apps public objects are shown on a microsite
# e.g: ['cosinnus_file', 'cosinnus_event', ]
COSINNUS_MICROSITE_DEFAULT_PUBLIC_APPS = ['cosinnus_file', 'cosinnus_event', 'cosinnus_etherpad', 'cosinnus_poll', 'cosinnus_marketplace',]

COSINNUS_BASE_PAGE_TITLE_TRANS = 'ecobasa.org'

COSINNUS_GROUP_OBJECT_MODEL = 'ecobasa.EcobasaCommunityProfile'
COSINNUS_USER_PROFILE_MODEL = 'ecobasa.EcobasaUserProfile'

COSINNUS_ETHERPAD_BASE_URL = 'https://pad.ecobasa.org/api'
COSINNUS_ETHERPAD_API_KEY = '30e6027d19afd4bbdbea69b1370c55552505e8f8d2edf4eb60f7e49fc1e48f04'

COSINNUS_ETHERPAD_ENABLE_ETHERCALC = False
COSINNUS_ETHERPAD_ETHERCALC_BASE_URL = 'https://calc.ecobasa.org'

# settings for email-dkim signing. you can follow this guide for creating a key https://blog.codinghorror.com/so-youd-like-to-send-some-email-through-code/ (point 2)
DKIM_DOMAIN = None # e.g. 'example.com'
DKIM_SELECTOR = None # e.g. 'selector' if using selector._domainkey.example.com
DKIM_PRIVATE_KEY = None # full private key string, including """-----BEGIN RSA PRIVATE KEY-----""", etc
# set these settings in your server's settings.py. then if you have all of them, you also need to include this:
if DKIM_SELECTOR and DKIM_DOMAIN and DKIM_PRIVATE_KEY: 
    EMAIL_BACKEND = 'cosinnus.backends.DKIMEmailBackend'

COSINNUS_SITE_PROTOCOL = 'http'

# should microsites be enabled per default for all portals?
# (can be set for each portal individually in their settings.py)
COSINNUS_MICROSITES_ENABLED = True


""" -----------  More configurable Cosinnus settings (for defaults check cosinnus/conf.py!)  ----------- """

#AWESOME_AVATAR = {...}
#COSINNUS_USER_PROFILE_MODEL = 'cosinnus.UserProfile'
#COSINNUS_ATTACHABLE_OBJECTS = {...}
#COSINNUS_ATTACHABLE_OBJECTS_SUGGEST_ALIASES = {...}
#COSINNUS_INITIAL_GROUP_WIDGETS = [...]
#COSINNUS_INITIAL_GROUP_MICROSITE_WIDGETS = [...]
#COSINNUS_INITIAL_USER_WIDGETS = [...]
#COSINNUS_MICROSITE_DISPLAYED_APP_OBJECTS = [...] 
# Navbar display in the apps menu
#COSINNUS_HIDE_APPS = [(...)]


""" -----------  This app's cosinnus-related custom settings  ----------- """

# new users that register will automatically be assigned these django permission groups
NEWW_DEFAULT_USER_AUTH_GROUPS = ['Pioneers']

# new user that register will automatically become members of these groups/projects (supply group slugs!)
NEWW_DEFAULT_USER_GROUPS = ['Basar']

# the "Home" group for this portal. if not set, some things won't work (like attaching files to direct messages)
NEWW_FORUM_GROUP_SLUG = 'Basar'

# if enabled, group admins will see a "rearrange" button and can re-order the widgets.
# pretty wonky and unintuitive right now, so be careful!
COSINNUS_ALLOW_DASHBOARD_WIDGET_REARRANGE = True

# Default country code to assume when none is entered for django-phonenumber-field
PHONENUMBER_DEFAULT_REGION = 'DE'

# PIWIK settings. set individually for each portal. won't load if PIWIK_SITE_ID is not set
PIWIK_SERVER_URL = '//stats.ecobasa.org/'
PIWIK_SITE_ID = 1

# default from-email:
COSINNUS_DEFAULT_FROM_EMAIL = 'noreply@ecobasa.org'
DEFAULT_FROM_EMAIL = COSINNUS_DEFAULT_FROM_EMAIL

# if activated, an imported user will be merged into an existing one if their emails are matching, 
# even if no override switch is given. their password is retained
COSINNUS_CSV_IMPORT_MERGE_EXISTING_USERS_BY_EMAIL = True


# dict of dicts with settings for each type of importer classes
# COSINNUS_CSV_IMPORT_TYPE_SETTINGS = {
#     'groups': {
#         'IMPORT_CLASS': 'drja.utils.import_utils.DRJAGroupCSVImporter', # extended Importer for DRJA
#     },
#     'users': {
#         'IMPORT_CLASS': 'drja.utils.import_utils.DRJAUserCSVImporter', # extended Importer for DRJA
#     },
# }


""" *** These settings don't usually have to be changed for any portal, so only tamper
    with them if you know what you are doing *** """

""" 
No portals are active yet, so these settings are disabled!

# this overrides the default setting, and is meant to! (a custom django command takes care of the proper static file collection for the right paths)
STATIC_ROOT = join(BASE_PATH, 'static-collected-%s' % COSINNUS_PORTAL_NAME)

# set to use the memcache instance of this portal ID. can be overridden.
if 'memcached' in CACHES['default']['BACKEND']:
    CACHES['default']['LOCATION'] = '127.0.0.1:113%02d' % SITE_ID

# We're adding overriding template dirs for each custom subdomain here,
# in line with django's philosophy of same paths overriding and cascading downwards.
TEMPLATE_DIRS = (
    join(BASE_PATH, 'ecobasa', 'templates_subdomain', COSINNUS_PORTAL_NAME),
) + TEMPLATE_DIRS

# Additional locations of static files
STATICFILES_DIRS = (
    join(BASE_PATH, 'static_subdomain', COSINNUS_PORTAL_NAME),
) + STATICFILES_DIRS
"""

DJAJAX_ALLOWED_ACCESSES = {
    'cosinnus.UserProfile': ('settings', ),
    'ecobasa.EcobasaUserProfile': ('settings', ),
    'ecobasa.EcobasaCommunityProfile': ('settings', ),
    'cosinnus_todo.TodoEntry': ('priority', 'assigned_to', 'is_completed', 'title', ),
    'cosinnus_todo.TodoList': ('title', ),
    'cosinnus_etherpad.Etherpad': ('title', ),
    'cosinnus_file.FileEntry': ('title', ),
}

COSINNUS_GROUP_ADDITIONAL_FORM_FIELDS = ['name_ru', 'description_ru', 'description_long_ru',
     'programs', 'categories', 'date_arrival', 'date_departure', ]
    # hidden:
    # 'trilateral', 'multilateral', 'is_goodpractice', 'ownership', 
    #'participants_requested', 'participants_requested_ru',
    #'participants_accepted', 'participants_accepted_ru', 'participants_final', 'participants_final_ru',
    #'sponsors'

# COSINNUS_GROUP_ADDITIONAL_INLINE_FORMSETS = ['drja.forms.DRJASponsorInlineFormset',]

# GOOGLE_MAPS_GEOCODING_API_SERVER_KEY = 'AIzaSyC4Mro7Ii-mSXnVbLhDpVnxG0uWBKlSn9s'

# determines which apps public objects are shown on a microsite
# e.g: ['cosinnus_file', 'cosinnus_event', ]
COSINNUS_MICROSITE_DEFAULT_PUBLIC_APPS = ['cosinnus_file', 'cosinnus_event', 'cosinnus_etherpad', 'cosinnus_poll', 'cosinnus_marketplace',]

# extended choices for topics
# WARNING: do NOT change remove/change these without a data migration! pure adding is ok.
COSINNUS_TOPIC_CHOICES = (
    ('', ''),
    (1 , _('Education')),
    (2 , _('Governance')),
    (4 , _('Energy')),
    (5 , _('Nutrition and Consumption')),
    (6 , _('Economy')),
    (7 , _('Volunteering')),
    (8 , _('History and politics')),
    (9 , _('Health')),
    (10, _('Art and Culture')),
    (11, _('Media')),
    (12, _('People with impairments')),
    (13, _('Human rights')),
    (14, _('Migration')),
    (15, _('Mobility')),
    (16, _('Music and theater')),
    (17, _('Nature and Environment')),
    (18, _('Spirituality')),
    (19, _('Sport')),
    (20, _('Community')),
    (21, _('Self-Sufficiency')),
    (22, _('Permaculture')),
    (23, _('Personal Development')),
)

COSINNUS_STREAM_SPECIAL_STREAMS = [{
    'title': 'ecobasa',
    'app_models': 'cosinnus_note.Note',
    'group_ids': [1, 2,], # this points to ecobasa core group
}, ]

COSINNUS_MAP_MARKER_ICONS = {
    'people': {
        'url': '/static/img/map_markers/marker_user_neutral.png',
        'width': 40,
        'height': 40
    },
    'events': {
        'url': '/static/img/map_markers/marker_event.png',
        'width': 40,
        'height': 40
    },
    'projects': {
        'url': '/static/img/map_markers/marker_project.png',
        'width': 40,
        'height': 40
    },
    'groups': {
        'url': '/static/img/map_markers/marker_group.png',
        'width': 40,
        'height': 40
    },
}

# send ToS as email after user registration
COSINNUS_SEND_TOS_AFTER_USER_REGISTRATION = True

# COSINNUS_FACEBOOK_INTEGRATION_ENABLED = True
# COSINNUS_FACEBOOK_INTEGRATION_APP_ID = '467240103473755'
# COSINNUS_FACEBOOK_INTEGRATION_APP_SECRET = None # in local settings.py!


# access token set in settings.py
# COSINNUS_CLEVERREACH_AUTO_SIGNUP_ENABLED = True
# COSINNUS_CLEVERREACH_GROUP_IDS = {
#     'default': , # ecobasa Newsletter DE 
#     'de': , # ecobasa Newsletter DE 
#     'ru': , # ecobasa Newsletter RU 
# }
# COSINNUS_CLEVERREACH_FORM_IDS = {
#     1353023: 160019, # Anmeldeformular DE
#     1351659: 157798, # Anmeldeformular RU
# }
