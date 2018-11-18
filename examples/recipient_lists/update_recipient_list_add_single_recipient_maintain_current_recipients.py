from sparkpost import SparkPost


# Example list id. Information on getting one is available here:
# https://developers.sparkpost.com/api/recipient-lists/#recipient-lists-post-create-a-recipient-list
list_id = "1234"

# Change this from None to the recipient email that should be added to the recipient list
email = None

sp = SparkPost()
recipient_list = sp.recipient_lists.get(list_id, True)
current_recipients = recipient_list["recipients"]
recipient_values = [recipient["address"] for recipient in current_recipients]
updated_recipients = [
    {"address": recipient_value} for recipient_value in recipient_values
]
updated_recipients.append({"address": {"email": email.strip().lower(), "name": ""}})
response = sp.recipient_lists.update(
    list_id, name="list name", recipients=updated_recipients
)
