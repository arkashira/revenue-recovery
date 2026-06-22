import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Config:
    stripe_secret_key: str
    revenue_recover_url: str

class StripeSDK:
    def __init__(self, config: Config):
        self.config = config

    def InitRevenueRecover(self):
        # Register webhook handlers
        self.register_webhook_handler()

    def register_webhook_handler(self):
        # Simulate registering a webhook handler
        # In a real implementation, this would involve making an API call to Stripe
        print("Webhook handler registered")

    def forward_failed_payment(self, event: Dict):
        # Simulate forwarding a failed payment event to RevenueRecover
        # In a real implementation, this would involve making an API call to RevenueRecover
        print("Failed payment event forwarded")

    def handle_webhook(self, event: Dict):
        if event["type"] == "invoice.payment_failed":
            self.forward_failed_payment(event)
        else:
            print("Unhandled event type")
