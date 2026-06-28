# partner-targets.md

## Partner Integration Roadmap for Revenue Recovery Platform

### Target Integrations

| Partner/API                | Free-Tier Limits                     | Integration Effort | Value-Add (User Job Solved)                                   | Affiliate/Revenue-Share |
|----------------------------|--------------------------------------|--------------------|---------------------------------------------------------------|--------------------------|
| **Stripe**                 | $0 for up to $1 million in revenue  | M                  | Streamlined payment processing and error handling             | Yes                      |
| **PayPal**                 | $0 for up to $10,000/month          | M                  | Facilitates diverse payment methods, reducing failed payments | Yes                      |
| **Chargebee**              | Free for up to 50 customers          | L                  | Subscription management and dunning automation                | Yes                      |
| **Recurly**                | Free for up to 10 subscriptions      | L                  | Advanced subscription billing and analytics                    | Yes                      |
| **Braintree**              | $0 for up to $1 million in revenue  | M                  | Simplifies payment processing and retries                      | Yes                      |
| **Zapier**                 | Free for 5 Zaps                      | S                  | Connects various apps for automated workflows                 | No                       |
| **Twilio**                 | $15 credit for new users             | M                  | Personalized SMS notifications for dunning communications      | No                       |
| **Intercom**               | Free for up to 500 users             | M                  | Customer communication and support for payment-related issues  | No                       |

### Rationale

1. **Stripe**: As one of the most popular payment processors, integrating with Stripe allows for seamless payment retries and effective error handling. Its extensive documentation and support make it a manageable integration.

2. **PayPal**: With a large user base, integrating PayPal can help capture payments that might fail through traditional credit card methods. This integration can reduce churn by offering more payment options.

3. **Chargebee**: This subscription management platform is ideal for SaaS companies and can help automate dunning processes, making it easier to recover lost revenue. The integration effort is higher due to its complexity, but the value it adds is significant.

4. **Recurly**: Similar to Chargebee, Recurly specializes in subscription billing and can provide insights into customer behavior, helping to optimize retry strategies.

5. **Braintree**: Owned by PayPal, Braintree provides robust payment processing capabilities and can help minimize failed payments through intelligent retry mechanisms.

6. **Zapier**: While not directly related to payment processing, Zapier can automate workflows between various applications, enhancing the overall user experience and operational efficiency.

7. **Twilio**: Integrating Twilio allows for personalized SMS notifications, which can significantly improve customer engagement during the dunning process.

8. **Intercom**: This customer communication platform can help address payment-related inquiries and issues, improving customer satisfaction and retention.

### Conclusion

The integration roadmap focuses on partners that provide significant value in minimizing failed payments and enhancing the revenue recovery process. Prioritizing those with affiliate or revenue-share opportunities can also create additional revenue streams for the revenue recovery platform.