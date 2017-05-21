"""The main Klaxer server"""

from flask import Flask, request

from klaxer.config import CLASSIFICATION_RULES, ENRICHMENTS, EXCLUSION_RULES, ROUTES
from klaxer.errors import AuthorizationError, NoRouteFoundError
from klaxer.lib import classify, enrich, filtered, route, send, validate
from klaxer.models import Alert

app = Flask(__name__)

CURRENT_FILTERS = []

@app.route('/alert/<service_name>/<token>', methods=['POST'])
def incoming(service_name, token):
    """An incoming alert. The core API method"""
    try:
        validate(service_name, token)
        data = request.get_json()
        alert = Alert.from_service(service_name, data)
        alert = classify(alert, CLASSIFICATION_RULES)
        # Filter based on rules (e.g. junk an alert if a string is in the body or if it came from a CI bot).
        if filtered(alert, EXCLUSION_RULES):
            return
        #Filtered based on user interactions (e.g. bail if we've snoozed the notification type snoozed).
        if filtered(alert, CURRENT_FILTERS):
            return
        #Enriched based on custom rules (e.g. all alerts with 'keepalive' have '@deborah' appended to them so Deborah gets an extra level of notification priority.
        alert = enrich(alert, ENRICHMENTS)
        # Determine where the message goes
        alert = route(alert, ROUTES)
        #The target channel gets queried for the most recent message. If it's identical, perform rollup. Otherwise, post the alert.
        send(alert)
        return "ok"
    except (AuthorizationError, NoRouteFoundError) as error:
        app.logger.exception('Failed to serve an alert response')
        return str(error), 500
