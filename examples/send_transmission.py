from sparkpost import SparkPost
s = SparkPost('YOUR API KEY')
response = s.transmission.send(recipients = ['bob.evans@messagesystems.com'], html = '<p>Hello world</p>', from_email = 'test@example.com', subject = 'my sub')
