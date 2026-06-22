import json
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Dict

@dataclass
class Customer:
    first_name: str
    plan_name: str
    amount_due: float
    retry_date: str

@dataclass
class EmailTemplate:
    template: str

class PersonalizedDunningEmailGenerator:
    def __init__(self, smtp_config: Dict[str, str] = None, sendgrid_api_key: str = None):
        self.smtp_config = smtp_config
        self.sendgrid_api_key = sendgrid_api_key

    def render_email(self, customer: Customer, email_template: EmailTemplate) -> str:
        template = email_template.template
        return template.replace("{{first_name}}", customer.first_name) \
                       .replace("{{plan_name}}", customer.plan_name) \
                       .replace("{{amount_due}}", str(customer.amount_due)) \
                       .replace("{{retry_date}}", customer.retry_date)

    def send_email(self, customer: Customer, email_template: EmailTemplate, to_email: str) -> None:
        if self.smtp_config:
            # Simulate sending email via SMTP
            print(f"Sending email via SMTP to {to_email}")
        elif self.sendgrid_api_key:
            # Simulate sending email via SendGrid API
            print(f"Sending email via SendGrid API to {to_email}")
        else:
            raise ValueError("Either SMTP config or SendGrid API key must be provided")

    def inject_open_rate_tracking_pixel(self, email: str) -> str:
        # Simulate injecting open-rate tracking pixel
        return email + "<img src='tracking_pixel.png'>"

    def preview_email(self, customer: Customer, email_template: EmailTemplate) -> str:
        rendered_email = self.render_email(customer, email_template)
        return rendered_email
