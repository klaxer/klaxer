"""Core methods"""

from datetime import datetime

from klaxer import config
from klaxer.errors import AuthorizationError, NoRouteFoundError
from klaxer.models import Severity


def validate(service_name, token):
    #TODO: Implement. Raise AuthorizationError if invalid, otherwise just pass through
    pass

    
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
