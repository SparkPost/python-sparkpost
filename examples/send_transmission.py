from sparkpost import transmission
t = transmission.Transmission()
response = t.send(recipients = [ { 'address': { 'email': 'bob.evans@messagesystems.com'}}], html = '<p>Hello world</p>', envelope_from = 'test@example.com', subject = 'my sub')
