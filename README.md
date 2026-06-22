# Stripe SDK
A lightweight SDK for Stripe that automatically forwards failed payment webhooks to RevenueRecover.

## Quick Start
1. Install the SDK using pip: `pip install stripe-sdk`
2. Import the SDK in your Python code: `from src.stripe_sdk import StripeSDK`
3. Create a `Config` object with your Stripe secret key and RevenueRecover URL: `config = Config(stripe_secret_key="your_key", revenue_recover_url="https://example.com")`
4. Initialize the SDK: `sdk = StripeSDK(config)`
5. Call the `InitRevenueRecover` method to register the webhook handler: `sdk.InitRevenueRecover()`
