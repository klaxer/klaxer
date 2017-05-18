"""The main Klaxer server"""

from flask import Flask, request

from klaxer.errors import AuthorizationError
from klaxer.lib import validate
from klaxer.models import Alert

app = Flask(__name__)

@app.route('/alert/<service_name>/<token>', methods=['POST'])
def alert(service_name, token):
    """An incoming alert. The core API method"""
    try:
        validate(service_name, token)
        data = request.get_json()
        alert = Alert.from_service(service_name, data)
        # Classify based on rules (e.g. alert.state = 'critical' if 'keepalive' in alert.text else 'warning')
        # Filter based on rules (e.g. junk an alert if a string is in the body or if it came from a CI bot).
        #Filtered based on user interactions (e.g. bail if we've snoozed the notification type snoozed).
        #Enriched based on custom rules (e.g. all alerts with 'keepalive' have '@deborah' appended to them so Deborah gets an extra level of notification priority.
        #The target channel gets queried for the most recent message. If it's identical, perform rollup. Otherwise, post the alert.
    except AuthorizationError:
        raise
