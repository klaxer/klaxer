"""Configuration, natch."""

import os

from klaxer.models import Severity

CLASSIFICATION_RULES = [
    lambda x: Severity.CRITICAL if 'error' in x.message.lower() else Severity.WARNING if 'warning' in x.message.lower() else None
]

EXCLUSION_RULES = [
    lambda x: 'keepalive' in x.message,
]

ENRICHMENTS = [
    lambda x: {'message': f'@deborah {x.message}'} if 'keepalive' in x.message else None,
]

ROUTES = [
    ('dmesg', lambda x: x.service == 'root'),
    ('apitests', lambda x: x.service == 'sensu'),
]

SLACK_TOKEN = os.environ.get('KLAXER_TOKEN')
SLACK_SIMULATOR_CHANNEL='#klaxer-test'

# Every 5 minutes
WINDOW = 60 * 5

# Database: Accepts postgresql or sqlite, default is sqlite
DB_CONNECTION = 'sqlite'
#DB_CONNECTION = 'postgresql'

# Inform user, password and host where PostgreSQL server is located
#POSTGRE_USER = ''
#POSTGRE_PASS = ''
#POSTGRE_HOST = '127.0.0.1'


# Messages
MSG_WELCOME = 'Welcome to Klaxer! Let staff know if you have any issues.'
MSG_UNVERIFIED = 'Your account is currently unverified and may be limited until final approval.'