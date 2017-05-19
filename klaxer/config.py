"""Configuration, natch."""

from klaxer.lib import Severity

CLASSIFICATION_RULES = [
    lambda x: Severity.CRITICAL if 'error' in x.message else Severity.WARNING if 'warning' in x.message else None
]

EXCLUSION_RULES = [
    lambda x: 'keepalive' in x.message,
]

ENRICHMENTS = [
    lambda x: {'message': f'@deborah {x.message}'} if 'keepalive' in x.message else None,
]

ROUTES = [
    ('#dmesg', lambda x: x.service == 'root'),
]

# Every 5 minutes
WINDOW = 60 * 5