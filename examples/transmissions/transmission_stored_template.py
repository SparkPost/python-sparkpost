from sparkpost import SparkPost

sp = SparkPost()

response = sp.transmission.send(
    recipients=['you@me.com'],
    template='my-template-id',
    use_draft_template=True
)
