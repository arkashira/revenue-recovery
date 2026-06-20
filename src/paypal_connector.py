import json
from dataclasses import dataclass
from typing import Dict
import hashlib
import hmac
import base64

@dataclass
class PayPalConnector:
    client_id: str
    client_secret: str
    webhook_url: str

    def validate_credentials(self) -> bool:
        # Simulate validation via sandbox
        return self.client_id == "valid_client_id" and self.client_secret == "valid_client_secret"

    def subscribe_to_webhooks(self) -> bool:
        # Simulate subscription to PayPal Webhooks
        return True

    def encrypt_credentials(self) -> Dict:
        encrypted_client_id = base64.b64encode(self.client_id.encode()).decode()
        encrypted_client_secret = base64.b64encode(self.client_secret.encode()).decode()
        return {"client_id": encrypted_client_id, "client_secret": encrypted_client_secret}

    def decrypt_credentials(self, encrypted_credentials: Dict) -> Dict:
        decrypted_client_id = base64.b64decode(encrypted_credentials["client_id"]).decode()
        decrypted_client_secret = base64.b64decode(encrypted_credentials["client_secret"]).decode()
        return {"client_id": decrypted_client_id, "client_secret": decrypted_client_secret}

    def get_connector_status(self) -> str:
        return "Connected" if self.validate_credentials() else "Disconnected"

    def verify_webhook_signature(self, webhook_event: Dict, signature: str) -> bool:
        # Simulate verification of webhook signature
        return hmac.new(self.client_secret.encode(), json.dumps(webhook_event, sort_keys=True).encode(), hashlib.sha256).digest() == base64.b64decode(signature)
