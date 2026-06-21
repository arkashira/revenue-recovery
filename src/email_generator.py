import json
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Dict, Optional

@dataclass
class Customer:
    first_name: str
    plan_name: str
    amount_due: float
    retry_date: str

class EmailGenerator:
    def __init__(self, smtp_config: Optional[Dict[str, str]] = None, sendgrid_api_key: Optional[str] = None):
        if not smtp_config and not sendgrid_api_key:
            raise ValueError("Either SMTP config or SendGrid API key must be provided")
        self.smtp_config = smtp_config
        self.sendgrid_api_key = sendgrid_api_key

    def generate_email(self, customer: Customer) -> str:
        template = """
Subject: Overdue Payment for {plan_name}

Dear {first_name},

Your payment for {plan_name} is overdue. The amount due is {amount_due}. Please settle this amount by {retry_date} to avoid any further action.

Best regards,
Finance Team
"""
        return template.format(
            first_name=customer.first_name,
            plan_name=customer.plan_name,
            amount_due=customer.amount_due,
            retry_date=customer.retry_date
        )

    def send_email(self, email: str, to_address: str) -> None:
        if self.smtp_config:
            # Simulate sending email via SMTP
            print(f"Sending email via SMTP to {to_address}")
        elif self.sendgrid_api_key:
            # Simulate sending email via SendGrid API
            print(f"Sending email via SendGrid API to {to_address}")

    def render_preview(self, email: str) -> str:
        return email

    def inject_open_rate_tracking_pixel(self, email: str) -> str:
        # Simulate injecting open-rate tracking pixel
        return email + "\n\n<img src='tracking_pixel.png' />"

def create_email_generator(smtp_config: Optional[Dict[str, str]] = None, sendgrid_api_key: Optional[str] = None) -> EmailGenerator:
    return EmailGenerator(smtp_config, sendgrid_api_key)
