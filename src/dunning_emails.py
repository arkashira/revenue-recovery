import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Dict

@dataclass
class Customer:
    name: str
    amount: float
    last_payment_date: str

class DunningEmails:
    def __init__(self):
        self.email_templates = {
            "first": "Dear {name}, your payment of {amount} is overdue. Please pay by {last_payment_date}.",
            "followup": "Dear {name}, this is a follow-up on your overdue payment of {amount}. Please pay immediately."
        }
        self.send_logs = []

    def send_email(self, customer: Customer, template_name: str, hours_after_failed_payment: int):
        template = self.email_templates[template_name]
        email_body = template.format(name=customer.name, amount=customer.amount, last_payment_date=customer.last_payment_date)
        email = EmailMessage()
        email.set_content(email_body)
        self.send_logs.append({"customer": customer.name, "template": template_name, "delivery_status": "sent", "hours_after_failed_payment": hours_after_failed_payment})
        return email

    def get_send_logs(self):
        return self.send_logs

    def get_customer_data(customer_name: str) -> Dict:
        # In-memory data for testing
        customers = {
            "John Doe": {"name": "John Doe", "amount": 100.0, "last_payment_date": "2024-09-16"},
            "Jane Doe": {"name": "Jane Doe", "amount": 200.0, "last_payment_date": "2024-09-17"}
        }
        return customers.get(customer_name)

def main():
    dunning_emails = DunningEmails()
    customer_name = "John Doe"
    customer_data = DunningEmails.get_customer_data(customer_name)
    if customer_data:
        customer = Customer(**customer_data)
        dunning_emails.send_email(customer, "first", 24)
        dunning_emails.send_email(customer, "followup", 48)
        print(dunning_emails.get_send_logs())

if __name__ == "__main__":
    main()
