import getpass
from openreview.api import OpenReviewClient

username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

BASE_API_URL = "https://api2.openreview.net"

client = OpenReviewClient(baseurl=BASE_API_URL, username=username, password=password)

# To send a general message to all recipients
message_template = """Dear {{fullname}},

xxxxx
xxxxx

Best,
"""

recipients_list = ["~AB_C1", "abc@gmail.com"]
sent = client.post_message(
    message=message_template, recipients=recipients_list, subject="xxx"
)


# To send a personalized message to each recipient
message_template = """Dear {{{{fullname}}}},

xxxxx
{}
xxxxx

Best,
"""

recipients_list = ["~AB_C1", "abc@gmail.com"]
for r in recipients_list:
    message_text = message_template.format("some_info")
    sent = client.post_message(
        message=message_text, recipients=[r], replyTo="xxx", subject="xxx"
    )

# Link to view emails sent: https://openreview.net/messages
# https://openreview-py.readthedocs.io/en/latest/api.html#openreview.Client.post_message
