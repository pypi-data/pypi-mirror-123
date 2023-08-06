# UA-Email-Client

Provides easy interface for sending emails through Amazons Simple Email Service.

## Motivation

To make a python API that could obfuscate the details of sending emails using AWS SES service.

## Code Example

```python
from ua_email_client import ua_email_client

client = ua_email_client.EmailClient(email)
# The template name given should be relative name to a file.
client.add_template("success.html")

# Destinations 
client.send_email(destinations, "success.html", subject, body)
```

## Installation

pip install --user ua-email-client

## Credits

[RyanJohannesBland](https://github.com/RyanJohannesBland)
[EtienneThompson](https://github.com/EtienneThompson)

## License

MIT
