from sparkpost.django.message import EmailMessageWithMetadata, \
    EmailMultiAlternativesWithMetadata


def send_django_email_with_metadata():
    """
    Make sure you setup your Django Email Backend before trying these examples:
    https://github.com/SparkPost/python-sparkpost/blob/master/docs/django/backend.rst

    EmailMessageWithMetadata is just a simple update to Django's EmailMessage
    (https://docs.djangoproject.com/en/2.0/topics/email/#django.core.mail.EmailMessage)
    Which adds a metadata field. The metadata can be sent back to you in
    webhook POSTs from SparkPost. Without these classes, The SparkPost Django
    email backend will not be able to send metadata with the email.
    """

    email = EmailMessageWithMetadata(
        'Hello',
        'Body goes here',
        'from@example.com',
        ['to1@example.com', 'to2@example.com'],
        ['bcc@example.com'],
        reply_to=['another@example.com'],
        headers={'Message-ID': 'foo'},
        metadata={'some_metadata': 'that you want'}
    )

    email.metadata['more_metadata'] = 'true'

    email.send(fail_silently=False)


def send_django_email_alternatives_with_metadata():
    """
    Same as send_django_email_with_metadata(), but using
    EmailMultiAlternativesWithMetadata. See send_django_email_with_metadata()
    doc string for more details
    """
    email = EmailMultiAlternativesWithMetadata(
        'Hello',
        'Body goes here',
        'from@example.com',
        ['to1@example.com', 'to2@example.com'],
        ['bcc@example.com'],
        reply_to=['another@example.com'],
        headers={'Message-ID': 'foo'},)

    email.metadata['more_metadata'] = 'true'

    html_content = '<p>This is an <strong>important</strong> message.</p>'
    email.attach_alternative(html_content, "text/html")

    email.send(fail_silently=False)
