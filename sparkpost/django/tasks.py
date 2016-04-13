from celery import chord
from celery.task import task

from .message import SparkPostMessage


@task()
def send_messages(obj, email_messages):
    """
    Celery task for 'send_messages' EmailBackend method.
    It sends all email messages in parallel via 'send_message' task,
    and then it reduces all results via `send_summary` task (celery chord is convenient)
    """
    return chord(send_message.s(obj, email_message) for email_message in email_messages)(send_summary.s())


@task()
def send_message(obj, message):
    try:
        response = obj._send(SparkPostMessage(message))
    except Exception:
        if not obj.fail_silently:
            raise
    else:
        return response['total_accepted_recipients']


@task()
def send_summary(send_results):
    return sum([send_result for send_result in send_results])
