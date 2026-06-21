import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class PaymentGateway(Enum):
    STRIPE = "stripe"
    BRAINTREE = "braintree"
    RECURLY = "recurly"

@dataclass
class WebhookEvent:
    id: str
    event: str
    data: Dict

class Connector:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def verify_webhook(self, event: WebhookEvent) -> bool:
        # Simulate webhook verification
        return event.id == "valid-id"

    def retry_api_call(self, max_retries: int) -> bool:
        # Simulate retry API call
        return max_retries > 0

    def map_event(self, event: WebhookEvent) -> Dict:
        # Simulate event mapping
        return {"event": event.event, "data": event.data}

class StripeConnector(Connector):
    def __init__(self):
        super().__init__(PaymentGateway.STRIPE)

class BraintreeConnector(Connector):
    def __init__(self):
        super().__init__(PaymentGateway.BRAINTREE)

class RecurlyConnector(Connector):
    def __init__(self):
        super().__init__(PaymentGateway.RECURLY)

def get_connector(gateway: PaymentGateway) -> Connector:
    if gateway == PaymentGateway.STRIPE:
        return StripeConnector()
    elif gateway == PaymentGateway.BRAINTREE:
        return BraintreeConnector()
    elif gateway == PaymentGateway.RECURLY:
        return RecurlyConnector()
    else:
        raise ValueError("Invalid payment gateway")
