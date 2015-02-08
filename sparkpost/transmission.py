import json

from .base import Resource


class Transmission(Resource):
    """
    Transmission class used to send, list and find transmissions

    The methods are:
    - send: sends a transmission with the API
    - get: retrieves a particuliar transmission by id
    - list: retrieves all transmissions in the system
    """

    key = 'transmissions'

    def _translate_keys(self, **kwargs):
        model = {
            'content': {},
            'options': {},
            'recipients': {}
        }

        model['description'] = kwargs.get('description')
        model['return_path'] = kwargs.get('return_path',
                                          'default@sparkpostmail.com')
        model['campaign_id'] = kwargs.get('campaign')
        model['metadata'] = kwargs.get('metadata')
        model['substitution_data'] = kwargs.get('substitution_data')

        model['options']['open_tracking'] = kwargs.get('track_opens', True)
        model['options']['click_tracking'] = kwargs.get('track_clicks', True)
        model['options']['sandbox'] = kwargs.get('use_sandbox')

        model['content']['use_draft_template'] = \
            kwargs.get('use_draft_template', False)
        model['content']['reply_to'] = kwargs.get('reply_to')
        model['content']['subject'] = kwargs.get('subject')
        model['content']['from'] = kwargs.get('from_email')
        model['content']['html'] = kwargs.get('html')
        model['content']['text'] = kwargs.get('text')
        model['content']['template_id'] = kwargs.get('template')
        model['content']['headers'] = kwargs.get('custom_headers')

        recipient_list = kwargs.get('recipient_list')
        if recipient_list:
          model['recipients']['list_id'] = recipient_list
        else:
          recipients = kwargs.get('recipients', [])
          model['recipients'] = self._extractRecipients(recipients)

        return model

    def _extractRecipients(self, recipients):
      formatted_recipients = []
      for recip in recipients:
        if isinstance(recip, str):
          formatted_recipients.append({'address': {'email': recip}})
        else:
          formatted_recipients.append(recip)
      return formatted_recipients

    def send(self, **kwargs):
        """
        Responsible for sending a transmission

        Args(dict with following keys):
           - recipients: list or dict. If list it is an array of email addresses, if dict {'address': {'name': 'Name', 'email': 'me' }
           - recipient_list: str, id of recipient list, if set recipients above will be ignored
           - template: str, id of template, if set html or text will not be used
           - use_draft_template: boolean, default to False. Set to true if you want to send a template that is a draft
           - html: str, html part of transmission
           - text: str, text part of transmission
           - subject: str, subject of transmission
           - from_email: friendly from of transmission, domain must be a verified sending domain to your account or transmission will fail
           - reply_to: str, reply_to of transmission
           - description: str, description of transmission
           - campaign: str, campaign of transmission
           - metatdata: dict, any data you want to send along with transmission, used in WebHooks
           - substitution_data: dict, corresponds to substitutions in html/text content. see https://www.sparkpost.com/docs/substitutions-reference
           - track_opens: boolean, defaults to True. Used to track opens of transmission
           - track_clicks:  boolean, defaults to True. Used to track clicks of transmission
           - use_sandbox: boolean, flag must be set to use sandbox domain instead of verified sending domain. limited to a lifetime of 50 transmissions with this domain
           - custom_headers: dict. used to set any headers associated with transmission
        """

        payload = self._translate_keys(**kwargs)
        results = self.request('POST', self.uri, data=json.dumps(payload))
        return results

    def get(self, transmission_id):
        """
        Finds a transmission by id

        Args:
           - transmission_id: The id of transmission you want to return

        Returns: https://www.sparkpost.com/docs/transmissions-api
        """
        uri = "%s/%s" % (self.uri, transmission_id)
        results = self.request('GET', uri)
        return results['transmission']

    def list(self):
        "Lists all transmissions in system"
        results = self.request('GET', self.uri)
        return results
