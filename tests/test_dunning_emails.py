from src.dunning_emails import DunningEmails, Customer, DunningEmails
import pytest
from datetime import datetime, timedelta

def test_send_email():
    dunning_emails = DunningEmails()
    customer = Customer("John Doe", 100.0, "2024-09-16")
    email = dunning_emails.send_email(customer, "first", 24)
    assert email.get_content() == "Dear John Doe, your payment of 100.0 is overdue. Please pay by 2024-09-16.\n"

def test_get_send_logs():
    dunning_emails = DunningEmails()
    customer = Customer("John Doe", 100.0, "2024-09-16")
    dunning_emails.send_email(customer, "first", 24)
    send_logs = dunning_emails.get_send_logs()
    assert len(send_logs) == 1
    assert send_logs[0]["customer"] == "John Doe"
    assert send_logs[0]["template"] == "first"
    assert send_logs[0]["delivery_status"] == "sent"
    assert send_logs[0]["hours_after_failed_payment"] == 24

def test_get_customer_data():
    customer_name = "John Doe"
    customer_data = DunningEmails.get_customer_data(customer_name)
    assert customer_data == {"name": "John Doe", "amount": 100.0, "last_payment_date": "2024-09-16"}

def test_get_customer_data_not_found():
    customer_name = "Unknown Customer"
    customer_data = DunningEmails.get_customer_data(customer_name)
    assert customer_data is None

def test_send_email_followup():
    dunning_emails = DunningEmails()
    customer = Customer("John Doe", 100.0, "2024-09-16")
    dunning_emails.send_email(customer, "first", 24)
    dunning_emails.send_email(customer, "followup", 48)
    send_logs = dunning_emails.get_send_logs()
    assert len(send_logs) == 2
    assert send_logs[1]["customer"] == "John Doe"
    assert send_logs[1]["template"] == "followup"
    assert send_logs[1]["delivery_status"] == "sent"
    assert send_logs[1]["hours_after_failed_payment"] == 48
