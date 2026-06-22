from personalized_dunning_email_generator import PersonalizedDunningEmailGenerator, Customer, EmailTemplate

def test_render_email():
    customer = Customer("John", "Basic", 10.99, "2024-09-16")
    email_template = EmailTemplate("Hello {{first_name}}, your {{plan_name}} plan is due for {{amount_due}} on {{retry_date}}.")
    generator = PersonalizedDunningEmailGenerator()
    rendered_email = generator.render_email(customer, email_template)
    assert rendered_email == "Hello John, your Basic plan is due for 10.99 on 2024-09-16."

def test_send_email_smtp():
    customer = Customer("John", "Basic", 10.99, "2024-09-16")
    email_template = EmailTemplate("Hello {{first_name}}, your {{plan_name}} plan is due for {{amount_due}} on {{retry_date}}.")
    generator = PersonalizedDunningEmailGenerator(smtp_config={"host": "smtp.example.com", "port": 587})
    generator.send_email(customer, email_template, "john@example.com")

def test_send_email_sendgrid():
    customer = Customer("John", "Basic", 10.99, "2024-09-16")
    email_template = EmailTemplate("Hello {{first_name}}, your {{plan_name}} plan is due for {{amount_due}} on {{retry_date}}.")
    generator = PersonalizedDunningEmailGenerator(sendgrid_api_key="SG.example.api.key")
    generator.send_email(customer, email_template, "john@example.com")

def test_inject_open_rate_tracking_pixel():
    email = "Hello John, your Basic plan is due for 10.99 on 2024-09-16."
    generator = PersonalizedDunningEmailGenerator()
    email_with_pixel = generator.inject_open_rate_tracking_pixel(email)
    assert email_with_pixel == email + "<img src='tracking_pixel.png'>"

def test_preview_email():
    customer = Customer("John", "Basic", 10.99, "2024-09-16")
    email_template = EmailTemplate("Hello {{first_name}}, your {{plan_name}} plan is due for {{amount_due}} on {{retry_date}}.")
    generator = PersonalizedDunningEmailGenerator()
    preview_email = generator.preview_email(customer, email_template)
    assert preview_email == "Hello John, your Basic plan is due for 10.99 on 2024-09-16."
