from sparkpost import SparkPost

sp = SparkPost('YOUR API KEY')

response = sp.transmission.send(
  recipients = ['you@me.com'],
  template = 'my-template-id',
  use_draft_template = True
)
