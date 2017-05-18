"""Models for DTO and other ops."""

TRANSFORMERS = {
    'sensu': transform_sensu
}

class Alert:
    """An alert. Duh."""

    def __init__(self, service, message, timestamp):
        self.count = 0
        self.service = service
        self.message = message
        self.timestamp = timestamp
        self.severity = None
        self.target = None

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        return setattr(self, item, value)

    def __hash__(self):
        # Ignore timestamp since this is used to snooze
        return hash((self.severity, self.service, self.message))

    @classmethod
    def from_service(cls, service_name, data):
        """Get an instance of the class with normalized service data"""
        return cls(service_name, *TRANSFORMERS[service_name](data))

def transform_sensu(data):
    """Decompose a sensu alert into arguments for an alert"""
    # TODO: maybe calulate a hashed alert ID here?
    return data.message, data.timestamp

