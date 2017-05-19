"""Core methods"""

from enum import Enum
from datetime import datetime

from klaxer import config
from klaxer.errors import AuthorizationError, NoRouteFoundError

class Destination:
    """Base for defining Slack destinations to send `Message`s to."""
    def __init__(self, channel, token=config.SLACK_TOKEN):
        """Initalize the `Destination`.

        :param channel: the Slack channel name to send alerts to
        :param token: the Slack API token to use for requests

        """
        self.channel = channel
        self.token = token
        self.host = 'https://slack.com/api/'
        self._alive = None

    def ping(self):
        """Check to see if the destination is reachable.

        :returns: whether or not the endpoint is available
        :rtype: bool

        """
        method = 'api.test'
        resource = f'{self.host}/{method}?token={self.token}'
        response = make_request(resource)
        self.last_checked = datetime.utcnow()
        self._alive = response.get('ok', False)
        return self._alive

    @property
    def alive(self, window=config.WINDOW):
        """The status of the API based on the last ping.

        :returns: whether or not the API is available
        :rtype: bool

        """
        diff = datetime.utcnow() - self.last_checked
        if diff.total_seconds > window:
            self._alive = self.ping()
        return self._alive

    def send_alert(self):
        logging.warning("Method send_alert not implemented!")
        return


class Slack(Destination):
    """Use Slack as the destination."""
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._channel_id = None
        self._alive = None

    @property
    def channel_id(self):
        """Lazy load the channel ID for `Destination` Slack channel.

        :returns: the channel ID for the given channel name
        :rtype: str

        """
        if not self._channel_id:
            self._channel_id = get_channel_id(self.channel)
        return self._channel_id

    def get_last_message(self, target):
        pass

    def delete_message(self, message):
        pass


class NoValueEnum(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)

class Severity(NoValueEnum):
    WARNING = 'warning'
    CRITICAL = 'critical'
    UNKNOWN = 'unknown'

def validate(service_name, token):
    #TODO: Implement. Raise AuthorizationError if invalid, otherwise just pass through
    pass


def get_channel_id(channel_name):
    """Get the name of a channel given its Slack ID.

    Currently a stub method!

    :param channel_name: the name of the channel to map
    :returns: the ID of the channel
    :rtype: str

    """
    return channel_name


def make_request(url, payload=None):
    with urllib.request.urlopen(url) as response:
        parsed = json.loads(response.read())
    return parsed


def classify(alert, rules):
    """Determine the severity of an alert

    :param alert: The alert to test
    :param rules: An array of classification rules to test against
    """
    for rule in rules:
        severity = rule(alert)
        if severity:
            alert.severity = severity
            break
    else:
        alert.severity = Severity.UNKNOWN
    return alert

def filtered(alert, rules):
    """Determine if an alert meets a rule in a ruleset"""
    return any(rule(alert) for rule in rules)

def enrich(alert, enrichments):
    """Enrich an alert"""
    for enrichment in enrichments:
        updates = enrichment(alert)
        if not updates:
            continue
        for name, value in enrichment(alert).items():
            alert[name] = value
    return alert

def route(alert, routes):
    for target, test in routes:
        if test(alert):
            alert.target = target
            return alert
    raise NoRouteFoundError()

def send(alert):
    slack = Slack()
    last = slack.get_last_message(alert.target)
    if alert == last:
        slack.delete_message(last)
    alert.count += 1 # TODO: actually extract the count from `last`
    slack.send_alert(alert)
