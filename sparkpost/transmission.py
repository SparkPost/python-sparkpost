import json
import requests

API_KEY = 'ef44e02616f071677714065510240f29c946fdf0'


class Transmission(object):
    """
    Transmission class used to send, list and find transmissions

    The methods are:
    - send: sends a transmission with the API
    - find: retrieves a particuliar transmission by id
    - list_all: retrieves all transmissions in the system
    """

    def __init__(self):
        """
        Constructor, current is empty
        """

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
        model['content']['from'] = kwargs.get('envelope_from')
        model['content']['html'] = kwargs.get('html')
        model['content']['text'] = kwargs.get('text')
        model['content']['email_rfc822'] = kwargs.get('rfc822')
        model['content']['template_id'] = kwargs.get('template')
        model['content']['headers'] = kwargs.get('custom_headers')
        model['recipients']['list_id'] = kwargs.get('recipient_list')
        model['recipients'] = kwargs.get('recipients')

        return model

    def __construct_url(self, **kwargs):
        config = {
            'options': {
                'protocol': 'https',
                'host': 'api-staging.sparkpost.com',
                'version': 'v1'
            }
        }
        port = ':' + config['options']['port'] if 'port' in config['options'] else ''

        return config['options']['protocol'] + '://' + config['options']['host'] + port + '/api/' + config['options']['version'] + '/transmissions'

    def __fetch(self, transmission_id=False):
        url = self.__construct_url()
        if transmission_id:
            url + '/' + transmission_id
        headers = {
            'Content-Type': 'application/json',
            'Authorization': API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return response.json()['errors']
        else:
            return response.json()

    def send(self, **kwargs):
        """
          Responsible for sending a transmission
        """
        payload = self.__translate_keys(**kwargs)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': API_KEY
        }
        url = self.__construct_url()
        print url

        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code != 200:
            return response.json()['errors']
        else:
            return response.json()

    def find(self, transmission_id):
        """
          Finds a transmission by id
        """
        return self.__fetch(transmission_id)

    def list_all(self):
        """
          Lists all transmissions in system
        """
        return self.__fetch()
