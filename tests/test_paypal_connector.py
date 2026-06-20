import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from paypal_connector import PayPalConnector
import pytest
import base64
import json
import hmac
import hashlib

def test_paypal_connector_validation():
    connector = PayPalConnector("valid_client_id", "valid_client_secret", "webhook_url")
    assert connector.validate_credentials() == True

def test_paypal_connector_invalid_validation():
    connector = PayPalConnector("invalid_client_id", "invalid_client_secret", "webhook_url")
    assert connector.validate_credentials() == False

def test_paypal_connector_subscribe_to_webhooks():
    connector = PayPalConnector("valid_client_id", "valid_client_secret", "webhook_url")
    assert connector.subscribe_to_webhooks() == True

def test_paypal_connector_encrypt_credentials():
    connector = PayPalConnector("valid_client_id", "valid_client_secret", "webhook_url")
    encrypted_credentials = connector.encrypt_credentials()
    assert encrypted_credentials["client_id"] != "valid_client_id"
    assert encrypted_credentials["client_secret"] != "valid_client_secret"

def test_paypal_connector_decrypt_credentials():
    connector = PayPalConnector("valid_client_id", "valid_client_secret", "webhook_url")
    encrypted_credentials = connector.encrypt_credentials()
    decrypted_credentials = connector.decrypt_credentials(encrypted_credentials)
    assert decrypted_credentials["client_id"] == "valid_client_id"
    assert decrypted_credentials["client_secret"] == "valid_client_secret"

def test_paypal_connector_get_connector_status():
    connector = PayPalConnector("valid_client_id", "valid_client_secret", "webhook_url")
    assert connector.get_connector_status() == "Connected"

def test_paypal_connector_verify_webhook_signature():
    connector = PayPalConnector("valid_client_id", "valid_client_secret", "webhook_url")
    webhook_event = {"event": "PAYMENT.SALE.DENIED"}
    signature = base64.b64encode(hmac.new(connector.client_secret.encode(), json.dumps(webhook_event, sort_keys=True).encode(), hashlib.sha256).digest()).decode()
    assert connector.verify_webhook_signature(webhook_event, signature) == True
