from email_generator import create_email_generator, Customer
import pytest

@pytest.fixture
def customer():
    return Customer("John", "Basic Plan", 100.0, "2024-09-20")

@pytest.fixture
def email_generator():
    smtp_config = {"host": "smtp.example.com", "port": 587}
    return create_email_generator(smtp_config)

def test_generate_email(customer):
    email_generator = create_email_generator({"host": "smtp.example.com", "port": 587})
    email = email_generator.generate_email(customer)
    assert "Dear John" in email
    assert "Basic Plan" in email
    assert "100.0" in email
    assert "2024-09-20" in email

def test_send_email(email_generator, customer):
    email = email_generator.generate_email(customer)
    email_generator.send_email(email, "john@example.com")
    # No assertion, just testing that it runs without error

def test_render_preview(email_generator, customer):
    email = email_generator.generate_email(customer)
    preview = email_generator.render_preview(email)
    assert preview == email

def test_inject_open_rate_tracking_pixel(email_generator, customer):
    email = email_generator.generate_email(customer)
    email_with_pixel = email_generator.inject_open_rate_tracking_pixel(email)
    assert "<img src='tracking_pixel.png' />" in email_with_pixel

def test_create_email_generator_with_smtp_config():
    smtp_config = {"host": "smtp.example.com", "port": 587}
    email_generator = create_email_generator(smtp_config)
    assert email_generator.smtp_config == smtp_config

def test_create_email_generator_with_sendgrid_api_key():
    sendgrid_api_key = "SG.example.key"
    email_generator = create_email_generator(sendgrid_api_key=sendgrid_api_key)
    assert email_generator.sendgrid_api_key == sendgrid_api_key

def test_create_email_generator_without_config():
    with pytest.raises(ValueError):
        create_email_generator()
