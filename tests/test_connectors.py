from connectors import PaymentGateway, WebhookEvent, Connector, get_connector

def test_verify_webhook():
    event = WebhookEvent("valid-id", "event", {})
    connector = get_connector(PaymentGateway.STRIPE)
    assert connector.verify_webhook(event) == True

def test_verify_webhook_invalid_id():
    event = WebhookEvent("invalid-id", "event", {})
    connector = get_connector(PaymentGateway.STRIPE)
    assert connector.verify_webhook(event) == False

def test_retry_api_call():
    connector = get_connector(PaymentGateway.STRIPE)
    assert connector.retry_api_call(3) == True

def test_retry_api_call_zero_retries():
    connector = get_connector(PaymentGateway.STRIPE)
    assert connector.retry_api_call(0) == False

def test_map_event():
    event = WebhookEvent("id", "event", {"data": "value"})
    connector = get_connector(PaymentGateway.STRIPE)
    result = connector.map_event(event)
    assert result == {"event": "event", "data": {"data": "value"}}

def test_get_connector():
    connector = get_connector(PaymentGateway.STRIPE)
    assert isinstance(connector, Connector)

def test_get_connector_invalid_gateway():
    try:
        get_connector("invalid-gateway")
        assert False
    except ValueError:
        assert True
