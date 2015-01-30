"import requests, json"

class Transmission(object):

  def __init__(self):
    """Test"""

  def __translate_keys(self, **kwargs):
    model = {
      'content': {},
      'options': {},
      'recipients': {}
    }

    model['description'] = kwargs.get('description')
    model['return_path'] = kwargs.get('return_path', 'default@sparkpostmail.com')
    model['campaign_id'] = kwargs.get('campaign')
    model['metadata'] = kwargs.get('metadata')
    model['substitution_data'] = kwargs.get('substitution_data')
    model['options']['open_tracking'] = kwargs.get('track_opens', True)
    model['options']['click_tracking'] = kwargs.get('track_clicks', True)
    model['content']['use_draft_template'] = kwargs.get('use_draft_template', False)
    model['content']['reply_to'] = kwargs.get('reply_to')
    model['content']['subject'] = kwargs.get('subject')
    model['content']['from'] = kwargs.get('from')
    model['content']['html'] = kwargs.get('html')
    model['content']['text'] = kwargs.get('text')
    model['content']['email_rfc822'] = kwargs.get('rfc822')
    model['content']['template_id'] = kwargs.get('template')
    model['content']['headers'] = kwargs.get('custom_headers')
    model['recipients']['list_id'] = kwargs.get('recipient_list')
    model['recipients'] = kwargs.get('recipients')

    return model


  def send(self, **kwargs):
    payload = self.__translate_keys(**kwargs)
    "Need to figure out how to get the config stuff into here"
    "headers = { 'authorization': apiKey }"
    "response = requests.post(constructUrl(), data = json.dumps(payload), headers = headers)"
