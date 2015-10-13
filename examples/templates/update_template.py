from sparkpost import SparkPost

sp = SparkPost()
response = sp.templates.update(
    'TEST_ID',
    name='Test Template',
    from_email='test@test.com',
    subject='Updated Test email template!',
    html='<b>This is a test email template! Updated!</b>'
)
print response
