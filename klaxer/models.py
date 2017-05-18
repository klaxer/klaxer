"""Models for DTO and other ops."""

TRANSFORMERS = {
    'sensu': transform_sensu
}

class Alert:
    """An alert. Duh."""

    def __init__(self, service_name, message, timestamp):
        self.service = service_name
        self.message = message
        self.timestamp = timestamp
        self.state = None

    @classmethod
    def from_service(cls, service_name, data):
        """Get an instance of the class with normalized service data"""
        return cls(service_name, *TRANSFORMERS[service_name](data))

def transform_sensu(data):
    """Decompose a sensu alert into arguments for an alert"""
    # TODO: maybe calulate a hashed alert ID here?
    return data.message, data.timestamp
